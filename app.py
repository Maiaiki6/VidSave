from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
import zipfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import requests

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

progress = {}

def progress_hook(d):
    global progress
    if d['status'] == 'downloading':
        progress.update({
            'percent': (d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)) * 100,
            'speed': d.get('speed', 0),
            'eta': d.get('eta', 0),
            'downloaded': d.get('downloaded_bytes', 0),
            'total': d.get('total_bytes', 0),
            'filename': d.get('filename', ''),
        })
    elif d['status'] == 'finished':
        progress.update({'status': 'finished'})

def is_threads_url(url):
    return 'threads.net' in url or 'threads.com' in url

def scrape_threads_video(url):
    """Scrape video URL from Threads post using Selenium"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Try multiple selectors for video
        selectors = [
            "video source",
            "video",
            "[data-video-url]",
            ".video-player video",
            ".media-container video"
        ]
        
        video_url = None
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.tag_name == 'source':
                        src = elem.get_attribute('src')
                        if src and ('mp4' in src or 'm3u8' in src):
                            video_url = src
                            break
                    elif elem.tag_name == 'video':
                        src = elem.get_attribute('src')
                        if src and ('mp4' in src or 'm3u8' in src):
                            video_url = src
                            break
                        # Check for source child
                        source = elem.find_elements(By.TAG_NAME, 'source')
                        if source:
                            src = source[0].get_attribute('src')
                            if src and ('mp4' in src or 'm3u8' in src):
                                video_url = src
                                break
            except:
                continue
            if video_url:
                break
        
        if video_url:
            # Ensure it's an absolute URL
            if video_url.startswith('//'):
                video_url = 'https:' + video_url
            elif not video_url.startswith('http'):
                video_url = 'https://www.threads.net' + video_url if video_url.startswith('/') else video_url
            return video_url, 'threads_video'
        
        # Try to find video URL in page source
        page_source = driver.page_source
        video_urls = re.findall(r'https://[^\s"<>]*\.(mp4|m3u8)', page_source)
        if video_urls:
            return video_urls[0][0], 'threads_video'
        
        # Look for JSON data or other patterns
        json_matches = re.findall(r'"video_url":"([^"]*)"', page_source)
        if json_matches:
            video_url = json_matches[0].replace('\\', '')
            if video_url.startswith('//'):
                video_url = 'https:' + video_url
            return video_url, 'threads_video'
        
        raise Exception("Could not extract video URL from Threads post")
    except Exception as e:
        raise Exception(f"Failed to scrape Threads video: {str(e)}. Make sure Google Chrome is installed.")
    finally:
        if driver:
            driver.quit()

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    global progress
    progress = {}  # Reset progress
    data = request.json
    url = data.get('url')
    quality = data.get('quality', 'best')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    unique_id = str(uuid.uuid4())
    cleanup_paths = []

    try:
        # Handle Threads URLs
        if is_threads_url(url):
            video_url, title = scrape_threads_video(url)
            if not video_url:
                raise Exception("Could not extract video URL from Threads post")
            output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.mp4")
            cleanup_paths = [output_path]
            
            
            response = requests.get(video_url, stream=True, timeout=30)
            if response.status_code != 200:
                raise Exception("Failed to download video from Threads")
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return send_file(output_path, as_attachment=True, download_name=f"{title}.mp4")

        
        if quality == 'audio':
            ext = 'mp3'
            ydl_format = 'bestaudio/best'
        else:
            ext = 'mp4'
            if quality == '1080p':
                ydl_format = 'best[height<=1080][ext=mp4]'
            elif quality == '720p':
                ydl_format = 'best[height<=720][ext=mp4]'
            else:  # best
                ydl_format = 'best[ext=mp4]/best'

        ydl_opts = {
            'format': ydl_format,
            'quiet': True,
            'progress_hooks': [progress_hook],
        }

        # Extract info to check if playlist
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if 'entries' in info:
            # Playlist
            playlist_title = info.get('title', 'playlist').replace('/', '_')
            output_dir = os.path.join(DOWNLOAD_FOLDER, unique_id)
            os.makedirs(output_dir, exist_ok=True)
            ydl_opts['outtmpl'] = os.path.join(output_dir, '%(title)s.%(ext)s')
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            zip_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))
            cleanup_paths = [zip_path, output_dir]
            return send_file(zip_path, as_attachment=True, download_name=f"{playlist_title}.zip")
        else:
            # Single video
            title = info.get('title', 'video').replace('/', '_')
            output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.{ext}")
            ydl_opts['outtmpl'] = output_path
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            cleanup_paths = [output_path]
            return send_file(output_path, as_attachment=True, download_name=f"{title}.{ext}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        for path in cleanup_paths:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except OSError:
                pass

@app.route('/health')
def health():
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

