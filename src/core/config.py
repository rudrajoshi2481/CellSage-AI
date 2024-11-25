"""Configuration module for the research assistant."""
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

@dataclass
class OllamaConfig:
    """Configuration for Ollama LLM."""
    base_url: str
    model_name: str

@dataclass
class AgentConfig:
    """Configuration for the research agent."""
    temperature: float
    max_iterations: int

class Config:
    """Main configuration class."""
    def __init__(self):
        self.ollama = OllamaConfig(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model_name=os.getenv("MODEL_NAME", "llama3.2:3b")
        )
        self.agent = AgentConfig(
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_iterations=int(os.getenv("MAX_ITERATIONS", "3"))
        )

    @classmethod
    def get_config(cls) -> 'Config':
        """Get configuration instance."""
        return cls()
