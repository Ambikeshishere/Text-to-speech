from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import cv2
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully', 'file_path': filepath})

@app.route('/edit', methods=['POST'])
def edit_video():
    data = request.json
    filepath = data.get('file_path')
    action = data.get('action')
    text = data.get('text', '')
    start = data.get('start', 0)
    end = data.get('end', 1)

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    cap = cv2.VideoCapture(filepath)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    start_frame = int(start * total_frames)
    end_frame = int(end * total_frames)

    output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'output.avi')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    current_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame >= start_frame and current_frame <= end_frame:
            if action == 'text' and text:
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            elif action == 'grayscale':
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            out.write(frame)

        current_frame += 1

    cap.release()
    out.release()

    return jsonify({'message': 'Video processed successfully', 'output_path': output_path})

@app.route('/download/<filename>')
def download_video(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
