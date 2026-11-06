#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""微信公众号 HTML 合规校验：禁用标签/属性、span leaf 包裹、半角标点。
用法: check_html.py 推文.html   （0 ERROR 才可发布）
"""
import re
import sys
from html.parser import HTMLParser

BAN = [
    (r"<style[\s>]", "<style> 会被过滤"),
    (r"<script[\s>]", "<script> 会被过滤"),
    (r"</?div[\s>]", "<div> 会被改写，请用 <section>"),
    (r"<link[\s>]", "外部 <link> 被过滤"),
    (r"\sclass\s*=", "class 属性会被剥离"),
    (r"\sid\s*=", "id 属性会被剥离"),
    (r"position\s*:\s*(fixed|absolute|sticky)", "position fixed/absolute/sticky 不支持"),
    (r"float\s*:", "float 不支持"),
    (r"@media", "@media 不支持"),
    (r"@keyframes", "@keyframes 不支持"),
    (r"@import", "@import 不支持"),
    (r"display\s*:\s*grid", "display:grid 不支持"),
    (r"var\s*\(\s*--", "CSS 变量不支持"),
    (r"url\(\s*['\"]?https?://[^)]*\.(woff2?|ttf|otf|eot)", "外部字体不支持"),
]
CJK = re.compile(r"[\u4e00-\u9fff\U00020000-\U0002ffff]")
HALF = re.compile(r"[\u4e00-\u9fff][,;!?]")
QUOTE = re.compile(r"[\"']")
CODE = re.compile(r"monospace|white-space\s*:\s*pre|consolas|sf mono", re.I)


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.leaf = 0
        self.code = 0
        self.leaf_n = 0
        self.unwrapped = []
        self.punct = []

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        leaf = tag == "span" and "leaf" in ad
        code = bool(CODE.search(ad.get("style", "") or ""))
        if leaf:
            self.leaf += 1
            self.leaf_n += 1
        if code:
            self.code += 1
        self.stack.append((tag, leaf, code))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for _, lf, cd in self.stack[i:]:
                    self.leaf -= lf
                    self.code -= cd
                del self.stack[i:]
                break

    def handle_data(self, data):
        t = data.strip()
        if not t or not CJK.search(t):
            return
        if self.leaf == 0:
            self.unwrapped.append(t[:24])
        if self.code == 0 and (HALF.search(t) or QUOTE.search(t)):
            self.punct.append(t[:24])


def main(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    err = []
    for pat, msg in BAN:
        n = len(re.findall(pat, html, re.I))
        if n:
            err.append(f"{msg}（{n} 处）")
    p = P()
    p.feed(html)
    if CJK.search(html) and p.leaf_n == 0:
        err.append('全文没有 <span leaf=""> 包裹，粘贴后样式会丢失')
    print(f"📋 校验: {path}\n   span leaf: {p.leaf_n} 处")
    if err:
        print("❌ ERROR：")
        for e in err:
            print("   •", e)
    if p.unwrapped:
        print(f"⚠️  {len(p.unwrapped)} 处中文未被 span leaf 包裹，例：{p.unwrapped[:3]}")
    if p.punct:
        print(f"⚠️  {len(p.punct)} 处疑似半角标点/直引号，例：{p.punct[:3]}")
    if not err and not p.unwrapped and not p.punct:
        print("\n✅ 完全合规，可直接粘贴到公众号编辑器")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
