"""Tests for the Research Assistant module."""
import pytest
from unittest.mock import Mock, patch

from src.core.research_assistant import ResearchAssistant


@pytest.fixture
def mock_pubmed_searcher():
    """Create a mock PubMed searcher."""
    with patch('src.core.research_assistant.PubMedSearcher') as mock:
        searcher = Mock()
        mock.return_value = searcher
        yield searcher


@pytest.fixture
def research_assistant(mock_pubmed_searcher):
    """Create a research assistant instance with mocked dependencies."""
    return ResearchAssistant()


def test_research_topic_success(research_assistant, mock_pubmed_searcher):
    """Test successful research topic execution."""
    # Mock search results
    mock_pubmed_searcher.search.return_value = [
        {
            'id': '12345',
            'title': 'Test Article',
            'abstract': 'Test abstract',
            'authors': ['Author 1', 'Author 2'],
            'journal': 'Test Journal',
            'year': '2023'
        }
    ]
    mock_pubmed_searcher.format_results.return_value = "Formatted results"
    
    # Mock LLM response
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'response': 'Test response'}
        mock_post.return_value.raise_for_status = lambda: None
        
        result = research_assistant.research_topic("test topic")
        
        assert "Research Findings" in result
        assert "Test response" in result
        mock_pubmed_searcher.search.assert_called_once_with("test topic")
        mock_pubmed_searcher.format_results.assert_called_once()
        assert mock_post.call_count == 3  # Initial + 2 follow-ups


def test_research_topic_pubmed_error(research_assistant, mock_pubmed_searcher):
    """Test handling of PubMed search errors."""
    mock_pubmed_searcher.search.side_effect = Exception("PubMed error")
    
    result = research_assistant.research_topic("test topic")
    
    assert "Error during research" in result
    assert "PubMed error" in result
    mock_pubmed_searcher.search.assert_called_once_with("test topic")


def test_research_topic_llm_error(research_assistant, mock_pubmed_searcher):
    """Test handling of LLM errors."""
    mock_pubmed_searcher.search.return_value = [{'title': 'Test'}]
    mock_pubmed_searcher.format_results.return_value = "Formatted results"
    
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("LLM error")
        
        result = research_assistant.research_topic("test topic")
        
        assert "Error during research" in result
        assert "LLM error" in result


def test_format_findings(research_assistant):
    """Test formatting of research findings."""
    findings = ["Finding 1", "Finding 2", "Finding 3"]
    
    result = research_assistant._format_findings(findings)
    
    assert "Research Findings:" in result
    assert "Analysis 1:" in result
    assert "Finding 1" in result
    assert "Analysis 2:" in result
    assert "Finding 2" in result
    assert "Analysis 3:" in result
    assert "Finding 3" in result
