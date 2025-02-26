from flask import Flask, render_template, request, jsonify
import os
from processor import TranscriptProcessor
import json

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Default instructions from the original processor
# Updated podcast analysis instructions
DEFAULT_INSTRUCTIONS = """
Analyze this podcast transcript and provide the following in JSON format:

ESSENTIAL:
1. podcastInfo: Take the transcript and give me the name, description (no longer than 300 characters), instructions, and conversation starters. Make sure the name follows this format Crazy Wisdom Companion: [Guest Name] and make sure the conversation starters are short and sweet and include the guests name inside of them so that the responses are based in the transcript not on your knowledge.

2. timeStamps: Give me time stamps for this episode every five minutes from the beginning to the end without worrying about the intro or outro. Make sure to include what was discussed at each part of the episode. Do it without brackets and only create a 00:00:00 if there is more than 60 minutes of content otherwise keep it like 00:00.

3. topicIntro: Give me an intro to the topics discussed mentioning my name Stewart Alsop and the guest's full name. Also add any links to the show notes that were mentioned for the guest. Make it only one paragraph and avoid using the word delve or sounding like chatgpt.

4. potentialTitles: Can you give me 10 possible titles for this episode, make them creative and analyze my part of the conversation (Stewart Alsop III) to get a sense for my voice.

5. keywords: Give me the keywords from the episode in a list in sentence form with commas in between each keyword.

6. keyInsights: Can you give me 7 key insights from this episode in a numbered list in full paragraph form.

7. episodeBlurb: Give me a blurb about this episode, 2-3 sentences as if I were talking about it, frame it as if you were me and you were sharing the podcast episode as a guest.

8. conversationGaps: Can you search the transcripts for any gaps in the conversation due to technical issues or when a guest or myself says something they didn't mean to say and stops the recording?

9. contactDetails: Can you find if the guest shared any contact details at the end of the conversation?

Structure all of this in a clear JSON format with all fields as required parts of the analysis.
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
    app.run(debug=True, port=5001)
