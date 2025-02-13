This Python Flask application allows users to convert text to speech and download the audio file. The key features and functionalities of this application include:

Home Route (/): Renders the home page (index.html).

Text-to-Speech Conversion Route (/convert):

Accepts a POST request containing text.

Converts the text to speech using the gTTS library.

Generates a unique filename for the audio file.

Removes any existing audio files in the static/audio directory.

Saves the new audio file in the static/audio directory.

Returns the home page with the new audio file available for playback.

Download Audio Route (/download/<filename>):

Provides a way to download the generated audio file.

The application ensures that only one audio file is present at a time by removing previous audio files before saving the new one. The audio files are stored in the static/audio directory, which is created if it doesn't exist.


libraries used

pip install flask

pip install opencv-python-headless

pip install gtts

pip install uuid

After this it will work 
