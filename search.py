"""
Semantic Scholar Academic Paper Search and BibTeX Citation Generation Tool
Features: Search papers → Get complete bibliographic information → Generate standard BibTeX citations
Fully free, API Key support for faster access
"""

import requests
import time
import re
import json
import os
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class ApiConfig:
    """API configuration with API key and corresponding proxy"""
    api_key: Optional[str]
    proxy: Optional[str]
    index: int
    last_used: float = 0.0
    rate_limited: bool = False
    healthy: bool = True


class ApiKeyManager:
    """Manager for handling multiple API keys and proxies"""

    def __init__(self, api_keys: List[str], proxies: List[Optional[str]], last_used_file: str = "config/last_used.json"):
        """
        Initialize API key manager

        Args:
            api_keys: List of API keys
            proxies: List of proxies (should match length of api_keys)
        """
        self.configs: List[ApiConfig] = []

        if not api_keys:
            raise ValueError("At least one API key must be provided")

        # Ensure proxies list matches API keys list
        if len(proxies) < len(api_keys):
            # Add null proxies for any missing
            proxies.extend([None] * (len(api_keys) - len(proxies)))
        else:
            proxies = proxies[:len(api_keys)]

        self.last_used_file = last_used_file

        for i, (api_key, proxy) in enumerate(zip(api_keys, proxies)):
            self.configs.append(ApiConfig(
                api_key=api_key,
                proxy=proxy,
                index=i
            ))

        # Load saved last_used times
        self._load_last_used_times()

        self._current_index: int = 0
        self._lock: bool = False

    def _load_last_used_times(self):
        """Load saved last_used times from file"""
        try:
            if os.path.exists(self.last_used_file):
                with open(self.last_used_file, "r", encoding="utf-8") as f:
                    last_used_data = json.load(f)
                loaded_count = 0
                for config in self.configs:
                    if config.api_key in last_used_data:
                        config.last_used = last_used_data[config.api_key]
                        loaded_count += 1
                print(f"✅ Loaded last used times for {loaded_count} API keys")
        except Exception as e:
            print(f"⚠️  Error loading last used times: {e}")

    def _save_last_used_times(self):
        """Save last_used times to file"""
        try:
            # Ensure config directory exists
            config_dir = os.path.dirname(self.last_used_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)

            last_used_data = {
                config.api_key: config.last_used
                for config in self.configs
            }

            with open(self.last_used_file, "w", encoding="utf-8") as f:
                json.dump(last_used_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving last used times: {e}")

    def get_next_config(self) -> ApiConfig:
        """Get the next available API configuration (with rotation)"""
        if len(self.configs) == 1:
            config = self.configs[0]
            config.last_used = time.time()
            self._save_last_used_times()
            return config

        # Find next available config
        start_index = self._current_index
        while True:
            self._current_index = (self._current_index + 1) % len(self.configs)
            config = self.configs[self._current_index]

            # Check if config is available
            if config.healthy and not config.rate_limited:
                config.last_used = time.time()
                self._save_last_used_times()
                return config

            # If we've checked all configs
            if self._current_index == start_index:
                # If all are rate limited, pick the first one and wait
                if all(config.rate_limited for config in self.configs):
                    print("⚠️  All API keys are rate limited, waiting to reset...")
                    time.sleep(1)
                    self._reset_rate_limits()
                    return self.get_next_config()

                # If all are unhealthy, pick the first one
                config.last_used = time.time()
                self._save_last_used_times()
                return config

    def mark_rate_limited(self, config: ApiConfig):
        """Mark a configuration as rate limited"""
        config.rate_limited = True
        config.last_used = time.time()
        self._save_last_used_times()

    def mark_unhealthy(self, config: ApiConfig):
        """Mark a configuration as unhealthy"""
        config.healthy = False
        config.last_used = time.time()
        self._save_last_used_times()

    def mark_healthy(self, config: ApiConfig):
        """Mark a configuration as healthy"""
        config.healthy = True
        config.rate_limited = False

    def _reset_rate_limits(self):
        """Reset rate limits for all configurations after cooldown"""
        for config in self.configs:
            if config.rate_limited and (time.time() - config.last_used > 1):
                config.rate_limited = False

    def get_stats(self) -> Dict:
        """Get manager statistics"""
        return {
            "total_configs": len(self.configs),
            "healthy_configs": sum(1 for c in self.configs if c.healthy),
            "rate_limited_configs": sum(1 for c in self.configs if c.rate_limited),
            "proxied_configs": sum(1 for c in self.configs if c.proxy),
            "current_index": self._current_index
        }


class AcademicCitationTool:
    """
    Tool for searching academic papers and generating BibTeX citations
    using Semantic Scholar API with support for multiple API keys and proxies.
    """

    def __init__(self, sem_api_key: Optional[str] = None, config_dir: str = "config"):
        """
        Initialize the academic citation tool

        Args:
            sem_api_key: Single API key (backward compatibility)
            config_dir: Directory containing configuration files
        """
        self.sem_url = "https://api.semanticscholar.org/graph/v1"
        self.crossref_headers = {"User-Agent": "AgentBot/1.0 (mailto:test@example.com)"}
        self.session = requests.Session()
        self.default_timeout = 10
        self.max_authors = 10

        # Load API keys and proxies
        self._load_config(sem_api_key, config_dir)

    def _parse_proxy(self, proxy_str: str) -> Optional[str]:
        """Parse various proxy formats to standard http:// format"""
        proxy_str = proxy_str.strip()

        # Handle null or empty
        if proxy_str.lower() == "null" or proxy_str == "":
            return None

        # If already has protocol (http:// or https://), use as is
        if proxy_str.startswith("http://") or proxy_str.startswith("https://"):
            return proxy_str

        # Format: host:port:username:password
        if proxy_str.count(":") == 3:
            host, port, username, password = proxy_str.split(":", 3)
            return f"http://{username}:{password}@{host}:{port}"

        # Format: host:port
        if proxy_str.count(":") == 1:
            return f"http://{proxy_str}"

        # Otherwise, assume invalid or return as is
        return proxy_str

    def _load_config(self, single_api_key: Optional[str], config_dir: str):
        """Load API keys and proxies from configuration files"""
        # Configuration file paths
        api_keys_file = os.path.join(config_dir, "api_keys.txt")
        proxies_file = os.path.join(config_dir, "proxies.txt")
        last_used_file = os.path.join(config_dir, "last_used.json")

        api_keys: List[str] = []
        proxies: List[Optional[str]] = []

        # Try to load from config files first
        if os.path.exists(api_keys_file):
            try:
                with open(api_keys_file, "r", encoding="utf-8") as f:
                    for line in f:
                        key = line.strip()
                        if key:
                            api_keys.append(key)
            except Exception as e:
                print(f"⚠️  Error loading API keys: {e}")

        if os.path.exists(proxies_file):
            try:
                with open(proxies_file, "r", encoding="utf-8") as f:
                    for line in f:
                        proxy = line.strip()
                        if proxy:
                            # Parse proxy format: host:port:username:password, or null
                            parsed_proxy = self._parse_proxy(proxy)
                            proxies.append(parsed_proxy)
                        else:
                            # Empty line means no proxy
                            proxies.append(None)
            except Exception as e:
                print(f"⚠️  Error loading proxies: {e}")

        # Fallback to single API key parameter (backward compatibility)
        if single_api_key and not api_keys:
            api_keys = [single_api_key]

        # Fallback to environment variables
        if not api_keys:
            api_keys = os.getenv("SEMANTIC_SCHOLAR_API_KEYS",
                              os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")).split(",")
            api_keys = [key.strip() for key in api_keys if key.strip()]

        if not proxies:
            proxy_env = os.getenv("SEMANTIC_SCHOLAR_PROXIES", "")
            proxies = [proxy.strip() if proxy and proxy.lower() != "null" else None
                      for proxy in proxy_env.split(",")]

        # Validate configuration
        if not api_keys:
            raise ValueError("No API keys configured. Please provide at least one API key.")

        self.manager = ApiKeyManager(api_keys, proxies, last_used_file)
        print(f"✅ Loaded {len(api_keys)} API keys, {sum(1 for p in proxies if p)} proxied configurations")

    def search_and_get_citations(self, query: str, limit: int = 3,
                                  include_bibtex: bool = True) -> Dict:
        """
        Search papers and get citation information (main interface)

        Args:
            query (str): Search keywords
            limit (int): Number of results to return, default: 3
            include_bibtex (bool): Whether to include BibTeX citations, default: True

        Returns:
            Dict: Search results in dictionary format
        """
        print(f"🔍 Searching: {query}...")

        # 1. Search using Semantic Scholar (get complete information)
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,venue,url,externalIds,abstract,citationCount,"
                      "fieldsOfStudy,isOpenAccess,openAccessPdf,journal,publicationTypes"
        }

        # Try to get results with retries
        max_retries = len(self.manager.configs) * 2
        for attempt in range(max_retries):
            config = self.manager.get_next_config()

            # Create headers
            headers = {}
            if config.api_key:
                headers["x-api-key"] = config.api_key

            # Create proxies
            proxies = None
            if config.proxy:
                proxies = {
                    "http": config.proxy,
                    "https": config.proxy
                }

            print(f"📡 Attempt {attempt + 1}: Using API key {config.index} {'(with proxy)' if config.proxy else '(direct)'}")

            try:
                sem_res = self.session.get(
                    f"{self.sem_url}/paper/search",
                    headers=headers,
                    params=params,
                    timeout=self.default_timeout,
                    proxies=proxies
                )

                if sem_res.status_code == 429:  # Rate limited
                    print(f"⚠️  API key {config.index} rate limited")
                    self.manager.mark_rate_limited(config)
                    time.sleep(1)
                    continue

                sem_res.raise_for_status()
                sem_data = sem_res.json().get("data", [])

                # Mark configuration as healthy
                self.manager.mark_healthy(config)

                if not sem_data:
                    return {"success": False, "query": query, "total_results": 0, "papers": [],
                           "message": "No relevant papers found."}

                # Process results
                papers_list = []
                for i, paper in enumerate(sem_data, 1):
                    paper_dict = self._process_paper(paper, include_bibtex)
                    papers_list.append(paper_dict)

                return {
                    "success": True,
                    "query": query,
                    "total_results": len(papers_list),
                    "papers": papers_list,
                    "api_key_used": config.index
                }

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"⚠️  API key {config.index} rate limited")
                    self.manager.mark_rate_limited(config)
                    time.sleep(1)
                else:
                    print(f"⚠️  API key {config.index} failed: HTTP {e.response.status_code}")
                    self.manager.mark_unhealthy(config)

            except requests.exceptions.ConnectionError as e:
                print(f"⚠️  Connection error with proxy {config.proxy}: {e}")
                self.manager.mark_unhealthy(config)

            except requests.exceptions.Timeout as e:
                print(f"⚠️  Timeout with proxy {config.proxy}: {e}")
                self.manager.mark_unhealthy(config)

            except Exception as e:
                print(f"⚠️  API key {config.index} failed: {e}")
                self.manager.mark_unhealthy(config)

            # Delay before next attempt
            time.sleep(0.5)

        return {"success": False, "query": query, "total_results": 0, "papers": [],
               "message": f"All {len(self.manager.configs)} API keys failed. Please check your configuration."}

    def _process_paper(self, paper: Dict, include_bibtex: bool) -> Dict:
        """Process a single paper result"""
        # Format authors
        authors = paper.get("authors", [])
        author_names = [a["name"] for a in authors[:self.max_authors]]
        if len(authors) > self.max_authors:
            author_names.append("et al.")
        authors_str = ", ".join(author_names)

        # Get field information with proper defaults
        doi = paper.get('externalIds', {}).get('DOI')
        title = paper.get('title', 'No Title')
        year = paper.get('year', None)
        venue = paper.get('venue', 'Unknown Venue')
        abstract = paper.get('abstract', 'No Abstract') or 'No Abstract'
        citation_count = paper.get('citationCount', 0)
        is_open_access = paper.get('isOpenAccess', False)
        fields_of_study = paper.get('fieldsOfStudy', []) or []

        # Get BibTeX
        bibtex_text = self._get_bibtex(paper, doi, include_bibtex)

        # Build paper dictionary
        paper_dict = {
            "index": paper.get('paperId'),
            "title": title,
            "authors": authors_str,
            "year": year,
            "venue": venue,
            "doi": doi,
            "citation_count": citation_count,
            "is_open_access": is_open_access,
            "fields_of_study": fields_of_study,
            "abstract": abstract,
            "url": paper.get('url', ''),
            "bibtex": bibtex_text if include_bibtex else None
        }

        return paper_dict

    def _get_bibtex(self, paper: Dict, doi: Optional[str], include_bibtex: bool) -> str:
        """Get BibTeX, with fallback mechanism for papers without DOI"""
        if not include_bibtex:
            return ""

        bibtex_text = "Unable to generate BibTeX"

        if doi:
            bibtex_text = self._fetch_crossref_bibtex(doi)

        if not bibtex_text or bibtex_text in ["Unable to generate BibTeX", "Failed to get BibTeX", "BibTeX timeout"]:
            bibtex_text = self._generate_fallback_bibtex(paper)

        return bibtex_text

    def _fetch_crossref_bibtex(self, doi: str) -> str:
        """Fetch BibTeX using CrossRef API"""
        url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
        try:
            res = self.session.get(
                url,
                headers=self.crossref_headers,
                timeout=self.default_timeout
            )
            if res.status_code == 200:
                return res.text
        except requests.exceptions.Timeout:
            return "BibTeX timeout"
        except Exception:
            pass
        return "Failed to get BibTeX"

    def _generate_fallback_bibtex(self, paper: Dict) -> str:
        """Generate fallback BibTeX for papers without DOI"""
        title = paper.get('title', 'No Title').replace("{", "\\{").replace("}", "\\}")
        year = paper.get('year', 'noyear')
        venue = paper.get('venue', 'Unknown Venue').replace("{", "\\{").replace("}", "\\}")

        # Generate citation key
        authors = paper.get('authors', [])
        if authors:
            first_author = authors[0]['name'].split()[-1]
            cite_key = f"{first_author}{year}{title[:20].replace(' ', '')}"
        else:
            cite_key = f"paper{year}{title[:20].replace(' ', '')}"

        cite_key = re.sub(r'[^a-zA-Z0-9]', '', cite_key)[:50]

        # Format authors
        author_list = []
        for author in authors[:self.max_authors]:
            name = author['name'].replace("{", "\\{").replace("}", "\\}")
            author_list.append(name)
        authors_str = " and ".join(author_list)
        if len(authors) > self.max_authors:
            authors_str += " and others"

        entry_type = "article" if "JournalArticle" in paper.get('publicationTypes', []) else "misc"

        bibtex = f"""@{entry_type}{{{cite_key},
  title = {{{title}}},
  author = {{{authors_str}}},
  year = {{{year}}},
  journal = {{{venue}}},
  url = {{{paper.get('url', '')}}},
  note = {{Retrieved from Semantic Scholar}}
}}"""
        return bibtex

    def get_single_paper_bibtex(self, doi: str) -> str:
        """Get BibTeX for a single paper directly using DOI"""
        bibtex = self._fetch_crossref_bibtex(doi)
        if bibtex and bibtex not in ["Failed to get BibTeX", "BibTeX timeout"]:
            return f"```bibtex\n{bibtex}\n```"
        else:
            return "❌ Failed to get BibTeX from DOI, please check if the DOI is correct."

    def get_manager_stats(self) -> Dict:
        """Get API manager statistics"""
        return self.manager.get_stats()

    def _load_keywords(self, keywords_file: str = "academic_keywords.json") -> List[str]:
        """Load academic keywords from JSON file"""
        try:
            if os.path.exists(keywords_file):
                with open(keywords_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading keywords: {e}")
        # Fallback keywords if file not found
        return ["machine learning", "deep learning", "artificial intelligence"]

    def _search_with_specific_config(self, config: ApiConfig, query: str, limit: int = 1) -> bool:
        """
        Perform a search using a specific API configuration.
        Returns True if successful, False otherwise.
        """
        params = {
            "query": query,
            "limit": limit,
            "fields": "paperId"
        }

        headers = {}
        if config.api_key:
            headers["x-api-key"] = config.api_key

        proxies = None
        if config.proxy:
            proxies = {
                "http": config.proxy,
                "https": config.proxy
            }

        try:
            sem_res = self.session.get(
                f"{self.sem_url}/paper/search",
                headers=headers,
                params=params,
                timeout=self.default_timeout,
                proxies=proxies
            )

            if sem_res.status_code == 429:
                self.manager.mark_rate_limited(config)
                return False

            sem_res.raise_for_status()
            self.manager.mark_healthy(config)
            config.last_used = time.time()
            self.manager._save_last_used_times()
            return True

        except Exception as e:
            print(f"⚠️  Keep-alive search failed for API key {config.index}: {e}")
            self.manager.mark_unhealthy(config)
            return False

    def check_idle_api_keys(self, idle_threshold_seconds: float = 86400) -> List[int]:
        """
        Check for API keys that haven't been used in the specified threshold.

        Args:
            idle_threshold_seconds: Idle threshold in seconds (default: 86400 = 1 day)

        Returns:
            List of config indices that are idle
        """
        current_time = time.time()
        idle_configs = []

        for config in self.manager.configs:
            # If last_used is 0 (never used) or exceeds threshold
            if config.last_used == 0 or (current_time - config.last_used > idle_threshold_seconds):
                idle_configs.append(config.index)

        return idle_configs

    def ping_idle_api_keys(self, idle_threshold_seconds: float = 86400) -> Dict[str, Any]:
        """
        Check for idle API keys and perform a search to keep them active.

        Args:
            idle_threshold_seconds: Idle threshold in seconds (default: 86400 = 1 day)

        Returns:
            Dictionary with results of the ping operation
        """
        import random

        idle_indices = self.check_idle_api_keys(idle_threshold_seconds)

        if not idle_indices:
            return {
                "success": True,
                "message": "No idle API keys found",
                "idle_count": 0,
                "poked_count": 0,
                "failed_count": 0
            }

        keywords = self._load_keywords()
        poked = []
        failed = []

        for config_idx in idle_indices:
            config = self.manager.configs[config_idx]
            query = random.choice(keywords)

            print(f"🔄 Pinging idle API key {config.index} with query: '{query}'")

            if self._search_with_specific_config(config, query):
                poked.append(config_idx)
                print(f"✅ Successfully pinged API key {config.index}")
            else:
                failed.append(config_idx)
                print(f"❌ Failed to ping API key {config.index}")

        return {
            "success": True,
            "message": f"Pinged {len(poked)} idle API keys",
            "idle_count": len(idle_indices),
            "poked_count": len(poked),
            "failed_count": len(failed),
            "poked_indices": poked,
            "failed_indices": failed
        }


# ==================== Usage Examples ====================

if __name__ == "__main__":
    try:
        tool = AcademicCitationTool()

        print("=" * 60)
        print("API Manager Statistics:", tool.get_manager_stats())
        print("=" * 60)

        # Test search
        result = tool.search_and_get_citations("attention", limit=2, include_bibtex=True)
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Error: {e}")
