#!/usr/bin/env python3
"""CLI interface for TextbookAgent."""
import argparse
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from src.agents.textbook_agent import TextbookAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)
console = Console()

def load_books(agent: TextbookAgent, file_paths: List[str]):
    """Load books into the agent.
    
    Args:
        agent: TextbookAgent instance
        file_paths: List of file paths to load
    """
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            console.print(f"[error]File not found: {file_path}[/error]")
            continue
            
        console.print(f"\n[info]Loading book: {path.name}[/info]")
        if agent.load_book(str(path)):
            console.print(f"[success]Successfully loaded: {path.name}[/success]")
        else:
            console.print(f"[error]Failed to load: {path.name}[/error]")

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Textbook Assistant - Your AI Study Companion")
    parser.add_argument("--books", nargs="*", help="Paths to textbooks to load")
    args = parser.parse_args()
    
    # Initialize agent
    agent = TextbookAgent()
    
    # Load books if provided
    if args.books:
        load_books(agent, args.books)
    
    console.print(Panel(
        "[bold green]Welcome to Textbook Assistant![/bold green]\n\n"
        "I can help you understand textbook content in detail. You can:\n"
        "• Load PDF or text files using the [cyan]load[/cyan] command\n"
        "• Ask me to [cyan]explain[/cyan] any topic\n"
        "• View [cyan]loaded[/cyan] books\n"
        "• [cyan]Clear[/cyan] my knowledge base\n"
        "• [cyan]Exit[/cyan] the assistant\n\n"
        "Type your command or question!",
        title="AI Study Companion",
        border_style="green"
    ))
    
    while True:
        try:
            command = Prompt.ask("\n[bold green]What would you like to do?[/bold green]").lower()
            
            if command == "exit":
                break
                
            elif command == "load":
                file_path = Prompt.ask("[cyan]Enter path to book[/cyan]")
                load_books(agent, [file_path])
                
            elif command == "loaded":
                books = agent.get_loaded_books()
                if books:
                    console.print("\n[info]Loaded books:[/info]")
                    for book in books:
                        console.print(f"• {Path(book).name}")
                else:
                    console.print("[warning]No books loaded yet[/warning]")
                    
            elif command == "clear":
                if Confirm.ask("[yellow]Are you sure you want to clear all knowledge?[/yellow]"):
                    agent.clear_knowledge()
                    console.print("[success]Knowledge base cleared[/success]")
                    
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
                
                console.print("\n[info]Generating explanation...[/info]")
                explanation = agent.explain_topic(topic, detail_level)
                
                # Display explanation in a nice panel with markdown formatting
                console.print(Panel(
                    Markdown(explanation),
                    title=f"Explanation: {topic}",
                    border_style="cyan"
                ))
                
            else:
                console.print("[warning]Unknown command. Try: load, explain, loaded, clear, or exit[/warning]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            console.print(f"[error]An error occurred: {str(e)}[/error]")

if __name__ == "__main__":
    main()
