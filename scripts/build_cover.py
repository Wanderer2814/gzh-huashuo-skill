#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 2.37:1 公众号封面（水墨风：左字右画，画块左缘蒙版柔化）。
用法: build_cover.py --art 插画.jpg --out 封面.png [--style h|v] [--title ...] [--sub ...]
要求: Pillow；字体见 FONT_CANDIDATES
"""
import argparse
import pathlib

from PIL import Image, ImageDraw, ImageFont

W, H = 1500, 634
PAPER = (246, 242, 234)
INK = (28, 25, 23)
MUTED = (140, 136, 128)

FONT_CANDIDATES = {
    "song": ["/System/Library/Fonts/Supplemental/Songti.ttc",
             "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
             "C:/Windows/Fonts/simsun.ttc"],
    "latin": ["/System/Library/Fonts/Supplemental/Georgia.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "C:/Windows/Fonts/georgia.ttf"],
}


def load(kind, size, index=0):
    for p in FONT_CANDIDATES[kind]:
        if pathlib.Path(p).exists():
            try:
                return ImageFont.truetype(p, size, index=index)
            except Exception:
                continue
    return ImageFont.load_default()


def art_block(art_path, box_w, box_h, focus=(0.5, 0.0)):
    """把插画按 cover 方式裁成 box_w×box_h，左缘做渐变透明蒙版。"""
    im = Image.open(art_path).convert("RGB")
    sw, sh = im.size
    scale = max(box_w / sw, box_h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    left = int((nw - box_w) * focus[0])
    top = int((nh - box_h) * focus[1])
    tile = im.crop((left, top, left + box_w, top + box_h))

    mask = Image.new("L", (box_w, box_h), 255)
    d = ImageDraw.Draw(mask)
    fade = int(box_w * 0.30)
    for x in range(fade):
        d.line([(x, 0), (x, box_h)], fill=int(255 * (x / fade)))
    return tile, mask


def build(args):
    canvas = Image.new("RGB", (W, H), PAPER)
    if args.art:
        bw = 606 if args.style == "h" else 700
        tile, mask = art_block(args.art, bw, H, focus=(0.5, 0.0))
        canvas.paste(tile, (W - bw, 0), mask)
    d = ImageDraw.Draw(canvas)

    # 顶部笔触线
    for x in range(W):
        a = max(0.0, 1 - x / W * 1.35)
        d.line([(x, 4), (x, 8)], fill=tuple(int(c * a + p * (1 - a)) for c, p in zip(INK, PAPER)))

    title = args.title
    sub = args.sub
    if args.style == "h":
        f = load("song", 94)
        d.text((96, 210), title, font=f, fill=INK)
        d.line([(96, 350), (192, 350)], fill=INK, width=3)
        d.text((96, 384), sub, font=load("latin", 20), fill=MUTED)
    else:
        f = load("song", 58)
        y = 58
        for ch in title:
            d.text((120, y), ch, font=f, fill=INK)
            y += 70
        d.line([(206, 58), (206, 578)], fill=(200, 193, 182), width=1)
        d.line([(252, 96), (372, 96)], fill=INK, width=2)
        for i, line in enumerate(sub.split("|")):
            d.text((252, 130 + i * 34), line, font=load("latin", 17), fill=MUTED)

    canvas.save(args.out)
    canvas.resize((900, 383), Image.LANCZOS).save(
        str(pathlib.Path(args.out).with_name(pathlib.Path(args.out).stem + "_900x383.png")))
    print(f"✓ {args.out} + _900x383")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--art", help="插画路径（可选，缺省为纯纸色排版）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="华说国际经济法")
    ap.add_argument("--sub", default="INTERNATIONAL ECONOMIC LAW TODAY")
    ap.add_argument("--style", choices=["h", "v"], default="h")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
