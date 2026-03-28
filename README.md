# Scholar Engine - Academic Paper Search and BibTeX Generator

> Quickly and reliably search for academic papers and generate standard BibTeX citations

[中文版本](README_zh.md) | Read this in Chinese

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
├── main.py                 # FastAPI main application
├── search.py               # Semantic Scholar API implementation
├── academic_keywords.json  # Academic keywords database
├── config/                 # Configuration directory
│   ├── api_keys.txt        # API key configuration
│   ├── api_keys.txt.example# API key configuration example
│   ├── proxies.txt         # Proxy configuration
│   ├── proxies.txt.example # Proxy configuration example
│   └── last_used.json      # API key usage records
├── API_USAGE_GUIDE.md      # Detailed API usage guide
├── ADVANCED_CONFIG.md      # Advanced configuration guide
├── CLAUDE.md               # Claude Code tool configuration
├── SOLUTIONS.md            # Solution descriptions
├── README.md               # Project documentation (English)
├── README_zh.md            # Project documentation (Chinese)
├── requirements.txt        # Dependencies list
├── start.sh                # Quick startup script
├── .claude/                # Claude IDE integration config
└── docs/                   # Documentation directory
    └── superpowers/        # Technical documentation
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

This project includes a custom Claude skill to help you use the API more effectively:

### Skill: Paper Search with Citation

- **Location**: `paper_search_with_citation/SKILL.md`
- **Purpose**: Guide users through calling the deployed academic search API using bash commands

### How to Use the Skill

This skill provides built-in guidance for common tasks. In Claude Code, you can activate it for quick access to:
- API endpoint examples
- curl command templates for searching papers
- Parameter documentation
- Examples of getting BibTeX citations
- Best practices for usage

It works alongside the documentation to help you get started quickly and make the most of the API.

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
