# Gemini Transcript Analysis

A Python tool that uses Google's Gemini 2.0 Flash model to analyze transcripts and provide structured insights.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

## Usage

1. Place your transcript in `transcript.txt`
2. Run the analysis: `python processor.py`
3. Find results in `analysis_results.json`