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

This project includes two custom Claude skills to help you use the API more effectively:

### 1. Paper Search with Citation Skill

- **Location**: `paper_search_with_citation/SKILL.md`
- **Purpose**: Guide users through calling the deployed academic search API using bash commands
- **Target Audience**: Users running the API locally or on their own infrastructure

### 2. Using Academic Search API Skill (IDE Integration)

- **Location**: `.claude/skills/paper_search/SKILL.md`
- **Purpose**: Professional integration for Claude Code (claude.ai/code) with IDE support
- **Target Audience**: Developers using Claude Code for research and writing

### Key Skill Features

Both skills provide comprehensive guidance for:
- **API Endpoint Examples**: All available endpoints with detailed examples
- **curl Command Templates**: Copy-paste commands for quick testing
- **Parameter Documentation**: Clear explanations of all search parameters
- **BibTeX Generation**: One-click access to professional citation formats
- **Health Monitoring**: Check API server status
- **Statistics & Analytics**: View API manager performance metrics
- **Formatted Output**: jq integration for clean, readable results

### How to Use the Skills in Claude Code

#### Step 1: Activate the Skill (Claude Code)

1. Open your project in VS Code or the Claude Code IDE
2. Type `/skill` in the Claude Code input
3. Select "Paper Search with Citation" or "Using Academic Search API"
4. The skill will load with all available commands and examples

#### Step 2: Quick Start with Skill Commands

```bash
# Health check (get API status)
curl http://localhost:8111/health

# Search for papers on "attention" with BibTeX (limit 3 results)
curl -X POST "http://localhost:8111/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "attention",
    "limit": 3,
    "include_bibtex": true
  }'

# Get BibTeX for a specific paper by DOI
curl "http://localhost:8111/bibtex/10.48550/arXiv.1706.03762"
```

### Skill Usage Scenarios

#### Scenario 1: Academic Writing

> "I'm writing a paper on transformer architectures and need to find relevant citations."

1. Activate the Paper Search with Citation skill
2. Use the search endpoint with query "transformer architecture"
3. Copy the BibTeX results directly into your LaTeX document
4. Verify citations with DOI-based lookups

#### Scenario 2: Research Exploration

> "I want to explore recent papers on quantum machine learning."

1. Activate the Using Academic Search API skill
2. Search with query "quantum machine learning" and limit=10
3. Parse results with jq to extract paper titles and authors
4. Analyze trends from the formatted output

#### Scenario 3: API Monitoring

> "I need to check if my local API server is running properly."

1. Use the health check command from the skill
2. Monitor API manager statistics to track performance
3. Get real-time information about API key health and proxy status

### Skill Configuration

Both skills are pre-configured for common use cases:

- **Local Development**: Points to http://localhost:8111
- **Remote Deployment**: Can be customized to your server address
- **IDE Integration**: Automatically detects project context
- **Documentation Links**: Direct access to Swagger UI and ReDoc

### Why Use the Claude Skill?

1. **Speed**: Instant access to all API commands without leaving your IDE
2. **Accuracy**: Verified examples that work with your project
3. **Consistency**: Standardized commands across all team members
4. **Productivity**: Copy-paste commands for rapid prototyping
5. **Learning**: Clear explanations for beginners and experts alike

The Claude skills make this academic search tool accessible to researchers, students, and developers of all skill levels.

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
