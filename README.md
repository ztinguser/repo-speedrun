# Repo Speedrun 🏎️

几分钟内读懂一个陌生的 GitHub 仓库。

Repo Speedrun 是一个 Codex Skill。它会从仓库的公开入口出发，沿着真实代码调用关系追踪一条代表性执行路径，并生成一份带有源码链接的限时阅读路线。

## 能得到什么

使用 Repo Speedrun 后，你会获得：

- 一份 30 秒仓库简介；
- 一条代表性的运行链路；
- 一份 5、15 或 30 分钟阅读路线；
- 固定到具体 commit 的 GitHub 源码链接；
- 与运行链路相关的测试，或有代码证据支持的测试缺口；
- 可选的后续深入阅读方向。

它不会简单罗列“看起来重要”的文件，而是尝试回答：

```text
程序从哪里开始？
→ 控制流经过了哪些模块？
→ 核心行为在哪里发生？
→ 最终产生了什么可观察结果？
```

## 安装

让 Codex 从下面的地址安装 Skill：

```text
https://github.com/ztinguser/repo-speedrun/tree/master/skills/repo-speedrun
```

例如，可以向 Codex 发送：

```text
请安装这个 Skill：
https://github.com/ztinguser/repo-speedrun/tree/master/skills/repo-speedrun
```

安装完成后，在新的对话中使用 `$repo-speedrun`。

## 使用方法

### 快速浏览仓库

```text
使用 $repo-speedrun 分析这个仓库：
https://github.com/charmbracelet/gum

阅读预算：5 分钟
```

### 追踪指定功能

```text
使用 $repo-speedrun 追踪 `gum input` 命令的执行过程：
https://github.com/charmbracelet/gum

阅读预算：15 分钟
```

还可以提供具体的分支、标签、目录或文件链接，以缩小分析范围。

## 工作方式

Repo Speedrun 会：

1. 获取并验证目标 GitHub 仓库；
2. 确定本次分析使用的准确 commit；
3. 找到一个公开入口；
4. 根据真实的定义、导入、注册和函数调用追踪执行路径；
5. 找到相关测试，或指出有证据支持的测试缺口；
6. 将结果压缩成符合阅读预算的代码导览。

仓库中的内容只会被当作分析证据，不会被当作需要执行的指令。

## 阅读预算

| 预算 | 适合场景 | 路线长度 |
| --- | --- | --- |
| 5 分钟 | 快速判断仓库是否值得深入 | 3–4 个检查点 |
| 15 分钟 | 理解一条完整的核心流程 | 5–7 个检查点 |
| 30 分钟 | 深入理解运行接线、边界和测试 | 7–10 个检查点 |

## 开发

在仓库根目录运行测试：

```powershell
python -m unittest discover -s tests -v
```

测试覆盖：

- 仓库清单文件识别；
- 入口文件候选识别；
- 测试文件候选识别；
- 文件信号组合分类；
- 真实临时 Git 仓库的快照生成。

## 项目结构

```text
repo-speedrun/
├─ skills/repo-speedrun/   可安装的 Codex Skill
├─ tests/                  自动化测试
└─ evals/                  行为评测案例
```

## 开源许可证

本项目基于 [MIT License](./LICENSE) 开源。