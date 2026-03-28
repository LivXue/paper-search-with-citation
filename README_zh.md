# Paper-Search-with-Citation Skill

> 快速、稳定地搜索学术论文并获取 BibTeX 引用格式

[中文版本](README_zh.md) | Read this in Chinese

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

### 1. 配置 Semantic Scholar API Key

在使用服务之前，您需要配置 Semantic Scholar API 密钥：

1. 从 [Semantic Scholar Developer](https://www.semanticscholar.org/product/api#api-key-form) 申请免费的 API 密钥
2. 创建或编辑 `config/api_keys.txt` 文件
3. 将您的 API 密钥添加到该文件中（每行一个密钥）：

```bash
# 如果 config 目录不存在则创建
mkdir -p config

# 创建 api_keys.txt 文件并添加您的 API 密钥
echo "your_semantic_scholar_api_key_here" > config/api_keys.txt
```

### 2. 启动服务

```bash
# 方式 1: 直接运行
python main.py

# 方式 2: 使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8111

# 方式 3: 使用启动脚本
./start.sh
```

### 3. 安装 Claude Code Skill

API 启动后，安装 Paper-Search-with-Citation skill 以在 Claude Code 中使用：

```bash
# 创建技能目录
mkdir -p .claude/skills/paper_search_with_citation

# 复制技能文件
cp paper_search_with_citation/SKILL.md .claude/skills/paper_search_with_citation/
```

### 4. 验证安装并访问 API 文档

```bash
# 健康检查
curl http://localhost:8111/health

# 在浏览器中访问 API 文档：
# - Swagger UI: http://localhost:8111/docs
# - ReDoc: http://localhost:8111/redoc
```

有关 API 使用的更多信息，请查看文档：
- API 文档: http://localhost:8111/docs

## 📖 详细使用指南

### 响应格式

API 为所有端点返回标准化的 JSON 响应。以下是搜索结果的详细格式：

#### 搜索响应格式
```json
{
  "success": true,
  "query": "attention",
  "total_results": 3,
  "papers": [
    {
      "index": "10.48550/arXiv.1706.03762",
      "title": "Attention Is All You Need",
      "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin",
      "year": 2017,
      "venue": "Neural Information Processing Systems",
      "doi": "10.48550/arXiv.1706.03762",
      "citation_count": 12345,
      "is_open_access": true,
      "fields_of_study": ["Computer Science", "Artificial Intelligence"],
      "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
      "url": "https://www.semanticscholar.org/paper/10.48550/arXiv.1706.03762",
      "bibtex": "@article{Vaswani2017AttentionIA,\n  title={Attention Is All You Need},\n  author={Ashish Vaswani and Noam Shazeer and Niki Parmar and Jakob Uszkoreit and Llion Jones and Aidan N. Gomez and Lukasz Kaiser and Illia Polosukhin},\n  journal={Neural Information Processing Systems},\n  year={2017}\n}"
    }
  ],
  "message": "Success",
  "api_key_used": 0
}
```

#### 论文对象字段
| 字段 | 类型 | 描述 |
|------|------|------|
| `index` | string | 论文标识符（通常是 DOI 或 Semantic Scholar 论文 ID） |
| `title` | string | 论文标题 |
| `authors` | string | 作者列表（格式："作者1, 作者2, ..."） |
| `year` | integer | 发表年份（未知时为 null） |
| `venue` | string | 发表 venue（期刊、会议等） |
| `doi` | string | DOI（数字对象标识符） |
| `citation_count` | integer | 引用次数 |
| `is_open_access` | boolean | 是否开放获取 |
| `fields_of_study` | array | 研究领域列表 |
| `abstract` | string | 论文摘要（不可用时为 null） |
| `url` | string | 论文在 Semantic Scholar 上的 URL |
| `bibtex` | string | BibTeX 引用（仅当 `include_bibtex=true` 时包含） |

#### 错误响应格式
```json
{
  "success": false,
  "query": "无效查询",
  "total_results": 0,
  "papers": [],
  "message": "解释失败原因的错误信息",
  "api_key_used": null
}
```

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
├── .gitignore              # Git 忽略规则
├── README.md               # 项目说明文档（英文）
├── README_zh.md            # 项目说明文档（中文）
├── academic_keywords.json  # 学术关键词数据库
├── config/                 # 配置文件目录
│   ├── api_keys.txt.example# API 密钥配置示例
│   └── proxies.txt.example # 代理配置示例
├── main.py                 # FastAPI 主程序
├── paper_search_with_citation/
│   └── SKILL.md            # 论文搜索与引用 agent skill
├── requirements.txt        # 依赖包列表
├── search.py               # Semantic Scholar API 实现
└── start.sh                # 快速启动脚本
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

## 🤖 Claude Skill - Paper-Search-with-Citation

本项目包含一个自定义的 Claude agent Skill，帮助您更有效地使用 API：

### Paper-Search-with-Citation Skill

- **位置**: `paper_search_with_citation/SKILL.md`
- **用途**: 指导用户如何使用 bash 命令调用部署好的文献搜索 API
- **目标用户**: AI agent 和在本地或自有基础设施上运行 API 的用户
- **设计目的**: Agent 自动化和集成到研究工作流中

### Skill 核心功能

本 Skill 为 AI agent 和用户提供了全面的指导：
- **API 端点示例**: 所有可用端点的详细示例
- **curl 命令模板**: 可直接复制使用的命令
- **参数文档**: 清晰的搜索参数说明
- **BibTeX 生成**: 一键获取专业引用格式
- **健康监控**: 检查 API 服务器状态
- **统计分析**: 查看 API 管理器性能指标
- **格式化输出**: 使用 jq 进行清晰的结果展示

### 如何在 Claude Code 中安装 Skill

要在 Claude Code 中使用 Paper-Search-with-Citation skill，您需要先安装它。Skill 可以安装在项目级别或全局级别。

#### 选项 1：项目级安装（推荐）

1. 在项目中创建技能目录：
```bash
mkdir -p .claude/skills/paper_search_with_citation
```

2. 复制技能文件：
```bash
cp paper_search_with_citation/SKILL.md .claude/skills/paper_search_with_citation/
```

3. 技能现在仅适用于此项目。

#### 选项 2：全局安装

1. 找到 Claude Code 全局配置目录（通常在您的主文件夹中）：
   - Linux/macOS: `~/.claude/skills/`
   - Windows: `%USERPROFILE%\.claude\skills\`

2. 创建技能目录：
```bash
mkdir -p ~/.claude/skills/paper_search_with_citation
```

3. 复制技能文件：
```bash
cp paper_search_with_citation/SKILL.md ~/.claude/skills/paper_search_with_citation/
```

4. 技能现在可用于您所有的 Claude Code 项目。

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
