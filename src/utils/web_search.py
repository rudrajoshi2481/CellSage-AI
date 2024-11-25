"""Web search utilities for the research assistant."""
import time
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import requests

logger = logging.getLogger(__name__)

class PubMedSearcher:
    """PubMed scientific literature search utility."""
    
    def __init__(self, max_results: int = 5, retry_count: int = 3, retry_delay: float = 1.0):
        """Initialize PubMed searcher.
        
        Args:
            max_results: Maximum number of results to return
            retry_count: Number of retries for failed requests
            retry_delay: Initial delay between retries (will use exponential backoff)
        """
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.max_results = max_results
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        
    def search(self, query: str) -> List[Dict]:
        """Search PubMed for scientific articles.
        
        Args:
            query: Search query
            
        Returns:
            List of article metadata dictionaries
        """
        try:
            # Search for article IDs
            search_url = f"{self.base_url}/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": query,
                "retmax": self.max_results,
                "retmode": "json"
            }
            
            response = self._make_request("GET", search_url, params=params)
            data = response.json()
            
            # Get article IDs
            article_ids = data["esearchresult"]["idlist"]
            
            # Fetch details for each article
            articles = []
            for article_id in article_ids:
                try:
                    article = self._fetch_article_details(article_id)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.error(f"Error fetching article details for PMID {article_id}: {str(e)}")
                    continue
                
                # Add delay between requests to avoid rate limiting
                time.sleep(0.5)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error during PubMed search: {str(e)}")
            return []
            
    def _fetch_article_details(self, article_id: str) -> Optional[Dict]:
        """Fetch detailed information for a PubMed article.
        
        Args:
            article_id: PubMed article ID
            
        Returns:
            Article metadata dictionary or None if failed
        """
        fetch_url = f"{self.base_url}/efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": article_id,
            "retmode": "xml"
        }
        
        response = self._make_request("GET", fetch_url, params=params)
        
        try:
            # Parse XML response
            root = ET.fromstring(response.text)
            article = root.find(".//PubmedArticle")
            
            if article is None:
                return None
                
            # Extract article metadata
            title = article.find(".//ArticleTitle")
            abstract = article.find(".//Abstract/AbstractText")
            authors = article.findall(".//Author")
            journal = article.find(".//Journal/Title")
            year = article.find(".//PubDate/Year")
            
            # Format author names
            author_names = []
            for author in authors:
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                if last_name is not None and fore_name is not None:
                    author_names.append(f"{fore_name.text} {last_name.text}")
                
            return {
                "id": article_id,
                "title": title.text if title is not None else "No title available",
                "abstract": abstract.text if abstract is not None else "No abstract available",
                "authors": author_names,
                "journal": journal.text if journal is not None else "Journal not specified",
                "year": year.text if year is not None else "Year not specified",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
            }
            
        except Exception as e:
            logger.error(f"Error parsing article {article_id}: {str(e)}")
            return None
            
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an HTTP request with retry logic.
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
            
        Raises:
            requests.exceptions.RequestException: If all retries fail
        """
        last_error = None
        delay = self.retry_delay
        
        for attempt in range(self.retry_count):
            try:
                response = requests.request(method, url, **kwargs)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", delay))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                    
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                last_error = e
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retry_count}): {str(e)}")
                
                if attempt < self.retry_count - 1:
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                
        raise last_error
        
    def format_results(self, articles: List[Dict]) -> str:
        """Format search results for display.
        
        Args:
            articles: List of article metadata dictionaries
            
        Returns:
            Formatted string of search results
        """
        if not articles:
            return "No articles found."
            
        formatted = []
        for article in articles:
            formatted.append(f"""Title: {article['title']}
Authors: {', '.join(article['authors'])}
Journal: {article['journal']} ({article['year']})
Abstract: {article['abstract']}
URL: {article['url']}
---""")
            
        return "\n\n".join(formatted)
