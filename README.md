# Agent Harness 101

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Pages](https://img.shields.io/badge/deployed-GitHub%20Pages-blue.svg)](https://albert-lv.github.io/harness-101)

《从零构建 AI Agent 与 Harness Engineering 实战课程》静态课程站点。

> **English**: This is the static course site for "Build AI Agents and Harness Engineering from Scratch" (Chinese).

本课程以 **Harness 12-Factor** 为主线组织：前置 → F1-F12 → 进阶阅读 → 结课项目。每章提供骨架代码（`starter/`）与参考实现（`solution/`），把“能跑的 Agent”打磨成“可上线 Harness”。

## 📚 Course Contents

A hands-on course covering:

- AI Agent fundamentals and design patterns
- Harness Engineering for reliable, observable agent systems
- The **Harness 12-Factor** methodology:
  1. Single Agent Loop
  2. Explicit Tool Contract
  3. Context Budgeting
  4. Failure-First Design
  5. Graceful Degradation
  6. Least-Privilege Tooling
  7. Human-in-the-Loop Gates
  8. Observable by Default
  9. Reproducible Runs
  10. Composable Agents
  11. Config-Driven Behavior
  12. Continuous Evaluation
- Tool use, planning, memory, sandboxing, and evaluation
- Building production-ready agent workflows

## 🚀 Quick Start

No build step required. Open the course directly:

```bash
# macOS / Linux
open index.html

# Windows
start index.html
```

Or serve it locally:

```bash
python -m http.server 8000
# Visit http://localhost:8000
```

## 🌐 Deploy

### Cloudflare Pages（默认）

本项目通过 `wrangler.jsonc` 部署到 Cloudflare Pages：

```bash
npx wrangler pages deploy .
```

访问：<https://harness-101.pages.dev/>

### GitHub Pages（备选）

1. Push the `main` branch to GitHub.
2. Go to **Settings → Pages**.
3. Select **Deploy from a branch**.
4. Choose `main` and root `/`.
5. Visit `https://<username>.github.io/harness-101/`.

## 🏗️ Repository Structure

```
├── index.html                 # Single-file course website (CSS/JS inlined)
├── agent-harness-course.md    # Course Markdown source (single source of truth)
├── GLOSSARY.md                # Consistent terminology for contributors
├── examples/                  # Per-Factor starter code and reference solutions
│   ├── prep/                  # 前置：环境与第一次 API 调用
│   ├── factor-1/              # Single Agent Loop
│   ├── factor-2/              # Explicit Tool Contract
│   ├── factor-3/              # Context Budgeting
│   ├── factor-4/              # Failure-First Design
│   ├── factor-5/              # Graceful Degradation
│   ├── factor-6/              # Least-Privilege Tooling
│   ├── factor-7/              # Human-in-the-Loop Gates
│   ├── factor-8/              # Observable by Default
│   ├── factor-9/              # Reproducible Runs
│   ├── factor-10/             # Composable Agents
│   ├── factor-11/             # Config-Driven Behavior
│   └── factor-12/             # Continuous Evaluation
├── wrangler.jsonc             # Cloudflare Pages deployment config
├── sitemap.xml                # Sitemap for search engines
├── robots.txt                 # Robots directives
├── _headers                   # Cloudflare Pages response headers
├── README.md                  # This file
└── CONTRIBUTING.md            # Contribution guidelines
```

## ✏️ Contributing

Content changes should be made in `agent-harness-course.md` first, then synchronized to `index.html`.

For typo fixes, content corrections, or translation proposals, please open an [Issue](https://github.com/albert-lv/harness-101/issues) or [Pull Request](https://github.com/albert-lv/harness-101/pulls).

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🔗 Keywords

`ai-agent` `agent-engineering` `harness-engineering` `llm` `prompt-engineering` `tool-use` `rag` `course` `education` `chinese` `github-pages`
