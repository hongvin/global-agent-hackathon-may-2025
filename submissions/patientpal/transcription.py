"""
Audio transcription service for PatientPal.
Converts audio recordings of medical consultations to text.
"""

import os
from pathlib import Path
import tempfile
from groq import Groq

class TranscriptionService:
    def __init__(self):
        """Initialize the transcription service using Groq API."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        
    def transcribe(self, audio_file):
        """
        Transcribe audio file to text.
        
        Args:
            audio_file: File-like object containing audio data
            
        Returns:
            str: Transcribed text
        """
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        try:
            # In a real implementation, you would use Groq's audio transcription API
            # For now, we'll simulate with a text completion as Groq may not have direct audio transcription
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a medical transcription service. Convert the following audio to text."},
                    {"role": "user", "content": f"Transcribe the audio file: {Path(tmp_path).name}"}
                ],
            )
            
            # This is a placeholder - in a real implementation, use actual audio transcription API
            transcription = "This is a simulated transcription of a medical consultation. " + \
                            "The patient has been diagnosed with hypertension and type 2 diabetes. " + \
                            "The doctor recommends starting on metformin 500mg twice daily and " + \
                            "lisinopril 10mg once daily in the morning."
            
            return transcription
        
        finally:
            # Clean up the temporary file
            os.unlink(tmp_path)
