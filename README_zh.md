# Scholar Engine - 学术文献搜索与 BibTeX 生成工具

> 快速、稳定地搜索学术论文并生成标准 BibTeX 引用格式

[English Version](README.md) | 英文版本

## 🎯 项目背景

随着能够自动进行研究的 AI Agent 的兴起，存在一个关键缺口：**大多数 Agent 缺乏搜索和引用学术文献的合适工具**。虽然 Agent 可以写作和分析，但它们需要可靠的学术文献访问渠道和规范的引用格式。

本项目填补了这一空白，提供了一个强大的学术论文搜索工具，它能够：
- 🔍 通过 Semantic Scholar API 搜索学术论文
- 📋 返回论文及 **BibTeX 格式引用**，立即可用
- 🤖 使 AI Agent 能够自主搜索文献和撰写论文
- ⚡ 具备多 API Key 和代理管理，提升搜索速率限制

无论您是在构建 AI 研究助手、使用 AI 辅助撰写论文，还是只是需要一个可靠的学术文献搜索方式，本工具都提供了 AI Agent 与学术知识之间缺失的连接。

## 🌟 主要功能

- 🚀 **快速启动** - 一键运行 API 服务
- 🔍 **精准搜索** - 使用 Semantic Scholar API 搜索论文
- 🔑 **多 API Key 管理** - 自动轮换，智能健康检测
- 🌐 **代理支持** - 灵活的代理配置
- 📋 **标准 BibTeX** - 一键获取专业引用格式
- 🎯 **简洁 API** - RESTful 设计，易于集成

## 🚀 快速开始

### 1. 启动服务

```bash
# 方式 1: 直接运行
python main.py

# 方式 2: 使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8111

# 方式 3: 使用启动脚本
./start.sh
```

### 2. 访问 API 文档

启动后，在浏览器中访问：
- **Swagger UI**: http://localhost:8111/docs
- **ReDoc**: http://localhost:8111/redoc

### 3. 快速测试

```bash
# 健康检查
curl http://localhost:8111/health

# 搜索论文
curl "http://localhost:8111/search?query=attention&limit=3"

# 获取 BibTeX
curl "http://localhost:8111/bibtex/10.48550/arXiv.1706.03762"
```

## 📖 详细使用指南

### Python 示例

```python
from search import AcademicCitationTool

# 初始化（自动从 config 目录加载配置）
tool = AcademicCitationTool()

# 搜索论文
result = tool.search_and_get_citations("Attention Is All You Need", limit=2)
print(result)

# 通过 DOI 获取 BibTeX
bibtex = tool.get_single_paper_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

### 配置 API Keys

在 `config/api_keys.txt` 中添加您的 Semantic Scholar API keys（每行一个）：

```txt
your_api_key_here
another_api_key_here
```

在 `config/proxies.txt` 中配置代理（可选，每行一个）：

```txt
null
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:8080
```

详细配置请参考 [ADVANCED_CONFIG.md](ADVANCED_CONFIG.md)

## 📁 项目结构

```
scholar_engine/
├── main.py                 # FastAPI 主程序
├── search.py               # Semantic Scholar API 实现
├── academic_keywords.json  # 学术关键词数据库
├── config/                 # 配置文件目录
│   ├── api_keys.txt        # API 密钥配置
│   ├── api_keys.txt.example# API 密钥配置示例
│   ├── proxies.txt         # 代理配置
│   ├── proxies.txt.example # 代理配置示例
│   └── last_used.json      # API 密钥使用记录
├── ADVANCED_CONFIG.md      # 高级配置指南
├── CLAUDE.md               # Claude Code 工具配置
├── SOLUTIONS.md            # 解决方案说明
├── README.md               # 项目说明文档（英文）
├── README_zh.md            # 项目说明文档（中文）
├── requirements.txt        # 依赖包列表
├── start.sh                # 快速启动脚本
├── .claude/                # Claude IDE 集成配置
│   └── skills/
│       └── paper_search/
│           └── SKILL.md    # Claude IDE skill
├── paper_search_with_citation/
│   └── SKILL.md            # 论文搜索与引用 skill
└── docs/                   # 文档目录
    └── superpowers/        # 技术文档
