"""AI Research Assistant with PubMed integration."""
import os
import json
import requests
from typing import Dict, List, Optional

from src.utils.logger import get_logger
from src.utils.web_search import PubMedSearcher

logger = get_logger(__name__)

class ResearchAssistant:
    """AI-powered research assistant with PubMed integration."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:3b"):
        """Initialize the research assistant.
        
        Args:
            base_url: Base URL for Ollama API
            model: Name of the model to use
        """
        self.base_url = base_url
        self.model = model
        self.pubmed_searcher = PubMedSearcher()
        
    def research_topic(self, topic: str, max_iterations: int = 3) -> str:
        """Research a topic using PubMed and LLM.
        
        Args:
            topic: Topic to research
            max_iterations: Maximum number of research iterations
            
        Returns:
            Research findings as a string
        """
        logger.info(f"Starting research on topic: {topic}")
        
        try:
            # Search PubMed for relevant scientific literature
            search_results = self.pubmed_searcher.search(topic)
            formatted_results = self.pubmed_searcher.format_results(search_results)
            
            # Create initial research prompt
            prompt = self._create_research_prompt(topic, formatted_results)
            
            # Get initial findings
            findings = []
            current_findings = self._get_llm_response(prompt)
            findings.append(current_findings)
            
            # Iteratively improve findings
            for i in range(max_iterations - 1):
                # Create follow-up prompt
                prompt = self._create_followup_prompt(topic, current_findings, formatted_results)
                
                # Get additional findings
                current_findings = self._get_llm_response(prompt)
                findings.append(current_findings)
                
            # Combine and format all findings
            final_response = self._format_findings(findings)
            logger.info("Research completed successfully")
            return final_response
            
        except Exception as e:
            error_msg = f"Error during research: {str(e)}"
            logger.error(error_msg)
            return error_msg
            
    def _create_research_prompt(self, topic: str, search_results: str) -> str:
        """Create the initial research prompt.
        
        Args:
            topic: Research topic
            search_results: Formatted search results from PubMed
            
        Returns:
            Research prompt for the LLM
        """
        return f"""Please analyze the following scientific literature about {topic}.

{search_results}

Based on these scientific sources, provide a comprehensive analysis that includes:
1. Key findings and conclusions
2. Important methodologies used
3. Any limitations or gaps in the research
4. Potential implications and applications

Please cite specific papers when discussing their findings."""
        
    def _create_followup_prompt(self, topic: str, current_findings: str, search_results: str) -> str:
        """Create a follow-up research prompt.
        
        Args:
            topic: Research topic
            current_findings: Current research findings
            search_results: Formatted search results from PubMed
            
        Returns:
            Follow-up prompt for the LLM
        """
        return f"""Based on the previous analysis and the available scientific literature about {topic}:

Previous Analysis:
{current_findings}

Available Literature:
{search_results}

Please provide additional insights focusing on:
1. Aspects not covered in the previous analysis
2. Alternative interpretations of the findings
3. Connections between different studies
4. Practical applications and future research directions

Continue to cite specific papers when discussing their findings."""
        
    def _get_llm_response(self, prompt: str) -> str:
        """Get a response from the LLM.
        
        Args:
            prompt: Prompt for the LLM
            
        Returns:
            LLM response
        """
        try:
            # Prepare the request
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1024
                }
            }
            
            # Make the request
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            return result.get('response', '')
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error getting LLM response: {str(e)}"
            logger.error(error_msg)
            return error_msg
            
    def _format_findings(self, findings: List[str]) -> str:
        """Format the research findings.
        
        Args:
            findings: List of research findings
            
        Returns:
            Formatted research findings
        """
        formatted = "Research Findings:\n\n"
        
        for i, finding in enumerate(findings, 1):
            formatted += f"Analysis {i}:\n"
            formatted += f"{finding}\n\n"
            
        return formatted
