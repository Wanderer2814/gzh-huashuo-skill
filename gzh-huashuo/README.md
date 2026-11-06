# gzh-huashuo · 「华说国际经济法」公众号排版技能

给 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 用的 skill：把推送稿 docx 排成可直接粘贴的公众号 HTML（水墨学术风），并提供封面图生成与合规校验。

## 安装

```bash
git clone <this-repo> ~/.dsh/skills/gzh-huashuo
```

装好后在会话里说「用华说模板排这篇推送稿」即可触发；或直接调用脚本：

```bash
python3 scripts/build_article.py spec.json -o 推文.html --avatar assets/masthead-avatar.jpg
python3 scripts/check_html.py 推文.html
python3 scripts/wrap_preview.py 推文.html
```

## 依赖

- Python 3.9+（标准库即可；封面生成需要 Pillow）
- 字体：macOS 自带 Songti SC / PingFang SC；其它平台请在 `scripts/build_cover.py` 里改 `FONT_CANDIDATES`

## 内容

```
SKILL.md                 # 工作流（agent 读这个）
references/template-spec.md    # 完整排版规范与 checklist
scripts/build_article.py # spec.json → 水墨模板 HTML
scripts/build_cover.py   # 2.37:1 封面（横排/竖排）
scripts/check_html.py    # 公众号合规校验（禁用标签 + span leaf + 半角标点）
scripts/wrap_preview.py  # 带「复制到公众号」按钮的预览页
assets/                  # 刊头头像等自有资产（不含第三方插画）
examples/                # 可跑样例
```

## 版权

- 代码与模板：MIT
- `assets/` 中的头像是本号自有资产，随本技能一并提供
- 技能**不含**任何第三方插画素材；使用者需自行提供图片并确保授权

## 与 gzh-design 的关系

另有一个通用排版技能 `gzh-design`（AGPL，作者甲木 × 摸鱼小李），主题库更全。本技能是**独立的专用模板**，自带校验与预览脚本、不依赖它；两者可共存。

## 发布到 DSH 插件市场

DSH 市场（`dsh-market` 插件）会自动索引 **GitHub 上带 `dsh-plugin` topic 的仓库**，所以发布 = 推一个仓库：

```bash
cd gzh-huashuo
git init && git add -A && git commit -m "init: gzh-huashuo skill"
git remote add origin git@github.com:<你的账号>/gzh-huashuo.git
git push -u origin main
```

然后在 GitHub 仓库页面 **Settings → Topics** 加上：

```
dsh-plugin
deepseek-harness
agent-skills
wechat
chinese
```

市场下次抓取（约数小时）后即可在插件市场搜到；也可以直接把仓库地址发给别人 `git clone <repo> ~/.dsh/skills/gzh-huashuo` 安装。
