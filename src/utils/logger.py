"""Logging utility for the research assistant."""
import logging


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.
    
    Args:
        name: Name for the logger
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Set up console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Set default level
        logger.setLevel(logging.INFO)
    
    return logger
