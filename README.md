# prototype-builder

面向产品经理的 Codex Skill：将需求快速落地为可运行、可测试的纯 HTML/CSS/JS 交互原型。

## 最新版本能力

- 多页面主流程原型（默认，不是单页静态图）
- 固定框架：左侧页面标签 + 中间原型画布 + 右侧批注面板
- 完整批注能力：新增、编辑、删除、拖拽、高亮、写回 HTML
- 支持单文件交付（`prototype.html`，内联 CSS/JS）
- 内置修改安全流程：改前备份到 `_backups`，改后乱码检查
- 新增截图 1:1 还原流程（中心画布优先）
- 新增 Figma 链接 1:1 还原流程（基于 Figma MCP）
- 新增 Codex CLI / Figma MCP 自举指引

## 目录结构

```text
prototype-builder/
  README.md
  SKILL.md
  scripts/
    scaffold_prototype.py
  references/
    discovery-question-bank.md
    prototype-qa-checklist.md
    template-left-tabs-right-annotations.md
    screenshot-restore-spec.md
    codex-cli-figma-mcp-bootstrap.md
  agents/
    openai.yaml
```

## 环境要求

- Codex（桌面版或支持 skills 的环境）
- Python 3.9+
- 需要 Figma 1:1 还原时：可用的 `codex` CLI 与 Figma MCP

## 快速开始

```bash
python scripts/scaffold_prototype.py --title "Manual Save Test" --pages Home Upload Review --out ./test --single-file
```

生成后可在输出目录看到 `prototype.html`。

## Figma MCP（可选）

需要做 Figma 链接 1:1 还原时：

```bash
codex mcp add figma --url https://mcp.figma.com/mcp
codex mcp list
```

确认列表中存在 `figma` 即可。

## 协作约定

- 修改前先备份到项目 `_backups`
- 修改后执行乱码检查
- 若出现乱码，立即从最新备份恢复并重改

## 维护者发布流程

```bash
git add .
git commit -m "feat: update prototype-builder skill"
git push origin main
```

## License

按团队策略配置（例如 MIT）。
