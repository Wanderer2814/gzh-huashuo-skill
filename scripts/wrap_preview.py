#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把正文片段包成带「复制到公众号」按钮的预览页。
用法: wrap_preview.py 推文.html [输出.html]
"""
import os
import sys

TPL = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>__T__ · 预览</title>
<style>
body{margin:0;background:#eef0f2;font-family:-apple-system,'PingFang SC',sans-serif;-webkit-text-size-adjust:100%}
.bar{position:fixed;top:0;left:0;right:0;height:54px;background:#fff;box-shadow:0 1px 10px rgba(0,0,0,.08);
display:flex;align-items:center;justify-content:space-between;padding:0 16px;z-index:99}
.hint{font-size:13px;color:#6b7280}
.btn{background:#1C1917;color:#fff;border:0;border-radius:9px;padding:10px 20px;font-size:14px;
font-weight:700;cursor:pointer}
.stage{max-width:700px;margin:78px auto 64px;padding:0 8px}
.toast{position:fixed;top:66px;left:50%;transform:translateX(-50%);background:#111827;color:#fff;
padding:11px 20px;border-radius:10px;font-size:14px;font-weight:600;opacity:0;transition:opacity .25s;z-index:100}
.toast.show{opacity:1}
</style></head><body>
<div class="bar"><span class="hint">👇 点右侧「复制到公众号」，再到编辑器粘贴</span>
<button class="btn" onclick="copyIt()">复制到公众号</button></div>
<div class="toast" id="t">已复制，去公众号编辑器 ⌘V 粘贴</div>
<div class="stage"><div id="content">__C__</div></div>
<script>
function copyIt(){
  var el=document.getElementById('content'),r=document.createRange();r.selectNodeContents(el);
  var s=getSelection();s.removeAllRanges();s.addRange(r);
  try{document.execCommand('copy');}catch(e){}
  s.removeAllRanges();
  var t=document.getElementById('t');t.classList.add('show');setTimeout(function(){t.classList.remove('show')},1800);
}
</script></body></html>"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    src = sys.argv[1]
    content = open(src, encoding="utf-8").read().strip()
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + "_预览.html"
    title = os.path.splitext(os.path.basename(src))[0]
    open(out, "w", encoding="utf-8").write(
        TPL.replace("__T__", title).replace("__C__", content))
    print(f"✓ 预览页：{out}")


if __name__ == "__main__":
    main()
