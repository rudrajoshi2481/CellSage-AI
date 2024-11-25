"""Tests for the configuration module."""
import os
from unittest import TestCase, main

from src.core.config import Config, OllamaConfig, AgentConfig

class TestConfig(TestCase):
    """Test cases for Config class."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
    
    def test_ollama_config_default_values(self):
        """Test default values for Ollama configuration."""
        self.assertEqual(self.config.ollama.base_url, "http://localhost:11434")
        self.assertEqual(self.config.ollama.model_name, "llama3.2:3b")
    
    def test_agent_config_default_values(self):
        """Test default values for Agent configuration."""
        self.assertEqual(self.config.agent.temperature, 0.7)
        self.assertEqual(self.config.agent.max_iterations, 3)
    
    def test_custom_env_values(self):
        """Test configuration with custom environment values."""
        # Set custom environment variables
        os.environ["OLLAMA_BASE_URL"] = "http://custom:8080"
        os.environ["MODEL_NAME"] = "custom-model"
        os.environ["TEMPERATURE"] = "0.5"
        os.environ["MAX_ITERATIONS"] = "5"
        
        # Create new config instance
        custom_config = Config()
        
        # Assert custom values
        self.assertEqual(custom_config.ollama.base_url, "http://custom:8080")
        self.assertEqual(custom_config.ollama.model_name, "custom-model")
        self.assertEqual(custom_config.agent.temperature, 0.5)
        self.assertEqual(custom_config.agent.max_iterations, 5)
        
        # Clean up environment
        del os.environ["OLLAMA_BASE_URL"]
        del os.environ["MODEL_NAME"]
        del os.environ["TEMPERATURE"]
        del os.environ["MAX_ITERATIONS"]

if __name__ == '__main__':
    main()
