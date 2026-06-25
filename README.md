# prototype-builder

一个可复用的 Codex Skill，用于快速生成可运行的纯 HTML/CSS/JS 产品原型，默认包含：左侧页面标签、中间原型画布、右侧批注面板。

## 功能特点

- 多页面主流程原型脚手架（非单页静态图）
- 左侧页面 Tabs + 右侧批注（Annotations）
- 批注支持新增、编辑、删除、拖拽定位、保存回 HTML
- 默认支持单文件交付（`prototype.html`）
- 内置文件安全流程：修改前备份到 `_backups`，修改后编码检查
- 中间画布为完整原型视口，不出现上下左右滚动条

## 目录结构

```text
prototype-builder/
  SKILL.md
  scripts/
    scaffold_prototype.py
  references/
    discovery-question-bank.md
    prototype-qa-checklist.md
    template-left-tabs-right-annotations.md
  agents/
    openai.yaml
```

## 环境要求

- Codex（桌面版或支持 skills 的运行环境）
- Python 3.9+

## 安装方式（给他人使用）

### 方式 1：直接拷贝目录

将 `prototype-builder` 目录复制到目标机器：

- Windows: `C:\Users\<用户名>\.codex\skills\prototype-builder`
- macOS/Linux: `~/.codex/skills/prototype-builder`

复制后重启/刷新 Codex 会话。

### 方式 2：通过 GitHub 仓库安装

1. 克隆仓库到本地。
2. 将仓库中的 `prototype-builder` 目录复制到上述 skills 路径。
3. 重启/刷新 Codex 会话。

## 快速开始

使用脚手架生成单文件原型：

```bash
python scripts/scaffold_prototype.py --title "Manual Save Test" --pages Home Upload Review --out ./test --single-file
```

生成后可在输出目录中看到 `prototype.html`。

## 协作约定（建议）

- 每次改动 skill 文件前先备份到项目 `_backups`
- 每次改动后执行乱码/编码检查
- 若出现乱码，立即回滚最近备份再重改

## 发布到 GitHub（维护者）

在已安装 Git 的环境执行：

```bash
git init
git add .
git commit -m "feat: add prototype-builder skill"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
```

## License

可按你的团队策略添加（例如 MIT）。
