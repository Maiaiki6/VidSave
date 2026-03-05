from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    unique_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.mp4")

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best[ext=mp4]/best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_path, as_attachment=True, download_name="video.mp4")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

@app.route('/health')
def health():
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

