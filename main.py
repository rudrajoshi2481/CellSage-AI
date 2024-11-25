"""Main script to demonstrate Research Assistant usage."""
from src import ResearchAssistant
from src.utils.logger import get_logger

# Set up logging
logger = get_logger(__name__)

def main():
    """Run the research assistant demo."""
    try:
        # Initialize the research assistant
        logger.info("Initializing Research Assistant...")
        assistant = ResearchAssistant()
        
        # Get research topic from user
        print("\nWelcome to the AI Research Assistant!")
        print("Enter a topic to research (e.g., 'The impact of artificial intelligence on healthcare')")
        topic = input("Research topic: ").strip()
        
        if not topic:
            logger.error("No topic provided")
            return 1
            
        logger.info(f"Researching topic: {topic}")
        
        # Get findings
        result = assistant.research_topic(topic)
        logger.info("Research completed successfully")
        print("\nResearch Findings:")
        print(result)
        
    except KeyboardInterrupt:
        logger.info("Research cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()
