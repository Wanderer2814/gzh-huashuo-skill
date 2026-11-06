#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""spec.json → 水墨模板公众号 HTML（华说国际经济法版式）。
用法: build_article.py spec.json -o 推文.html [--avatar assets/masthead-avatar.jpg]
"""
import argparse
import base64
import html as H
import json
import pathlib
import sys

INK, BODY, MUTED = "#1C1917", "#3F3A35", "#8A837B"
LINE, CARD, PAPER, WHITE = "#DED7CB", "#E6DFD2", "#FAF7F1", "#FFFFFF"
SONG = "'Songti SC','STSong','Songti TC',serif"
FONT = ("-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB',"
        "'Microsoft YaHei',sans-serif")
BRAND_CN, BRAND_EN = "华说国际经济法", "INTERNATIONAL ECONOMIC LAW TODAY"
BYLINE = [("文字｜杨国华"), ("编辑｜陈志康")]


def leaf(t):
    return f'<span leaf="">{t}</span>'


def uri(p):
    p = pathlib.Path(p)
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def build(spec, avatar_uri):
    A = []
    add = A.append
    add(f'<section style="max-width:677px;margin:0 auto;background:{WHITE};font-family:{FONT};'
        f'color:{BODY};line-height:1.8;letter-spacing:0.5px;overflow-x:hidden;">')

    # 刊头
    add('<section style="padding:16px 10px 0;">')
    add(f'<section style="height:2px;background:linear-gradient(to right,rgba(28,25,23,.92) 0%,'
        f'rgba(28,25,23,.55) 42%,rgba(28,25,23,.16) 76%,rgba(28,25,23,0) 100%);">'
        f'<span leaf=""><br></span></section>')
    add('<section style="display:flex;align-items:center;justify-content:space-between;'
        'margin:14px 0 18px;">')
    add(f'<section style="display:flex;align-items:center;">'
        f'<section style="width:58px;height:58px;padding:2px;background:{WHITE};'
        f'border:1px solid {LINE};box-sizing:border-box;">'
        f'{leaf(f"<img src=\"{avatar_uri}\" style=\"width:100%;height:100%;display:block;object-fit:cover;\">")}'
        f'</section>'
        f'<section style="margin-left:13px;">'
        f'<p style="font-family:{SONG};font-size:16px;font-weight:700;color:{INK};'
        f'letter-spacing:2px;margin:0;line-height:1.35;">{leaf(BRAND_CN)}</p>'
        f'<p style="font-size:9px;color:{MUTED};letter-spacing:0.8px;margin:4px 0 0;line-height:1.3;">'
        f'{leaf(BRAND_EN)}</p></section></section>')
    add(f'<p style="font-size:11px;color:{MUTED};letter-spacing:1px;margin:0;text-align:right;'
        f'white-space:nowrap;">{leaf(spec["date"])}</p>')
    add('</section>')
    add(f'<section style="height:1px;background:{LINE};margin-bottom:24px;">'
        f'<span leaf=""><br></span></section>')
    add(f'<h3 style="font-family:{SONG};font-size:25px;font-weight:700;color:{INK};'
        f'margin:0 0 13px;line-height:1.45;letter-spacing:1px;">{leaf(spec["title"])}</h3>')
    if spec.get("subtitle"):
        add(f'<p style="font-size:14px;color:{MUTED};margin:0 0 12px;line-height:1.7;">'
            f'{leaf(spec["subtitle"])}</p>')
    if spec.get("column"):
        add(f'<p style="margin:0 0 26px;"><span style="display:inline-block;border:1px solid {INK};'
            f'color:{INK};font-size:11px;font-weight:700;padding:1px 10px;border-radius:3px;'
            f'letter-spacing:2px;">{leaf(spec["column"])}</span></p>')
    add('</section>')

    # 内容
    add('<section style="padding:0 10px;">')
    for b in spec.get("blocks", []):
        t = b.get("type")
        if t == "p":
            add(f'<p style="margin-bottom:20px;font-size:15px;line-height:1.85;'
                f'text-align:justify;">{leaf(b["text"])}</p>')
        elif t == "subhead":
            add(f'<p style="font-family:{SONG};font-size:16px;font-weight:700;color:{INK};'
                f'margin:28px 0 16px;padding-left:11px;border-left:2px solid {INK};'
                f'line-height:1.6;">{leaf(b["text"])}</p>')
        elif t == "label":
            add(f'<p style="font-size:12px;font-weight:700;color:{MUTED};letter-spacing:2px;'
                f'margin:10px 0 12px;padding-left:11px;border-left:2px solid {INK};'
                f'line-height:1.4;">{leaf(b["text"])}</p>')
        elif t == "date_right":
            add(f'<p style="text-align:right;font-size:12px;color:{MUTED};letter-spacing:1px;'
                f'margin:-4px 0 22px;">{leaf(b["text"])}</p>')
        elif t == "imgs":
            paths, mode = b["paths"], b.get("mode", "card")
            for i, p in enumerate(paths):
                mb = "0" if i == len(paths) - 1 else "14px"
                src = uri(p)
                if mode == "card":
                    add(f'<section style="width:420px;max-width:100%;margin:0 auto {mb};'
                        f'background:{WHITE};padding:4px;border:1px solid {CARD};'
                        f'box-shadow:0 3px 10px -4px rgba(28,25,23,0.14);box-sizing:border-box;">'
                        f'{leaf(f"<img src=\"{src}\" style=\"width:100%;height:auto;display:block;\">")}'
                        f'</section>')
                else:
                    add(f'<section style="margin:0 0 {mb};background:{WHITE};padding:4px;'
                        f'border:1px solid {CARD};box-shadow:0 3px 10px -4px rgba(28,25,23,0.14);'
                        f'box-sizing:border-box;">'
                        f'{leaf(f"<img src=\"{src}\" style=\"max-width:100%;height:auto;display:block;margin:0 auto;\">")}'
                        f'</section>')
        elif t == "links":
            add(f'<section style="background:{PAPER};border:1px solid {CARD};padding:16px 18px;'
                f'margin:6px 0 22px;">')
            for it in b["items"]:
                add(f'<p style="font-size:13px;color:{INK};font-weight:700;margin:0 0 4px;'
                    f'line-height:1.7;text-align:justify;">{leaf(it["title"])}</p>')
                add(f'<p style="font-size:11px;color:{MUTED};margin:0 0 12px;line-height:1.7;'
                    f'word-break:break-all;">{leaf(H.escape(it["url"]))}</p>')
            add('</section>')
    add('</section>')

    # END
    add('<section style="padding:0 10px;"><section style="text-align:center;margin:34px 0 18px;">'
        '<section style="display:flex;align-items:center;justify-content:center;">'
        f'<span style="height:1.5px;width:64px;background:linear-gradient(to right,transparent,{INK});'
        'margin-right:12px;"><span leaf=""><br></span></span>'
        f'<span style="font-family:{SONG};font-size:11px;color:{INK};letter-spacing:4px;'
        f'font-weight:700;">{leaf("E N D")}</span>'
        f'<span style="height:1.5px;width:64px;background:linear-gradient(to left,transparent,{INK});'
        'margin-left:12px;"><span leaf=""><br></span></span></section></section></section>')

    # 署名
    add('<section style="padding:0 10px;">')
    for i, name in enumerate(BYLINE):
        mb = "3px" if i == 0 else "12px"
        add(f'<p style="text-align:right;font-family:{SONG};font-size:13px;color:{INK};'
            f'font-weight:700;margin:0 0 {mb};letter-spacing:1px;line-height:1.9;">{leaf(name)}</p>')
    add(f'<p style="text-align:right;font-size:11px;color:{MUTED};margin:0 0 30px;'
        f'letter-spacing:1px;">{leaf(BRAND_CN + " · " + spec["date"])}</p></section>')

    add('</section>')
    return "\n".join(A)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--avatar", default=str(pathlib.Path(__file__).parent.parent /
                                            "assets/masthead-avatar.jpg"))
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text(encoding="utf-8"))
    out = build(spec, uri(a.avatar))
    pathlib.Path(a.out).write_text(out, encoding="utf-8")
    print(f"✓ {a.out}（{len(out)} 字符）")


if __name__ == "__main__":
    main()
