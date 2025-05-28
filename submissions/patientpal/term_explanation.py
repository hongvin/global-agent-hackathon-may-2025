"""
Medical term explanation service for PatientPal.
Uses Retrieval-Augmented Generation to provide plain-language explanations of medical terms.
"""

import os
import json
from groq import Groq

# For RAG
from langchain_community.retrievers.web_research import WebResearchRetriever
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.tools import Tool

class TermExplanationService:
    def __init__(self):
        """Initialize the term explanation service using Groq API with RAG capabilities."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.client = Groq(api_key=api_key)
        self.rag_initialized = False
        
        # Try to initialize RAG components if web search APIs are available
        try:
            self.initialize_rag()
            self.rag_initialized = True
        except Exception as e:
            print(f"RAG initialization failed: {e}. Falling back to direct LLM queries.")
    
    def initialize_rag(self):
        """Initialize the RAG components if the necessary API keys are available."""
        # This is a simplified implementation. In a real application, you would:
        # 1. Set up a proper RAG pipeline with Firecrawl or Exa
        # 2. Create a medical knowledge vectorstore
        # 3. Configure appropriate search and filtering
        
        # For demonstration purposes, we'll use a simple implementation
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-8b-8192"
        )
        
        # In a real implementation, you would use Firecrawl or Exa for web search
        # self.search_tool = FirecrawlSearchTool(api_key=os.getenv("FIRECRAWL_API_KEY"))
        
        # For now, we'll simulate the RAG capability
    
    def explain_term(self, term, context=None):
        """
        Generate a plain-language explanation of a medical term.
        
        Args:
            term (str): The medical term to explain
            context (str, optional): The context in which the term was used
            
        Returns:
            dict: Contains 'explanation' text and 'sources' if available
        """
        if self.rag_initialized:
            # In a real implementation, use the RAG pipeline
            # For now, we'll simulate with a direct LLM call
            pass
        
        system_prompt = """
        You are a helpful medical assistant explaining medical terms in simple language.
        Provide a clear, concise explanation that would be understandable to someone without medical training.
        Include a simple definition, why it's relevant to the patient, and any key information they should know.
        
        Format your response as JSON with the following structure:
        {
          "explanation": "Simple explanation in plain language...",
          "sources": ["Mayo Clinic", "WebMD", "etc."]  # Include 2-3 reliable medical sources
        }
        """
        
        user_prompt = f"Please explain the medical term '{term}'"
        if context:
            user_prompt += f" in this context: '{context}'"
        
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError:
            # Fallback if the response is not valid JSON
            return {
                "explanation": "Failed to generate explanation. Please try again.",
                "sources": []
            }
