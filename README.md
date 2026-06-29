# prototype-builder

面向产品经理的 Codex Skill：将需求快速落地为可运行、可测试的纯 HTML/CSS/JS 交互原型。

## 最新版本能力

- 多页面主流程原型（默认，不是单页静态图）
- 固定框架：左侧页面标签 + 中间原型画布 + 右侧批注面板
- 完整批注能力：新增、编辑、删除、拖拽、高亮、写回 HTML
- 支持单文件交付（`prototype.html`，内联 CSS/JS）
- 内置修改安全流程：改前备份到 `_backups`，改后乱码检查
- 新增截图 1:1 还原流程（中心画布优先）
- 新增 Figma 链接 1:1 还原流程（基于 `figma-bridge`）
- 新增 `figma-bridge` MCP 配置指引

## 本次更新（2026-06-29）

- 移除自动安装 Codex CLI / Figma MCP 的流程要求
- 改为用户在 Codex MCP 配置中添加 `figma-bridge`
- 收到 Figma 链接后，优先使用 `figma-bridge` 的 `get_design_context` 还原选中节点

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
- 需要 Figma 1:1 还原时：已配置的 `figma-bridge` MCP

## 快速开始

```bash
python scripts/scaffold_prototype.py --title "Manual Save Test" --pages Home Upload Review --out ./test --single-file
```

生成后可在输出目录看到 `prototype.html`。

## Figma MCP（可选）

需要做 Figma 链接 1:1 还原时，将以下内容添加到 Codex 的 MCP 配置中：

```json
{
  "figma-bridge": {
    "command": "npx",
    "args": ["-y", "@gethopp/figma-mcp-bridge"]
  }
}
```

用户发送 Figma 链接后，优先通过 `figma-bridge` 的 `get_design_context` 对选中节点进行 1:1 还原。

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
