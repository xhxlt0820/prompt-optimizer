# 🔧 Prompt Optimizer

> AI Prompt Quality Analyzer & Optimizer - Improve your AI prompts with instant feedback

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/prompt-optimizer.svg)](https://pypi.org/project/prompt-optimizer/)

## 🎯 What It Does

**Prompt Optimizer** is a CLI tool that analyzes the quality of your AI prompts and suggests improvements. It helps you:

- ✨ **Analyze** prompt quality (scored 0-100)
- 💡 **Identify** missing components (role, task, format, etc.)
- 🛠️ **Optimize** prompts using structured frameworks (RTF, CREATE)
- 📊 **Estimate** token usage for cost calculation

## 🚀 Quick Start

```bash
# Install
pip install prompt-optimizer

# Analyze a prompt
prompt-optimizer "Write a blog about Python"

# Improve a prompt
prompt-optimizer "Code a web scraper" --improve

# Use CREATE framework
prompt-optimizer "Build a todo app" --framework CREATE --improve
```

## 📊 Quality Framework

Prompts are scored based on 8 components:

| Component | Weight | Description |
|-----------|--------|-------------|
| Length | 20% | Sufficient detail |
| Role | 15% | AI persona/persona assignment |
| Task | 15% | Clear action verbs |
| Format | 10% | Output structure specified |
| Example | 10% | Desired output example |
| Constraint | 10% | Boundaries and limits |
| Context | 10% | Background information |
| Steps | 5% | Step-by-step instructions |

## 📦 Frameworks

| Framework | Description | Best For |
|-----------|-------------|----------|
| RTF | Role-Task-Format | Quick, simple prompts |
| CREATE | Comprehensive structure | Complex tasks |
| CREATE-MORE | Extended with meta | Professional/production |

## 💰 Support

If this tool helps you, consider supporting the project:

- **GitHub Sponsors**: https://github.com/sponsors/xhxlt0820
- **USDC (Base)**: `0x1a1d74e0cf80757784e30a9e8ce15d78033c4426`
- **Alipay**: xiaohuxian@gmail.com

## 📄 License

MIT License - feel free to use, modify, and distribute!
