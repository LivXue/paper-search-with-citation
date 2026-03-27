# 学术文献搜索与 BibTeX 生成工具

## FastAPI 部署

本项目已包含完整的 FastAPI API 部署！

### 快速启动

```bash
# 方式 1: 直接运行
python main.py

# 方式 2: 使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8111

# 方式 3: 使用启动脚本
./start.sh
```

### API 文档

- 访问 http://localhost:<your-port>/docs 查看 API 文档 (Swagger UI)
- 访问 http://localhost:<your-port>/redoc 查看 ReDoc 文档
- 详细使用说明请参考 [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md)

### 高级配置

支持多 API Key 和代理配置！详细信息请查看 [ADVANCED_CONFIG.md](ADVANCED_CONFIG.md)

- **API Keys 配置**: `config/api_keys.txt` (每行一个 API Key)
- **代理配置**: `config/proxies.txt` (每行一个代理)

### 配置文件格式

**config/api_keys.txt:**
```txt
your_api_key_here
another_api_key_here
```

**config/proxies.txt:**
```txt
null
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:8080
```

---

## 问题分析

直接访问 Google Scholar 页面（如 `https://scholar.googleusercontent.com/...`）会被拦截或超时，原因包括：

1. **网络限制**：Google 服务在特定地区可能无法直接访问
2. **反爬虫机制**：Google Scholar 有严格的反爬虫措施
3. **IP 封锁**：频繁请求可能导致 IP 被临时封锁

## 解决方案

我们提供了两个可靠的替代方案来获取学术文献的引用信息和 BibTeX 格式数据。

---

## 方案 1：OpenAlex API（推荐）

**文件**：[openalex_search.py](openalex_search.py)

OpenAlex 是一个完全免费、开放的学术文献索引，无需 API 密钥即可使用（只需提供邮箱用于速率限制）。

### 使用方法

```python
from openalex_search import AcademicCitationTool

# 初始化（使用您的邮箱）
tool = AcademicCitationTool(email="your_email@example.com")

# 搜索论文
result = tool.search_and_get_citations("Attention Is All You Need", limit=2)
print(result)

# 通过 DOI 获取 BibTeX
bibtex = tool.get_single_paper_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

### 优势

- ✅ 完全免费且开源
- ✅ 无需 API 密钥
- ✅ 提供完整的元数据（作者、摘要、引用数等）
- ✅ 支持通过 DOI 获取 BibTeX
- ✅ 没有严格的访问限制

---

## 方案 2：Semantic Scholar API

**文件**：[S2_search.py](S2_search.py)

Semantic Scholar 提供高质量的学术文献数据，支持 API 密钥以获得更高的请求配额。

### 使用方法

```python
from S2_search import AcademicCitationTool

# 初始化（使用您的 API 密钥）
tool = AcademicCitationTool(sem_api_key="your_api_key")

# 搜索论文（返回字典格式）
result = tool.search_and_get_citations("Transformer", limit=2, include_bibtex=True)
if result["success"]:
    for paper in result["papers"]:
        print(f"标题: {paper['title']}")
        print(f"BibTeX: {paper['bibtex']}")
else:
    print(f"错误: {result['message']}")

# 通过 DOI 获取 BibTeX
bibtex = tool.get_single_paper_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

### 优势

- ✅ 数据质量高
- ✅ 提供引用关系分析
- ✅ 有免费 API 额度

---

## 运行示例

### OpenAlex 示例

```bash
python3 openalex_search.py
```

### Semantic Scholar 示例

```bash
python3 S2_search.py
```

### 运行测试

```bash
python3 tests/test_S2_search.py
```

---

## 功能特性

### 两个工具都支持

- 🔍 论文搜索（通过关键词）
- 📋 BibTeX 生成
- 📄 通过 DOI 获取引用
- 🔄 降级方案（当无法获取官方 BibTeX 时）
- ⚡ 会话管理和超时处理

### OpenAlex 独有

- 🎯 返回格式化的文本结果（方便直接阅读）
- 🆓 完全免费，无 API 密钥要求

### Semantic Scholar 独有

- 📊 返回结构化的字典数据（便于程序处理）
- 🔑 支持 API 密钥以获得更高配额

---

## 解决方案对比

| 方案 | 推荐度 | 易用性 | 成本 | 稳定性 | 数据格式 |
|------|--------|--------|------|--------|----------|
| OpenAlex | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 免费 | 高 | 文本/字典 |
| Semantic Scholar | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 免费/付费 | 高 | 字典 |
| Google Scholar (直接) | ⭐ | ⭐ | 免费 | 低 | HTML |

---

## 如果确实需要访问 Google Scholar

如果您确实需要从 Google Scholar 获取数据，可以考虑以下方法（但请注意遵守 Google 的服务条款）：

### 使用代理服务器

```python
import requests
from fake_useragent import UserAgent

def fetch_with_proxy(url, proxy_url=None):
    headers = {
        "User-Agent": UserAgent().random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        return response.text if response.status_code == 200 else None
    except Exception as e:
        print(f"Error: {e}")
        return None
```

### 使用 Selenium 或 Playwright（模拟浏览器）

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def fetch_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(3)  # 等待页面加载
        return driver.page_source
    finally:
        driver.quit()
```

---

## 总结

**强烈建议使用 OpenAlex 或 Semantic Scholar 等官方 API，而不是尝试绕过 Google Scholar 的反爬虫机制。** 这些官方 API 提供了更稳定、更高效且更合法的方式来获取学术文献数据。

## 文件结构

```
scholar_engine/
├── openalex_search.py          # OpenAlex API 实现（推荐）
├── S2_search.py                 # Semantic Scholar API 实现
├── SOLUTIONS.md                 # 详细的解决方案说明
├── README.md                    # 本文档
├── tests/
│   └── test_S2_search.py       # S2_search.py 测试文件
└── docs/
    └── superpowers/
        ├── specs/               # 设计规格说明
        └── plans/               # 实现计划
```