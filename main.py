"""Main script to demonstrate Research Assistant usage."""
from src import ResearchAssistant
from src.utils.logger import get_logger
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme
from rich.prompt import Prompt

# Set up logging
logger = get_logger(__name__)

# Set up rich console with custom theme
theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "prompt": "green bold"
})
console = Console(theme=theme)

def main():
    """Run the research assistant demo."""
    try:
        # Initialize the research assistant
        logger.info("Initializing Research Assistant...")
        assistant = ResearchAssistant()
        
        # Display welcome message
        console.print(Panel(
            "[prompt]Welcome to the AI Research Assistant![/prompt]\n\n"
            "This tool helps you research topics using scientific literature from PubMed.\n"
            "Example topics:\n"
            "• The impact of artificial intelligence on healthcare\n"
            "• Recent advances in quantum computing\n"
            "• Climate change effects on biodiversity",
            title="About",
            border_style="green"
        ))
        
        # Get research topic from user
        topic = Prompt.ask("\n[prompt]Enter your research topic[/prompt]")
        if not topic.strip():
            console.print("[error]Error: No topic provided[/error]")
            return 1
            
        logger.info(f"Researching topic: {topic}")
        console.print(f"\n[info]Researching: {topic}[/info]")
        console.print("[info]This may take a few minutes...[/info]")
        
        # Get findings
        result = assistant.research_topic(topic)
        logger.info("Research completed successfully")
        
        # Display results with rich formatting
        console.print("\n[info]Research Findings:[/info]")
        # Create a panel with markdown content
        md = Markdown(result)
        console.print(Panel(md, title="AI Research Assistant", border_style="cyan"))
        
    except KeyboardInterrupt:
        console.print("\n[warning]Research cancelled by user[/warning]")
        return 1
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
        console.print(f"\n[error]Error during research: {str(e)}[/error]")
        return 1
    
    return 0

if __name__ == "__main__":
    main()
