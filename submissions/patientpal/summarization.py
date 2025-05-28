"""
Consultation summarization service for PatientPal.
Summarizes medical consultations and identifies key medical terms.
"""

import os
import json
from groq import Groq

class ConsultationSummaryService:
    def __init__(self):
        """Initialize the consultation summary service using Groq API."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
    
    def summarize(self, transcription):
        """
        Summarize the consultation transcription and identify key medical terms.
        
        Args:
            transcription (str): Transcription text from medical consultation
            
        Returns:
            dict: Contains 'summary' text and 'terms' list of identified medical terms
        """
        system_prompt = """
        You are a medical assistant helping patients understand their doctor consultations.
        Given a transcription of a medical consultation, provide:
        1. A concise summary of the key points in plain language
        2. A list of medical terms that might be confusing for the patient
        
        Format your response as JSON with the following structure:
        {
          "summary": "Clear, concise summary in plain language...",
          "terms": [
            {"term": "medical term 1", "context": "brief context from the consultation"},
            {"term": "medical term 2", "context": "brief context from the consultation"}
          ]
        }
        """
        
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please summarize and identify medical terms in this consultation: {transcription}"}
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
                "summary": "Failed to generate summary. Please try again.",
                "terms": []
            }
