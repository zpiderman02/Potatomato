from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# Directory to temporarily store downloaded videos
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Get the request data
        data = request.json
        video_url = data.get('video_url')
        quality = data.get('quality')

        # Validate input
        if not video_url:
            return jsonify({'error': 'No video URL provided'}), 400

        # Download the YouTube video using pytube
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(res=quality, file_extension="mp4").first()

        if not video_stream:
            return jsonify({'error': f'{quality} quality not available for this video.'}), 404

        # Save the video
        video_file = video_stream.download(output_path=DOWNLOAD_FOLDER)
        video_filename = os.path.basename(video_file)

        # Send the file back to the client
        return send_file(
            os.path.join(DOWNLOAD_FOLDER, video_filename),
            as_attachment=True,
            download_name=video_filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Server is running!'})

if __name__ == '__main__':
    app.run(debug=True)
