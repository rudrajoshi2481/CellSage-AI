# 🤖 AI Research Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/your-username/agents-lllm/issues)

> 📚 A powerful, AI-driven research assistant that leverages Ollama LLM to perform intelligent, iterative research on any topic.

<p align="center">
  <em>Transforming the way we conduct research with AI</em>
</p>

## ✨ Key Features

- 🧠 **Advanced LLM Integration** - Seamless integration with Ollama for state-of-the-art language processing
- 🔄 **Iterative Research** - Conducts multi-step research with progressive refinement
- 📊 **Smart Analysis** - Intelligent processing and synthesis of research findings
- 📝 **Comprehensive Logging** - Detailed tracking of research progress and findings
- ⚡ **High Performance** - Optimized for efficient processing and quick results
- 🛡️ **Full Test Coverage** - Ensuring reliability and stability
- ⚙️ **Flexible Configuration** - Easy customization through environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Ollama server (local or remote)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd agents-lllm
```

2. **Set up virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2:3b

# Agent Configuration
TEMPERATURE=0.7
MAX_ITERATIONS=3
```

## 💻 Usage

```python
from src import ResearchAssistant

# Initialize the research assistant
assistant = ResearchAssistant()

# Start researching
findings = assistant.research_topic("Artificial Intelligence in Healthcare")

# Process findings
for finding in findings:
    print(f"Finding {finding['iteration']}: {finding['content']}")
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run tests
python -m pytest src/tests/

# Generate coverage report
python -m pytest --cov=src src/tests/
```

## 📁 Project Structure

```
agents-lllm/
├── src/
│   ├── core/           # Core functionality
│   ├── utils/          # Utility functions
│   └── tests/          # Test suite
├── research_data/      # Research data storage
├── textbook_knowledge/ # Knowledge base
├── uploaded_books/     # Book storage
├── .env               # Environment configuration
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Ollama team for their amazing LLM
- All contributors who help improve this project
- Open source community for various tools and libraries used

---

<p align="center">
  Made with ❤️ by the AI Research Assistant Team
</p>
