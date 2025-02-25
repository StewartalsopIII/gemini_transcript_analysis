from flask import Flask, render_template, request, jsonify
import os
from processor import TranscriptProcessor
import json

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Default instructions from the original processor
DEFAULT_INSTRUCTIONS = """
Analyze this transcript and provide:
1. Overall summary (max 3 paragraphs)
2. Main topics discussed (as a list)
3. Key action items or decisions made
4. Important quotes (up to 5)
5. Participant sentiment analysis

Structure all of this in a clear JSON format.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_transcript():
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    # Check if file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    try:
        # Read file content
        with open(file_path, 'r') as f:
            transcript = f.read()
        
        # Process transcript
        processor = TranscriptProcessor()
        results = processor.process_transcript(transcript, DEFAULT_INSTRUCTIONS)
        
        # Return results as JSON
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)
