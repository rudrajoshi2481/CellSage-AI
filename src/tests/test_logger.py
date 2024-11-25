"""Tests for the logging utility."""
import logging
import unittest
from unittest.mock import patch

from src.utils.logger import setup_logger

class TestLogger(unittest.TestCase):
    """Test cases for logger setup utility."""
    
    def test_logger_creation(self):
        """Test logger creation with default name."""
        logger = setup_logger()
        self.assertIsInstance(logger, logging.Logger)
        
    def test_logger_custom_name(self):
        """Test logger creation with custom name."""
        custom_name = "test_logger"
        logger = setup_logger(custom_name)
        self.assertEqual(logger.name, custom_name)
        
    def test_logger_handler_setup(self):
        """Test logger handler configuration."""
        logger = setup_logger()
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)
        
    def test_logger_formatter(self):
        """Test logger formatter configuration."""
        logger = setup_logger()
        formatter = logger.handlers[0].formatter
        self.assertIsInstance(formatter, logging.Formatter)
        
    def test_logger_level(self):
        """Test logger level configuration."""
        logger = setup_logger()
        self.assertEqual(logger.level, logging.INFO)
        
    def test_logger_singleton(self):
        """Test logger singleton behavior."""
        logger1 = setup_logger("test")
        logger2 = setup_logger("test")
        self.assertEqual(len(logger2.handlers), 1)  # Should not add duplicate handlers
        
if __name__ == '__main__':
    unittest.main()
