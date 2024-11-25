"""TextbookAgent for reading and explaining textbook content."""
import os
import warnings
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import PyPDF2
from rich.progress import Progress, SpinnerColumn, TextColumn
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from src.utils.logger import get_logger

# Filter out LangChain deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='langchain.*')

logger = get_logger(__name__)

class TextbookAgent:
    """Agent for processing and explaining textbook content."""
    
    def __init__(self, storage_dir: str = "textbook_knowledge"):
        """Initialize the TextbookAgent.
        
        Args:
            storage_dir: Directory to store vector embeddings
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            persist_directory=str(self.storage_dir / "vectors"),
            embedding_function=self.embeddings
        )
        
        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Track loaded books
        self.books_file = self.storage_dir / "books.txt"
        self.loaded_books = self._load_book_list()
        
    def _load_book_list(self) -> List[str]:
        """Load list of previously processed books."""
        if self.books_file.exists():
            return self.books_file.read_text().splitlines()
        return []
        
    def _save_book_list(self):
        """Save list of processed books."""
        self.books_file.write_text("\n".join(self.loaded_books))
        
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
        
    def load_book(self, file_path: str, with_progress: bool = True) -> bool:
        """Load and process a textbook.
        
        Args:
            file_path: Path to PDF or text file
            with_progress: Show progress bar
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = str(Path(file_path).resolve())
            
            # Check if already loaded
            if file_path in self.loaded_books:
                logger.info(f"Book already loaded: {file_path}")
                return True
                
            # Extract text based on file type
            if file_path.lower().endswith('.pdf'):
                text = self._extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Add progress bar if requested
            if with_progress:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description="Processing book...", total=None)
                    # Add chunks to vector store with metadata
                    self.vector_store.add_texts(
                        texts=chunks,
                        metadatas=[{"source": file_path, "chunk": i} for i in range(len(chunks))]
                    )
            else:
                # Add chunks without progress bar
                self.vector_store.add_texts(
                    texts=chunks,
                    metadatas=[{"source": file_path, "chunk": i} for i in range(len(chunks))]
                )
                
            # Update loaded books list
            self.loaded_books.append(file_path)
            self._save_book_list()
            
            logger.info(f"Successfully loaded book: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading book {file_path}: {str(e)}")
            return False
            
    def explain_topic(self, topic: str, detail_level: str = "phd") -> str:
        """Explain a topic using loaded textbook knowledge.
        
        Args:
            topic: Topic to explain
            detail_level: Level of detail (phd, master, undergraduate)
            
        Returns:
            Detailed explanation of the topic
        """
        try:
            # Get relevant chunks from vector store
            results = self.vector_store.similarity_search_with_relevance_scores(
                topic,
                k=5  # Get top 5 most relevant chunks
            )
            
            if not results:
                return "I don't have enough information about this topic in my knowledge base."
                
            # Prepare context from relevant chunks
            context = "\n\n".join([chunk.page_content for chunk, score in results if score > 0.5])
            
            # Create prompt based on detail level
            detail_prompts = {
                "phd": "Explain this topic as if teaching a PhD student, including theoretical foundations, current research, and advanced concepts:",
                "master": "Explain this topic as if teaching a master's student, balancing theory and practical applications:",
                "undergraduate": "Explain this topic as if teaching an undergraduate student, focusing on fundamental concepts:"
            }
            
            prompt = f"""{detail_prompts.get(detail_level, detail_prompts['phd'])}

Topic: {topic}

Relevant Information:
{context}

Please provide a comprehensive explanation that includes:
1. Theoretical background and foundations
2. Key concepts and principles
3. Advanced applications and implications
4. Current research directions (if applicable)
5. Related topics and connections"""
            
            # Get response from Ollama
            response = ""
            for line in self._get_llm_response(prompt):
                words = line.split()
                for word in words:
                    print(word, end=' ', flush=True)  # Print each word with a space
                response += line + "\n"
            return response
            
        except Exception as e:
            logger.error(f"Error explaining topic: {str(e)}")
            return f"Error explaining topic: {str(e)}"
            
    def _get_llm_response(self, prompt: str):
        """Get response from Ollama LLM with streaming.
        
        Args:
            prompt: Input prompt
        
        Yields:
            Incremental parts of LLM response
        """
        try:
            import requests
            import json
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:3b",
                    "prompt": prompt,
                    "stream": True,  # Enable streaming
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2048
                    }
                },
                stream=True  # Enable streaming in the request
            )
            response.raise_for_status()
            
            # Stream response data
            for line in response.iter_lines():
                if line:
                    # Parse JSON and extract the response field
                    data = json.loads(line)
                    yield data.get('response', '')
                    
        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            yield f"Error: {str(e)}"
            
    def get_loaded_books(self) -> List[str]:
        """Get list of loaded books.
        
        Returns:
            List of book file paths
        """
        return self.loaded_books.copy()
        
    def clear_knowledge(self):
        """Clear all stored knowledge."""
        try:
            # Clear vector store
            self.vector_store = Chroma(
                persist_directory=str(self.storage_dir / "vectors"),
                embedding_function=self.embeddings
            )
            # Clear book list
            self.loaded_books = []
            self._save_book_list()
            logger.info("Knowledge base cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing knowledge base: {str(e)}")
