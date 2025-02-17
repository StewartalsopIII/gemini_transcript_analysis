import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re

class TranscriptProcessor:
    def __init__(self):
        """Initialize the Gemini 2.0 Flash client with API key from .env"""
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
            
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize Gemini 2.0 Flash model
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Set default generation config for consistent outputs
        self.generation_config = {
            "temperature": float(os.getenv("TEMPERATURE", 0.3)),
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": int(os.getenv("MAX_OUTPUT_TOKENS", 2048)),
        }

    def clean_response(self, text: str) -> str:
        """Remove markdown code blocks and clean the response for JSON parsing."""
        # Remove markdown code blocks
        text = re.sub(r'```json\n', '', text)
        text = re.sub(r'\n```', '', text)
        return text.strip()

    def process_transcript(self, transcript: str, instructions: str) -> dict:
        """Process entire transcript in one shot using Gemini 2.0 Flash's large context window.
        
        Args:
            transcript (str): The complete transcript text
            instructions (str): Specific processing instructions
            
        Returns:
            dict: Processed results in JSON format
        """
        prompt = f"""
        Instructions: {instructions}
        
        Please analyze the following transcript and provide results in JSON format:
        
        {transcript}
        
        Return your complete analysis as a valid JSON object without any markdown formatting.
        """
        
        try:
            # Updated safety settings to use the new format
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=safety_settings
            )
            
            cleaned_response = self.clean_response(response.text)
            return json.loads(cleaned_response)
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "details": "Error occurred during transcript processing"
            }

def main():
    # Initialize processor
    processor = TranscriptProcessor()
    
    # Read transcript from file
    with open('transcript.txt', 'r') as file:
        transcript = file.read()
    
    # Define processing instructions
    instructions = """
    Analyze this transcript and provide:
    1. Overall summary (max 3 paragraphs)
    2. Main topics discussed (as a list)
    3. Key action items or decisions made
    4. Important quotes (up to 5)
    5. Participant sentiment analysis
    
    Structure all of this in a clear JSON format.
    """
    
    # Process transcript
    results = processor.process_transcript(transcript, instructions)
    
    # Save results to JSON file
    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Analysis complete. Results saved to analysis_results.json")

if __name__ == "__main__":
    main()