# Scholar Engine - Academic Paper Search and BibTeX Generator

> Quickly and reliably search for academic papers and generate standard BibTeX citations

[中文版本](README_zh.md) | Read this in Chinese

## 🎯 Project Background

With the rise of AI agents that can automatically conduct research, there's a critical gap: **most agents lack proper tools to search and cite academic papers**. While agents can write and analyze, they need reliable access to scholarly literature with proper citation formats.

This project fills that gap by providing a robust academic paper search tool that:
- 🔍 Searches academic papers via Semantic Scholar API
- 📋 Returns papers with **BibTeX format citations** ready to use
- 🤖 Enables AI agents to autonomously search literature and write papers
- ⚡ Features multi-API key and proxy management for higher rate limits

Whether you're building an AI research assistant, writing a paper with AI help, or just need a reliable way to search academic literature, this tool provides the missing link between AI agents and scholarly knowledge.

## 🌟 Key Features

- 🚀 **Quick Start** - One-click API service startup
- 🔍 **Precision Search** - Search papers using Semantic Scholar API
- 🔑 **Multi-API Key Management** - Automatic rotation with intelligent health monitoring
- 🌐 **Proxy Support** - Flexible proxy configuration
- 📋 **Standard BibTeX** - One-click access to professional citation formats
- 🎯 **Simple API** - RESTful design for easy integration

## 🚀 Quick Start

### 1. Start the Service

```bash
# Method 1: Direct run
python main.py

# Method 2: Using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8111

# Method 3: Using startup script
./start.sh
```

### 2. Access API Documentation

After starting, visit in your browser:
- **Swagger UI**: http://localhost:8111/docs
- **ReDoc**: http://localhost:8111/redoc

### 3. Quick Tests

```bash
# Health check
curl http://localhost:8111/health

# Search papers
curl "http://localhost:8111/search?query=attention&limit=3"

# Get BibTeX
curl "http://localhost:8111/bibtex/10.48550/arXiv.1706.03762"
```

## 📖 Detailed Usage Guide

### Python Example

```python
from search import AcademicCitationTool

# Initialize (automatically loads from config directory)
tool = AcademicCitationTool()

# Search papers
result = tool.search_and_get_citations("Attention Is All You Need", limit=2)
print(result)

# Get BibTeX by DOI
bibtex = tool.get_single_paper_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

### Configure API Keys

Add your Semantic Scholar API keys to `config/api_keys.txt` (one per line):

```txt
your_api_key_here
another_api_key_here
```

Configure proxies in `config/proxies.txt` (one per line, optional):

```txt
null
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:8080
```

For detailed configuration, please refer to [ADVANCED_CONFIG.md](ADVANCED_CONFIG.md).

## 📁 Project Structure

```
scholar_engine/
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation (English)
├── README_zh.md            # Project documentation (Chinese)
├── academic_keywords.json  # Academic keywords database
├── config/                 # Configuration directory
│   ├── api_keys.txt.example# API key configuration example
│   └── proxies.txt.example # Proxy configuration example
├── main.py                 # FastAPI main application
├── paper_search_with_citation/
│   └── SKILL.md            # Paper search with citation agent skill
├── requirements.txt        # Dependencies list
├── search.py               # Semantic Scholar API implementation
└── start.sh                # Quick startup script
```

## 🎯 Core Features

### AcademicCitationTool (search.py)

- **Search Functionality**: Search for academic papers by keywords
- **BibTeX Generation**: Get standard BibTeX citation formats
- **API Key Management**: Automatic rotation with health status tracking
- **Proxy Support**: HTTP/HTTPS proxies with authentication support
- **Rate Limiting**: Intelligent detection and recovery mechanisms
- **Fallback Solution**: Alternative methods when official BibTeX is unavailable

## 📚 Additional Documentation

- [API Usage Guide](API_USAGE_GUIDE.md) - Detailed curl command examples
- [Advanced Configuration Guide](ADVANCED_CONFIG.md) - Multi-API key and proxy configuration
- [Solutions Description](SOLUTIONS.md) - Technical implementation details

## 🤖 Claude Skill - Paper Search with Citation

This project includes a custom Claude agent skill to help you use the API more effectively:

### Paper Search with Citation Skill

- **Location**: `paper_search_with_citation/SKILL.md`
- **Purpose**: Guide users through calling the deployed academic search API using bash commands
- **Target Audience**: AI agents and users running the API locally or on their own infrastructure
- **Designed for**: Agent automation and integration into research workflows

### Key Skill Features

This skill provides comprehensive guidance for AI agents and users:
- **API Endpoint Examples**: All available endpoints with detailed examples
- **curl Command Templates**: Copy-paste commands for quick testing
- **Parameter Documentation**: Clear explanations of all search parameters
- **BibTeX Generation**: One-click access to professional citation formats
- **Health Monitoring**: Check API server status
- **Statistics & Analytics**: View API manager performance metrics
- **Formatted Output**: jq integration for clean, readable results

### How to Install the Skill in Claude Code

To use the Paper-Search-with-Citation skill in Claude Code, you need to install it first. The skill can be installed either for this specific project or globally for all projects.

#### Option 1: Project-Level Installation (Recommended)

1. Create the skills directory in your project:
```bash
mkdir -p .claude/skills/paper_search_with_citation
```

2. Copy the skill file:
```bash
cp paper_search_with_citation/SKILL.md .claude/skills/paper_search_with_citation/
```

3. The skill is now available for this project only.

#### Option 2: Global Installation

1. Locate your Claude Code global configuration directory (usually in your home folder):
   - On Linux/macOS: `~/.claude/skills/`
   - On Windows: `%USERPROFILE%\.claude\skills\`

2. Create the skill directory:
```bash
mkdir -p ~/.claude/skills/paper_search_with_citation
```

3. Copy the skill file:
```bash
cp paper_search_with_citation/SKILL.md ~/.claude/skills/paper_search_with_citation/
```

4. The skill is now available for all your Claude Code projects.

## 💡 Common Questions

**Q: Do I need an API Key?**

A: Yes, the Semantic Scholar API requires an API Key. You can:
- Configure API keys in config/api_keys.txt (recommended)
- Or set the SEMANTIC_SCHOLAR_API_KEY environment variable

**Q: How to get an API Key?**

A: Please visit [Semantic Scholar Developer](https://www.semanticscholar.org/developer) to apply for a free API Key.

**Q: How to configure proxies?**

A: Add proxy configurations line by line in config/proxies.txt, supporting various formats. See [ADVANCED_CONFIG.md](ADVANCED_CONFIG.md) for details.

## 🤝 Contribution

Welcome to submit Issues and Pull Requests!

## 📄 License

MIT License

---

**Note**: For Chinese documentation, please refer to [README_zh.md](README_zh.md). If you're new to the project, it's recommended to start with the [API Usage Guide](API_USAGE_GUIDE.md) for detailed step-by-step examples!
