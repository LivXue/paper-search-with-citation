bash# Academic Search API Usage Guide

## API Access Information

- **Base URL**: http://localhost:8111
- **API Documentation**: http://localhost:8111/docs

## Calling the API with curl

### 1. Health Check

```bash
curl http://localhost:8111/health
```

### 2. Search Papers (POST Method)

```bash
curl -X POST "http://localhost:8111/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "attention",
    "limit": 3,
    "include_bibtex": true
  }'
```

### 3. Search Papers (GET Method)

```bash
curl "http://localhost:8111/search?query=attention&limit=3&include_bibtex=true"
```

**Parameter Description:**
- `query`: Search keywords (required)
- `limit`: Number of results to return, range 1-20 (optional, default 3)
- `include_bibtex`: Whether to include BibTeX, true/false (optional, default true)

### 4. Get BibTeX Citation (POST Method)

```bash
curl -X POST "http://localhost:8111/bibtex" \
  -H "Content-Type: application/json" \
  -d '{"doi": "10.48550/arXiv.1706.03762"}'
```

### 5. Get BibTeX Citation (GET Method)

```bash
curl "http://localhost:8111/bibtex/10.48550/arXiv.1706.03762"
```

**Parameter Description:**
- `doi`: DOI of the paper (required)

### 6. View API Manager Statistics

```bash
curl "http://localhost:8111/manager/stats"
```

Return information includes:
- Total configurations
- Healthy configurations
- Rate-limited configurations
- Proxied configurations
- Current index

### 7. Formatted Output (Using jq)

If `jq` is installed, you can use it to format JSON output:

```bash
# Search and format output
curl "http://localhost:8111/search?query=attention&limit=2" | jq .

# Show only paper titles
curl "http://localhost:8111/search?query=attention&limit=3" | jq -r '.papers[].title'

# Get BibTeX and save to file
curl "http://localhost:8111/bibtex/10.48550/arXiv.1706.03762" | jq -r '.bibtex' > paper.bib
```
