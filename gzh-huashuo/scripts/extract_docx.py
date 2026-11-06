#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docx → markdown + images/（纯标准库）。用法: extract_docx.py 稿.docx -o out.md"""
import argparse
import pathlib
import re
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    z = zipfile.ZipFile(a.docx)
    rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    rid2file = {r.get("Id"): r.get("Target") for r in rels}
    root = ET.fromstring(z.read("word/document.xml"))

    outdir = pathlib.Path(a.out).parent
    imgdir = outdir / "images"
    imgdir.mkdir(parents=True, exist_ok=True)

    lines, n = [], 0
    for p in root.iter(f"{W}p"):
        buf = []
        for node in p.iter():
            if node.tag == f"{W}t" and node.text:
                buf.append(node.text)
            elif node.tag == f"{A}blip":
                rid = node.get(f"{R}embed")
                src = rid2file.get(rid)
                if src:
                    n += 1
                    ext = pathlib.Path(src).suffix or ".png"
                    name = f"{n:02d}-image{n}{ext}"
                    (imgdir / name).write_bytes(z.read("word/" + src.lstrip("/")))
                    buf.append(f"\n![](images/{name})\n")
        text = "".join(buf).strip()
        if text:
            lines.append(text)

    lines = [re.sub(r"^[\u3000\s]+|[\u3000\s]+$", "", l) for l in lines]
    out = "\n\n".join([l for l in lines if l])
    pathlib.Path(a.out).write_text(out, encoding="utf-8")
    print(f"✓ {a.out}  段落 {len(lines)} · 图片 {n}")


if __name__ == "__main__":
    main()