```

## 🎯 核心特性

### AcademicCitationTool（search.py）

- **搜索功能**: 通过关键词搜索学术论文
- **BibTeX 生成**: 获取标准 BibTeX 引用格式
- **API Key 管理**: 自动轮替，健康状态追踪
- **代理支持**: HTTP/HTTPS 代理，支持认证
- **速率限制**: 智能检测和恢复机制
- **降级方案**: 无法获取官方 BibTeX 时的替代方案

## 📚 更多文档

- [API 使用指南](API_USAGE_GUIDE.md) - 详细的 curl 命令示例
- [高级配置指南](ADVANCED_CONFIG.md) - 多 API Key 和代理配置
- [解决方案说明](SOLUTIONS.md) - 技术实现细节

## 🤖 Claude Skill - 论文搜索与引用

本项目包含两个自定义的 Claude Skill，帮助您更有效地使用 API：

### 1. 论文搜索与引用 Skill

- **位置**: `paper_search_with_citation/SKILL.md`
- **用途**: 指导用户如何使用 bash 命令调用部署好的文献搜索 API
- **适用场景**: 在本地或自有基础设施上运行 API 的用户

### 2. 使用学术搜索 API Skill（IDE 集成）

- **位置**: `.claude/skills/paper_search/SKILL.md`
- **用途**: 为 Claude Code（claude.ai/code）提供专业的 IDE 集成支持
- **适用场景**: 使用 Claude Code 进行研究和写作的开发者

### Skill 核心功能

两个 Skill 都提供了全面的指导：
- **API 端点示例**: 所有可用端点的详细示例
- **curl 命令模板**: 可直接复制使用的命令
- **参数文档**: 清晰的搜索参数说明
- **BibTeX 生成**: 一键获取专业引用格式
- **健康监控**: 检查 API 服务器状态
- **统计分析**: 查看 API 管理器性能指标
- **格式化输出**: 使用 jq 进行清晰的结果展示

### 如何在 Claude Code 中使用 Skill

#### 步骤 1：激活 Skill（Claude Code）

1. 在 VS Code 或 Claude Code IDE 中打开项目
2. 在 Claude Code 输入框中输入 `/skill`
3. 选择"Paper Search with Citation"或"Using Academic Search API"
4. Skill 会加载所有可用的命令和示例

#### 步骤 2：使用 Skill 命令快速开始

```bash
# 健康检查（获取 API 状态）
curl http://localhost:8111/health

# 搜索"attention"相关论文，包含 BibTeX（限制 3 个结果）
curl -X POST "http://localhost:8111/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "attention",
    "limit": 3,
    "include_bibtex": true
  }'

# 通过 DOI 获取特定论文的 BibTeX
curl "http://localhost:8111/bibtex/10.48550/arXiv.1706.03762"
```

### Skill 使用场景

#### 场景 1：学术写作

> "我正在写一篇关于 transformer 架构的论文，需要找到相关的引用。"

1. 激活 Paper Search with Citation Skill
2. 使用搜索端点，查询关键词 "transformer architecture"
3. 将 BibTeX 结果直接复制到 LaTeX 文档中
4. 通过 DOI 验证引用

#### 场景 2：研究探索

> "我想探索量子机器学习的最新论文。"

1. 激活 Using Academic Search API Skill
2. 使用查询 "quantum machine learning" 搜索，limit=10
3. 使用 jq 解析结果，提取论文标题和作者
4. 从格式化输出中分析趋势

#### 场景 3：API 监控

> "我需要检查本地 API 服务器是否正常运行。"

1. 使用 Skill 中的健康检查命令
2. 监控 API 管理器统计信息，跟踪性能
3. 获取 API 密钥健康状态和代理状态的实时信息

### Skill 配置

两个 Skill 都已为常见使用场景预先配置：

- **本地开发**: 指向 http://localhost:8111
- **远程部署**: 可自定义到您的服务器地址
- **IDE 集成**: 自动检测项目上下文
- **文档链接**: 直接访问 Swagger UI 和 ReDoc

### 为什么使用 Claude Skill？

1. **速度**: 在 IDE 中即时访问所有 API 命令，无需离开工作环境
2. **准确性**: 已验证的示例与您的项目配合使用
3. **一致性**: 所有团队成员使用标准化命令
4. **生产力**: 可复制粘贴的命令用于快速原型开发
5. **学习性**: 为初学者和专家提供清晰的解释

Claude Skill 使这个学术搜索工具对所有技能水平的研究人员、学生和开发者都可访问。

## 💡 常见问题

**Q: 需要 API Key 吗？**

A: Semantic Scholar API 需要 API Key。您可以：
- 在 config/api_keys.txt 中配置 API keys（推荐）
- 或设置 SEMANTIC_SCHOLAR_API_KEY 环境变量

**Q: 如何获取 API Key？**

A: 请访问 [Semantic Scholar Developer](https://www.semanticscholar.org/developer) 申请免费的 API Key。

**Q: 如何配置代理？**

A: 在 config/proxies.txt 中每行添加一个代理配置，支持多种格式。详见 [ADVANCED_CONFIG.md](ADVANCED_CONFIG.md)。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**提示**: 如果您是新手，建议从 [API 使用指南](API_USAGE_GUIDE.md) 开始，那里有详细的 step-by-step 示例！
