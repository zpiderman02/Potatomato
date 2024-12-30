from flask import Flask, request, send_file, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

# Define the download folder
DOWNLOAD_FOLDER = "downloads"

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Get the YouTube video URL and quality from the request
        video_url = request.json.get('video_url')
        quality = request.json.get('quality')

        # Validate input
        if not video_url or not quality:
            return jsonify({"error": "Missing video URL or quality parameter"}), 400

        # Download the video using pytube
        yt = YouTube(video_url)

        # Select stream based on quality
        stream = None
        if quality == '1080p':
            stream = yt.streams.filter(res="1080p", file_extension='mp4').first()
        elif quality == '720p':
            stream = yt.streams.filter(res="720p", file_extension='mp4').first()
        elif quality == '480p':
            stream = yt.streams.filter(res="480p", file_extension='mp4').first()
        elif quality == '4k':
            stream = yt.streams.filter(res="2160p", file_extension='mp4').first()

        if not stream:
            return jsonify({"error": "Video stream not found for the given quality"}), 404

        # Download the video
        file_path = stream.download(output_path=DOWNLOAD_FOLDER)

        # Ensure the file exists and is the correct type
        if not os.path.exists(file_path) or not file_path.endswith(".mp4"):
            return jsonify({"error": "Downloaded file is corrupted or incorrect format"}), 500

        # Send the file back to the user
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
