# AI Research Assistant

A Python-based research assistant that leverages the Ollama LLM to perform iterative research on given topics.

## Features

- Configurable LLM integration with Ollama
- Iterative research capability
- Comprehensive logging
- Full test coverage
- Environment-based configuration

## Requirements

- Python 3.8+
- Ollama server running locally or remotely

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agents-lllm
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following configuration:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2:3b

# Agent Configuration
TEMPERATURE=0.7
MAX_ITERATIONS=3
```

## Usage

```python
from src import ResearchAssistant

# Initialize the research assistant
assistant = ResearchAssistant()

# Research a topic
findings = assistant.research_topic("Artificial Intelligence in Healthcare")

# Process findings
for finding in findings:
    print(f"Finding {finding['iteration']}: {finding['content']}")
```

## Testing

Run the test suite:

```bash
python -m pytest src/tests/
```

For coverage report:

```bash
python -m pytest --cov=src src/tests/
```

## Project Structure

```
agents-lllm/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── research_assistant.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_config.py
│   │   ├── test_logger.py
│   │   └── test_research_assistant.py
│   └── __init__.py
├── .env
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# CellSage-AI
# CellSage-AI
