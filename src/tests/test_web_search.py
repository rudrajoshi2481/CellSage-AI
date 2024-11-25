"""Tests for the scientific literature search utility."""
import unittest
from unittest.mock import patch, MagicMock
import time
import requests
from src.utils.web_search import PubMedSearcher

class TestPubMedSearcher(unittest.TestCase):
    """Test cases for PubMedSearcher class."""
    
    def setUp(self):
        """Set up test environment."""
        self.searcher = PubMedSearcher(max_results=3, max_retries=2, retry_delay=0.1)
        
    def test_format_results_empty(self):
        """Test formatting empty results."""
        formatted = self.searcher.format_results([])
        self.assertEqual(formatted, "No scientific literature found.")
        
    def test_format_results_success(self):
        """Test formatting search results."""
        results = [
            {
                'title': 'Test Article',
                'abstract': 'Test abstract',
                'journal': 'Test Journal',
                'year': '2023',
                'authors': 'Smith, John; Doe, Jane',
                'pmid': '12345',
                'url': 'https://pubmed.ncbi.nlm.nih.gov/12345/'
            }
        ]
        
        formatted = self.searcher.format_results(results)
        
        self.assertIn('Test Article', formatted)
        self.assertIn('Test abstract', formatted)
        self.assertIn('Test Journal (2023)', formatted)
        self.assertIn('Smith, John; Doe, Jane', formatted)
        self.assertIn('https://pubmed.ncbi.nlm.nih.gov/12345/', formatted)
        
    @patch('requests.get')
    def test_search_success(self, mock_get):
        """Test successful PubMed search."""
        # Mock search response
        mock_search_response = MagicMock()
        mock_search_response.json.return_value = {
            'esearchresult': {
                'idlist': ['12345', '67890']
            }
        }
        
        # Mock article responses
        mock_article1_response = MagicMock()
        mock_article1_response.content = '''<?xml version="1.0"?>
            <!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2019//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd">
            <PubmedArticleSet>
                <PubmedArticle>
                    <MedlineCitation Status="Publisher" Owner="NLM">
                        <Article>
                            <ArticleTitle>Test Article 1</ArticleTitle>
                            <Abstract>
                                <AbstractText>Test abstract 1</AbstractText>
                            </Abstract>
                            <Journal>
                                <Title>Test Journal 1</Title>
                            </Journal>
                            <AuthorList CompleteYN="Y">
                                <Author ValidYN="Y">
                                    <LastName>Smith</LastName>
                                    <ForeName>John</ForeName>
                                </Author>
                            </AuthorList>
                        </Article>
                        <DateCompleted>
                            <Year>2023</Year>
                        </DateCompleted>
                    </MedlineCitation>
                </PubmedArticle>
            </PubmedArticleSet>'''
            
        mock_article2_response = MagicMock()
        mock_article2_response.content = '''<?xml version="1.0"?>
            <!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2019//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd">
            <PubmedArticleSet>
                <PubmedArticle>
                    <MedlineCitation Status="Publisher" Owner="NLM">
                        <Article>
                            <ArticleTitle>Test Article 2</ArticleTitle>
                            <Abstract>
                                <AbstractText>Test abstract 2</AbstractText>
                            </Abstract>
                            <Journal>
                                <Title>Test Journal 2</Title>
                            </Journal>
                            <AuthorList CompleteYN="Y">
                                <Author ValidYN="Y">
                                    <LastName>Doe</LastName>
                                    <ForeName>Jane</ForeName>
                                </Author>
                            </AuthorList>
                        </Article>
                        <DateCompleted>
                            <Year>2023</Year>
                        </DateCompleted>
                    </MedlineCitation>
                </PubmedArticle>
            </PubmedArticleSet>'''
            
        # Setup mock responses
        mock_get.side_effect = [
            mock_search_response,  # First call for search
            mock_article1_response,  # Second call for first article
            mock_article2_response  # Third call for second article
        ]
        
        # Perform search
        results = self.searcher.search("test query")
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Test Article 1')
        self.assertEqual(results[0]['abstract'], 'Test abstract 1')
        self.assertEqual(results[0]['journal'], 'Test Journal 1')
        self.assertEqual(results[0]['authors'], 'Smith, John')
        
        # Verify API calls
        self.assertEqual(mock_get.call_count, 3)
        
    @patch('requests.get')
    @patch('time.sleep')
    def test_search_rate_limit_retry_success(self, mock_sleep, mock_get):
        """Test PubMed search with rate limit and successful retry."""
        # Mock responses
        mock_error_response = MagicMock()
        mock_error_response.raise_for_status.side_effect = requests.exceptions.HTTPError("429 Rate limit exceeded")
        
        mock_success_response = MagicMock()
        mock_success_response.json.return_value = {
            'esearchresult': {
                'idlist': ['12345']
            }
        }
        
        mock_article_response = MagicMock()
        mock_article_response.content = '''<?xml version="1.0"?>
            <!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2019//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd">
            <PubmedArticleSet>
                <PubmedArticle>
                    <MedlineCitation Status="Publisher" Owner="NLM">
                        <Article>
                            <ArticleTitle>Test Article</ArticleTitle>
                            <Abstract>
                                <AbstractText>Test abstract</AbstractText>
                            </Abstract>
                            <Journal>
                                <Title>Test Journal</Title>
                            </Journal>
                            <AuthorList CompleteYN="Y">
                                <Author ValidYN="Y">
                                    <LastName>Smith</LastName>
                                    <ForeName>John</ForeName>
                                </Author>
                            </AuthorList>
                        </Article>
                        <DateCompleted>
                            <Year>2023</Year>
                        </DateCompleted>
                    </MedlineCitation>
                </PubmedArticle>
            </PubmedArticleSet>'''
            
        # Setup mock to fail once then succeed
        mock_get.side_effect = [
            mock_error_response,  # First call fails
            mock_success_response,  # Second call succeeds
            mock_article_response  # Third call for article details
        ]
        
        # Perform search
        results = self.searcher.search("test query")
        
        # Verify retry behavior
        self.assertEqual(mock_get.call_count, 3)
        mock_sleep.assert_called_once()
        
        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Article')
        
    @patch('requests.get')
    @patch('time.sleep')
    def test_search_rate_limit_max_retries(self, mock_sleep, mock_get):
        """Test PubMed search with rate limit exceeding max retries."""
        # Mock error response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("429 Rate limit exceeded")
        mock_get.return_value = mock_response
        
        # Perform search
        results = self.searcher.search("test query")
        
        # Verify retry behavior
        self.assertEqual(mock_get.call_count, self.searcher.max_retries)
        self.assertEqual(mock_sleep.call_count, self.searcher.max_retries - 1)
        
        # Verify fallback results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Search Limited')
        self.assertIn('technical issues', results[0]['abstract'])
        
    @patch('requests.get')
    def test_search_non_rate_limit_error(self, mock_get):
        """Test PubMed search with non-rate-limit error."""
        # Mock error response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server error")
        mock_get.return_value = mock_response
        
        # Perform search
        results = self.searcher.search("test query")
        
        # Verify no retries and fallback results
        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Search Limited')
        
if __name__ == '__main__':
    unittest.main()
