import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).parent.parent
RAMP = " .`:-=+*cs#%@"
COLS = 100
CROP = (296, 372, 664, 724)
BACKGROUND = 215
CHAR_W, ROW_H, PAD = 6, 12, 14
NBSP = " "


def to_rows(photo: Path) -> list[str]:
    crop = Image.open(photo).convert("L").crop(CROP)
    rows = int(COLS * crop.height / crop.width * 0.5)
    background = np.asarray(crop.resize((COLS, rows), Image.BILINEAR)).astype(float) > BACKGROUND

    big = np.asarray(crop.resize((COLS * 4, rows * 8), Image.LANCZOS)).astype(float)
    subject = big < BACKGROUND
    lo, hi = np.percentile(big[subject], 2), np.percentile(big[subject], 98)
    stretched = Image.fromarray((np.clip((big - lo) / (hi - lo), 0, 1) * 255).astype("uint8"))
    mask = Image.fromarray((subject * 255).astype("uint8"))
    sharp = ImageOps.equalize(stretched, mask=mask).filter(ImageFilter.UnsharpMask(radius=3, percent=150))
    light = np.asarray(sharp.resize((COLS, rows), Image.LANCZOS)).astype(float) / 255

    top = len(RAMP) - 1
    lines = []
    for r in range(rows):
        line = ""
        for c in range(COLS):
            line += " " if background[r, c] else RAMP[max(1, min(top, int(light[r, c] * top + 0.5)))]
        lines.append(line.rstrip())
    return lines


def to_svg(lines: list[str]) -> str:
    width = COLS * CHAR_W + PAD * 2
    height = len(lines) * ROW_H + PAD * 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" rx="10" fill="#0d1117"/>',
        '<g font-family="ui-monospace, SFMono-Regular, Consolas, Menlo, monospace" font-size="10" fill="#b1bac4">',
    ]
    for i, line in enumerate(lines):
        text = line.lstrip()
        if not text:
            continue
        x = PAD + (len(line) - len(text)) * CHAR_W
        y = PAD + i * ROW_H
        begin = round(0.3 + i * 0.07, 2)
        length = len(text) * CHAR_W
        parts.append(
            f'<clipPath id="r{i}"><rect x="{x}" y="{y}" width="0" height="{ROW_H}">'
            f'<animate attributeName="width" from="0" to="{length}" begin="{begin}s" dur="0.5s" fill="freeze"/></rect></clipPath>'
            f'<text x="{x}" y="{y + ROW_H - 3}" textLength="{length}" lengthAdjust="spacing" clip-path="url(#r{i})">'
            f'{text.replace(" ", NBSP)}</text>'
        )
    parts.append("</g></svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    photo = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts" / "source-photo.jpg"
    out = ROOT / "assets" / "portrait.svg"
    out.write_text(to_svg(to_rows(photo)), encoding="utf-8")
    print(out, out.stat().st_size)
