"""AI Research Assistant with PubMed integration."""
import os
import json
import requests
from typing import Dict, List, Optional, Generator, Callable
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from src.utils.logger import get_logger
from src.utils.web_search import PubMedSearcher

logger = get_logger(__name__)

class ResearchDisplay:
    """Handles the CLI display of research progress."""
    
    def __init__(self):
        """Initialize the research display."""
        self.console = Console()
        self.layout = Layout()
        self.current_stage = ""
        self.papers_found = 0
        self.current_iteration = 0
        self.max_iterations = 0
        self.stream_content = []
        
    def create_layout(self) -> Layout:
        """Create the layout for the research display."""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        return self.layout
        
    def update_display(self, stage: str, content: str) -> None:
        """Update the display with new content."""
        self.current_stage = stage
        
        if stage == "PUBMED" and "Found" in content:
            self.papers_found = int(content.split()[1])
        elif stage == "ITERATION":
            self.current_iteration = int(content.split()[2].split('/')[0])
        
        # Keep last 10 content updates
        self.stream_content.append((stage, content))
        if len(self.stream_content) > 10:
            self.stream_content.pop(0)
    
    def generate_status_table(self) -> Table:
        """Generate the status table."""
        table = Table(show_header=False, expand=True)
        table.add_column("Status", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Current Stage", self.current_stage)
        table.add_row("Papers Found", str(self.papers_found) if self.papers_found else "Searching...")
        if self.current_iteration:
            table.add_row("Analysis Iteration", f"{self.current_iteration}/{self.max_iterations-1}")
        
        return table
    
    def generate_stream_panel(self) -> Panel:
        """Generate the stream panel."""
        content = "\n".join([f"[cyan]{stage}:[/cyan] {msg}" for stage, msg in self.stream_content])
        return Panel(content, title="Research Stream", border_style="blue")
    
    def render(self) -> None:
        """Render the current state."""
        self.layout["header"].update(
            Panel("Research Assistant", style="bold blue", border_style="blue")
        )
        
        main_layout = Layout()
        main_layout.split_row(
            Layout(self.generate_status_table(), ratio=1),
            Layout(self.generate_stream_panel(), ratio=2)
        )
        self.layout["main"].update(main_layout)
        
        self.layout["footer"].update(
            Panel(f"Last Update: {datetime.now().strftime('%H:%M:%S')}", border_style="blue")
        )

class ResearchAssistant:
    """AI-powered research assistant with PubMed integration."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:3b", 
                 data_dir: str = "research_data"):
        """Initialize the research assistant.
        
        Args:
            base_url: Base URL for Ollama API
            model: Name of the model to use
            data_dir: Directory to store research data and papers
        """
        self.base_url = base_url
        self.model = model
        self.pubmed_searcher = PubMedSearcher()
        self.data_dir = os.path.abspath(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        self.display = ResearchDisplay()
        
    def research_topic(self, topic: str, max_iterations: int = 3) -> str:
        """Research a topic using PubMed and LLM.
        
        Args:
            topic: Topic to research
            max_iterations: Maximum number of research iterations
            
        Returns:
            Research findings as a string
        """
        logger.info(f"Starting research on topic: {topic}")
        self.display.max_iterations = max_iterations
        
        # Create live display
        layout = self.display.create_layout()
        
        with Live(layout, refresh_per_second=4, screen=True):
            try:
                # Create topic-specific directory
                topic_dir = os.path.join(self.data_dir, self._sanitize_filename(topic))
                os.makedirs(topic_dir, exist_ok=True)
                
                # Create stream log file
                stream_log_path = os.path.join(topic_dir, "research_stream.log")
                
                def log_stream(stage: str, content: str):
                    """Log stream updates to file and display."""
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"[{timestamp}] {stage}: {content}\n"
                    
                    # Write to stream log
                    with open(stream_log_path, 'a', encoding='utf-8') as f:
                        f.write(log_entry)
                    
                    # Update display
                    self.display.update_display(stage, content)
                    self.display.render()
                
                log_stream("START", f"Beginning research on topic: {topic}")
                
                # Search PubMed for relevant scientific literature
                log_stream("PUBMED", "Searching PubMed for relevant papers...")
                search_results = self.pubmed_searcher.search(topic)
                log_stream("PUBMED", f"Found {len(search_results)} relevant papers")
                
                formatted_results = self.pubmed_searcher.format_results(search_results)
                
                # Save PubMed results
                self._save_json(os.path.join(topic_dir, "pubmed_results.json"), search_results)
                self._save_text(os.path.join(topic_dir, "formatted_results.txt"), formatted_results)
                
                # Create initial research prompt
                log_stream("ANALYSIS", "Starting initial analysis...")
                prompt = self._create_research_prompt(topic, formatted_results)
                
                # Get initial findings with streaming
                findings = []
                for chunk in self._get_llm_response_stream(prompt):
                    log_stream("ANALYSIS", chunk)
                current_findings = self._get_llm_response(prompt)
                findings.append(current_findings)
                
                # Save initial findings
                self._save_text(os.path.join(topic_dir, "findings_0.txt"), current_findings)
                
                # Iteratively improve findings
                for i in range(max_iterations - 1):
                    log_stream("ITERATION", f"Starting iteration {i+1}/{max_iterations-1}")
                    
                    # Create follow-up prompt
                    prompt = self._create_followup_prompt(topic, current_findings, formatted_results)
                    
                    # Get additional findings with streaming
                    for chunk in self._get_llm_response_stream(prompt):
                        log_stream("ANALYSIS", chunk)
                    current_findings = self._get_llm_response(prompt)
                    findings.append(current_findings)
                    
                    # Save iteration findings
                    self._save_text(os.path.join(topic_dir, f"findings_{i+1}.txt"), current_findings)
                
                # Combine and format all findings
                log_stream("FINALIZING", "Combining all findings...")
                final_response = self._format_findings(findings)
                
                # Save final response
                self._save_text(os.path.join(topic_dir, "final_findings.txt"), final_response)
                
                # Save research metadata
                metadata = {
                    "topic": topic,
                    "timestamp": str(datetime.now()),
                    "model": self.model,
                    "iterations": max_iterations,
                    "num_papers": len(search_results)
                }
                self._save_json(os.path.join(topic_dir, "metadata.json"), metadata)
                
                log_stream("COMPLETE", "Research completed successfully")
                logger.info("Research completed successfully")
                return final_response
                
            except Exception as e:
                error_msg = f"Error during research: {str(e)}"
                if 'log_stream' in locals():
                    log_stream("ERROR", error_msg)
                logger.error(error_msg)
                return error_msg
            
    def _get_llm_response_stream(self, prompt: str) -> Generator[str, None, None]:
        """Get a streaming response from the LLM.
        
        Args:
            prompt: Prompt for the LLM
            
        Yields:
            Chunks of the LLM response
        """
        try:
            # Prepare the request
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1024
                }
            }
            
            # Make the streaming request
            with requests.post(url, json=data, stream=True) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk_data = json.loads(line)
                            if 'response' in chunk_data:
                                yield chunk_data['response']
                        except json.JSONDecodeError:
                            continue
                    
        except requests.exceptions.RequestException as e:
            error_msg = f"Error getting streaming LLM response: {str(e)}"
            logger.error(error_msg)
            yield error_msg
            
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

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize a string to be used as a filename.
        
        Args:
            filename: String to sanitize
            
        Returns:
            Sanitized filename
        """
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def _save_json(self, filepath: str, data: Dict) -> None:
        """Save data as JSON.
        
        Args:
            filepath: Path to save the file
            data: Data to save
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _save_text(self, filepath: str, text: str) -> None:
        """Save text to a file.
        
        Args:
            filepath: Path to save the file
            text: Text to save
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
