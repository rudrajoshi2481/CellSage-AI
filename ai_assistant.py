#!/usr/bin/env python3
"""Unified AI Assistant combining research and textbook capabilities."""
import argparse
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from src.core.research_assistant import ResearchAssistant
from src.agents.textbook_agent import TextbookAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)
console = Console()

class AIAssistant:
    """Unified AI Assistant combining research and textbook capabilities."""
    
    def __init__(self):
        """Initialize the AI Assistant."""
        self.research_assistant = ResearchAssistant()
        self.textbook_agent = TextbookAgent()
        
    def load_books(self, file_paths: List[str]) -> None:
        """Load books into the textbook agent.
        
        Args:
            file_paths: List of file paths to load
        """
        for file_path in file_paths:
            path = Path(file_path)
            if not path.exists():
                console.print(f"[error]File not found: {file_path}[/error]")
                continue
                
            console.print(f"\n[info]Loading book: {path.name}[/info]")
            if self.textbook_agent.load_book(str(path)):
                console.print(f"[success]Successfully loaded: {path.name}[/success]")
            else:
                console.print(f"[error]Failed to load: {path.name}[/error]")
                
    def research_topic(self, topic: str) -> None:
        """Research a topic using scientific literature.
        
        Args:
            topic: Topic to research
        """
        console.print("\n[info]Researching topic using scientific literature...[/info]")
        findings = self.research_assistant.research_topic(topic)
        
        # Display results
        console.print("\n[info]Research Findings:[/info]")
        console.print(Panel(
            Markdown(findings),
            title="Scientific Literature Research",
            border_style="blue"
        ))
        
    def explain_topic(self, topic: str, detail_level: str = "phd") -> None:
        """Explain a topic using loaded textbook knowledge.
        
        Args:
            topic: Topic to explain
            detail_level: Level of detail (phd, master, undergraduate)
        """
        console.print("\n[info]Generating explanation from textbook knowledge...[/info]")
        explanation = self.textbook_agent.explain_topic(topic, detail_level)
        
        # Display explanation
        console.print(Panel(
            Markdown(explanation),
            title=f"Textbook Explanation ({detail_level} level)",
            border_style="cyan"
        ))
        
    def show_loaded_books(self) -> None:
        """Display list of loaded books."""
        books = self.textbook_agent.get_loaded_books()
        if books:
            table = Table(title="Loaded Books", show_header=True, header_style="bold magenta")
            table.add_column("Book Name", style="dim")
            table.add_column("Full Path", style="dim")
            
            for book in books:
                path = Path(book)
                table.add_row(path.name, str(path))
                
            console.print("\n", table)
        else:
            console.print("[warning]No books loaded yet[/warning]")
            
    def clear_knowledge(self) -> None:
        """Clear textbook knowledge base."""
        if Confirm.ask("[yellow]Are you sure you want to clear all knowledge?[/yellow]"):
            self.textbook_agent.clear_knowledge()
            console.print("[success]Knowledge base cleared[/success]")

def show_help():
    """Display help information."""
    help_text = """
Available Commands:
• [cyan]research[/cyan] <topic> - Research a topic using scientific literature
• [cyan]explain[/cyan] <topic> - Explain a topic using textbook knowledge
• [cyan]load[/cyan] - Load a textbook or PDF
• [cyan]books[/cyan] - Show loaded books
• [cyan]clear[/cyan] - Clear textbook knowledge
• [cyan]help[/cyan] - Show this help message
• [cyan]exit[/cyan] - Exit the assistant

Example Usage:
> research quantum computing
> explain neural networks
> load textbook.pdf
    """
    console.print(Panel(help_text, title="AI Assistant Help", border_style="green"))

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="AI Assistant - Your Research and Learning Companion")
    parser.add_argument("--books", nargs="*", help="Paths to textbooks to load")
    args = parser.parse_args()
    
    # Initialize assistant
    assistant = AIAssistant()
    
    # Load books if provided
    if args.books:
        assistant.load_books(args.books)
    
    # Welcome message
    console.print(Panel(
        "[bold green]Welcome to AI Assistant![/bold green]\n\n"
        "I can help you with:\n"
        "• Researching topics using scientific literature\n"
        "• Understanding textbook content in detail\n"
        "• Learning complex topics at different academic levels\n\n"
        "Type [cyan]help[/cyan] to see available commands!",
        title="AI Research & Learning Assistant",
        border_style="green"
    ))
    
    while True:
        try:
            command = Prompt.ask("\n[bold green]What would you like to do?[/bold green]").lower().strip()
            
            if command == "exit":
                break
                
            elif command == "help":
                show_help()
                
            elif command == "load":
                file_path = Prompt.ask("[cyan]Enter path to book[/cyan]")
                assistant.load_books([file_path])
                
            elif command == "books":
                assistant.show_loaded_books()
                
            elif command == "clear":
                assistant.clear_knowledge()
                
            elif command.startswith("research"):
                # Get topic from command or prompt
                topic = command[9:].strip() if len(command) > 9 else None
                if not topic:
                    topic = Prompt.ask("[cyan]What topic would you like me to research?[/cyan]")
                assistant.research_topic(topic)
                
            elif command.startswith("explain"):
                # Get topic from command or prompt
                topic = command[8:].strip() if len(command) > 8 else None
                if not topic:
                    topic = Prompt.ask("[cyan]What topic would you like me to explain?[/cyan]")
                
                # Get detail level
                detail_level = Prompt.ask(
                    "[cyan]Choose detail level[/cyan]",
                    choices=["phd", "master", "undergraduate"],
                    default="phd"
                )
                
                assistant.explain_topic(topic, detail_level)
                
            else:
                console.print("[warning]Unknown command. Type 'help' to see available commands.[/warning]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            console.print(f"[error]An error occurred: {str(e)}[/error]")

if __name__ == "__main__":
    main()
