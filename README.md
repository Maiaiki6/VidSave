# VidSave – Video Downloader

A sleek, fast, and user-friendly web application for downloading videos from YouTube and other platforms. Built with Flask and yt_dlp, VidSave provides a minimal yet powerful interface to fetch and save your favorite videos.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

✨ **Key Highlights:**
- 🎥 Download videos from YouTube and 1000+ supported platforms
- 🎨 Modern, dark-themed UI with gradient accents
- ⚡ Fast streaming download with optimal quality selection
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🔒 Secure server-side processing
- 🚀 Easy deployment to Railway
- ✅ Health check endpoint for monitoring

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask (Python) |
| Video Download | yt_dlp |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Deployment | Heroku, Docker-ready |

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection for video downloads

## Installation

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd VidSave
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the app:**
   Open your browser and navigate to `http://localhost:5000`

## Usage

### Web Interface

1. Enter a video URL (YouTube, Instagram, TikTok, etc.)
2. Click the **Download** button
3. Wait for processing (status updates shown in real-time)
4. Your video downloads automatically

### Supported Platforms

VidSave supports 1000+ platforms including:
- YouTube
- Instagram
- TikTok
- Vimeo
- Twitter/X
- Facebook
- And many more...

## API Endpoints

### POST `/download`
Download a video from the provided URL.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response (Success - 200):**
- Returns the video file as an MP4 attachment

**Response (Error - 400/500):**
```json
{
  "error": "Error message describing the issue"
}
```

### GET `/`
Serves the main HTML interface.

**Response:** HTML page

### GET `/health`
Health check endpoint.

**Response (200):**
```json
{
  "status": "running"
}
```

## Deployment

### Deploy to Railway

1. **Create a Railway account** at [railway.app](https://railway.app)

2. **Connect your repository:**
   - Log in to Railway dashboard
   - Click **New Project** → **Deploy from GitHub**
   - Select your GitHub repository
   - Authorize Railway to access your repo

3. **Configure the deployment:**
   - Railway auto-detects your Python project
   - Ensure `Procfile` is present (already included)
   - Set environment variables if needed (see below)

4. **Deploy automatically:**
   - Railway deploys automatically on every push to your main branch
   - Monitor deployment logs in the Railway dashboard

5. **Access your app:**
   - Railway provides a unique domain URL
   - View it in the Railway dashboard under your project

### Environment Variables

Railway automatically sets the `PORT` environment variable. No additional configuration needed for basic setup.

**Optional custom variables:**
```
PORT=5000  (set by Railway automatically)
```

To add custom variables in Railway:
- Open your project
- Go to **Variables** tab
- Add key-value pairs as needed

## Configuration

### Custom Settings

Edit `app.py` to customize:

- **Download folder:** Change `DOWNLOAD_FOLDER` variable
- **Output format:** Modify `ydl_opts` parameters
- **Port:** Set `PORT` environment variable
- **Host binding:** Change `host` in `app.run()`

### Video Format Options

Current configuration downloads the best available MP4 format. To change:

```python
ydl_opts = {
    'format': 'best[ext=mp4]/best',  # Edit this line
    # Options: 'best', 'worst', 'bestaudio', 'bestvideo', etc.
}
```

## File Structure

```
VidSave/
├── app.py              # Flask application & API endpoints
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment config
├── README.md          # This file
└── downloads/         # Downloaded videos (auto-created)
```

## Performance & Limitations

⚠️ **Important Notes:**
- Large videos may take time to download and process
- Some platforms may have DRM protection and cannot be downloaded
- Downloads are temporary and removed after serving
- Server resources limit concurrent downloads
- Respect platform terms of service and copyright laws

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No URL provided" error | Ensure you entered a valid URL |
| Download fails silently | Check if the video URL is accessible |
| 500 error | The video platform may not be supported or the video is blocked |
| Slow performance | Wait for the download to complete; large files take time |
| Railway app crashes | Check Railway dashboard logs under **Logs** tab for error details |

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Security & Legal Notice

⚖️ **Important:**
- Use VidSave responsibly and respect copyright laws
- Only download content you have permission to download
- Check local regulations regarding video downloading
- This tool is for educational purposes and personal use

## Support

For issues, feature requests, or questions:
- Open a GitHub issue
- Email: [mustymaks@hotmail.com]

## Changelog

### v1.0.0 - Initial Release
- Core video download functionality
- Modern web UI
- Health check endpoint
- Heroku deployment ready

---

**Made with ❤️ by the VidSave Team**
