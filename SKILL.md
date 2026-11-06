---
name: gzh-huashuo
description: 「华说国际经济法」公众号排版工作流（水墨学术风）。把 docx/md/纯文本里的单篇或多篇文章，排成可直接粘贴进微信公众号编辑器的 HTML：水墨刊头（半身头像＋宋体刊名＋英文副行＋右对齐日期）、墨色栏目标签、宣纸色卡片、END 线与两行署名（文字｜杨国华 / 编辑｜陈志康），并提供 2.37:1 封面图与合规校验。触发场景：(1) 用户提到「华说国际经济法」「华说」公众号要发文；(2) 用户要把推送稿 docx 排成公众号推文；(3) 用户要这套水墨模板的封面图/头像配套；(4) 用户要给这套模板加栏目、改署名、改配色。
---

# 华说国际经济法 · 公众号排版工作流

把一个「推送稿」变成可直接粘贴的公众号推文。**版式固定、颜色固定、署名固定**——不做二次创作，只做排版。

## 一、这套模板长什么样

```
──────────────  笔触线（墨色，左浓右淡，2px）
[半身头像58²]  华说国际经济法                     2026年11月2日
              INTERNATIONAL ECONOMIC LAW TODAY
──────────────  1px 淡墨线
标题（宋体 25px，墨色）
[栏目]（墨色描边胶囊）
正文（苹方 15px / 1.85，纯文本，不加任何标记）
图片（宣纸色卡片：4px 内边距 + 1px 描边）
「相关资料」灰卡（宣纸底 #FAF7F1）
        E N D（墨色渐变短线）
                    文字｜杨国华
                    编辑｜陈志康
        华说国际经济法 · 日期
```

**铁律**
- ❌ 不用朱印/红印章（已废弃）；刊头左侧是**半身头像小图**
- ❌ 正文**不加下划线、不加粗、不加高亮**——原文没标就不标
- ❌ 不出现「点赞/在看/转发/留言」，也不出现付费/会员/价格字样
- ❌ 不主动加小标题；原文有「一、二、」才用墨色左竖条小标题
- ✅ 栏目、图片、资料卡按原文结构走，一个不漏
- ✅ 日期右对齐；署名固定两行 `文字｜杨国华` / `编辑｜陈志康`

## 二、工作流（5 步）

### 0. 取稿
用户会给 `.docx`（常含多篇，如《推送稿(4)》）。先抽文字与图片：

```bash
python3 scripts/extract_docx.py 推送稿.docx -o out.md    # 依赖 python-docx 或标准库解包
```
若手边没有该脚本，用 `python-docx` 或 unzip + 解析 `word/document.xml` 取段落与 `word/media/*`。
**多篇稿子要按标题＋日期切开，一篇一推文**，除非用户明确要合刊。

### 1. 结构确认（默认做，除非用户说"直接排"）
把识别结果报给用户：共 N 篇、每篇标题/日期/图片数/是否有资料链接。
**这一步 10 秒，拦住整篇返工。**

### 2. 写 spec（JSON）
按 `examples/spec-example.json` 组织：

```json
{
  "title": "保障措施成热门话题",
  "date": "2026年11月2日",
  "column": "前沿观察",
  "blocks": [
    {"type": "p", "text": "第一段……"},
    {"type": "label", "text": "相关推文"},
    {"type": "imgs", "paths": ["a.jpeg","b.jpeg"], "mode": "card"},
    {"type": "links", "items": [{"title":"…","url":"…"}]}
  ]
}
```
支持块：`p` / `subhead` / `label` / `date_right` / `imgs`(card|full) / `links`。

### 3. 生成 HTML
```bash
python3 scripts/build_article.py spec.json -o 推文.html --avatar assets/masthead-avatar.jpg
```

### 4. 校验（强制）
```bash
python3 scripts/check_html.py 推文.html     # 必须 0 ERROR / 0 WARNING
```
它查：禁用标签与属性（style/script/div/class/id/position/float/@media）、
中文文本是否都被 `<span leaf="">` 包裹、正文里的半角标点与直引号。

### 5. 出预览页（一键复制）
```bash
python3 scripts/wrap_preview.py 推文.html   # 生成 *_预览.html
```
交付话术：**打开预览页 → 右上角「复制到公众号」→ 编辑器 ⌘V**。

## 三、封面图（2.37:1）

公众号封面首图比例 2.35–2.37:1，本模板用 **1500×634**（后台另存 900×383）。

```bash
python3 scripts/build_cover.py --out 封面.png --art 你的插画.jpg
```
两种版式：横排（左字右画）、竖排（竖排刊名＋竖线）。画块左缘用渐变蒙版柔化进纸色，**不留硬接缝**。

**人物构图规则（重要）**：封面里的**人物只露上半身、被底边裁掉**，不要放整个人；头部约在画面 45–50% 高度、人物居横向 75% 左右。

## 四、颜色与字体

```
墨     #1C1917      正文墨灰 #3F3A35      辅助灰 #8A837B
淡墨线 #DED7CB      卡片描边 #E6DFD2      宣纸底 #FAF7F1
标题/刊名  Songti SC（宋体）；正文 PingFang SC
```
需要强调「华说」二字时可换楷体/行楷，或用清华紫 `#660874`（详见 references/template-spec.md 的方案表）。

## 五、素材与版权

- 本技能**不自带**任何第三方插画；`assets/` 里的头像是本号自有资产，插画请自备（自摄/委托/授权/公有领域）。
- 图片一律 **base64 内嵌**进 HTML，否则粘到公众号会掉图：
  ```python
  import base64, pathlib
  uri = "data:image/jpeg;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
  ```
- 刊头头像用小图（260px 压缩版即可），否则单篇 HTML 会到 1MB 以上。

## 六、常见坑

| 坑 | 现象 | 解法 |
|---|---|---|
| 漏 `<span leaf="">` | 粘贴后样式整片丢失 | 跑 `check_html.py` |
| 中文里混半角逗号/直引号 | 校验 WARNING | 全角化，引号用 “”「」 |
| 截图满宽铺开 | 占掉半篇篇幅 | 截图卡片固定 420px 居中 |
| 图片用相对路径 | 公众号显示裂图 | 必须 base64 内嵌 |
| 正文自作主张加下划线 | 与「不做二次强调」冲突 | 删掉 |
| 封面人物全身入画 | 与既定构图不符 | 裁到腰部，底边裁切 |

## 七、参考文件

- `references/template-spec.md`：完整规范（四段式骨架、色板、checklist、待定项、华说二字方案表）
- `examples/spec-example.json` + `examples/sample-article.html`：可跑的样例
