from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "separated"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Run Demucs to separate vocals
    subprocess.run(["demucs", file_path])

    output_vocals = f"separated/htdemucs/{file.filename[:-4]}/vocals.wav"
    output_music = f"separated/htdemucs/{file.filename[:-4]}/no_vocals.wav"

    return jsonify({
        "message": "Processing complete",
        "vocals": output_vocals,
        "music": output_music
    })

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
