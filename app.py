from flask import Flask, render_template, request, send_from_directory
import os
from gtts import gTTS
import uuid

app = Flask(__name__)

# Directory to save the audio files
AUDIO_FOLDER = 'static/audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form['text']
    if not text:
        return render_template('index.html', error="Please enter some text.")
    
    # Generate a unique filename for each audio file
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
    
    # Check if there's an existing audio file, and remove it
    existing_audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.mp3')]
    if existing_audio_files:
        # Delete the existing audio file
        old_audio_file = os.path.join(AUDIO_FOLDER, existing_audio_files[0])
        os.remove(old_audio_file)
    
    # Generate the new speech audio
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)

    # Return the audio file to be played in the frontend
    return render_template('index.html', audio_file=audio_filename)

@app.route('/download/<filename>')
def download_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
