# SRT Translator 🎬

A minimal, free, and easy-to-deploy SRT subtitle translator using Flask and Google Translate (no API key needed).

## Features

- ✅ **100% Free** - Uses Google Translate API with no authentication required
- ✅ **Local Execution** - Runs entirely on your machine
- ✅ **Simple UI** - Minimal web interface for uploading and translating SRT files
- ✅ **Dockerized** - Ready to deploy on any Docker-compatible platform
- ✅ **Multiple Languages** - Supports 20+ languages
- ✅ **Batch Processing** - Translates all subtitles in one go

## Quick Start

### Prerequisites
- Python 3.11+ (for local development)
- Docker (for containerized deployment)

### Local Development

1. **Clone/Setup the project:**
   ```bash
   cd /path/to/translation
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   python server.py
   ```

5. **Open in browser:**
   ```
   http://localhost:5000
   ```

### Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t srt-translator .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 srt-translator
   ```

3. **Access the app:**
   ```
   http://localhost:5000
   ```

## Supported Languages

Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese (Simplified & Traditional), Arabic, Hindi, Polish, Turkish, Dutch, Swedish, Danish, Finnish, Greek, and more.

## How It Works

1. **Upload** an SRT file via the web interface
2. **Select** target language
3. **Click** "Translate SRT"
4. The app parses the SRT file, translates each subtitle using Google Translate
5. **Download** the translated SRT file automatically

## API Endpoint

```
POST /api/translate
```

**Parameters:**
- `file` (multipart/form-data): SRT file
- `target_lang` (string): Target language code (e.g., "es", "fr", "de")

**Response:**
- Returns the translated SRT file as a downloadable attachment

## File Structure

```
.
├── server.py              # Flask backend
├── templates/
│   └── index.html         # Frontend UI
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md            # This file
```

## Limitations

- **Size limit:** 50MB max file size
- **Rate limit:** Google Translate has unofficial rate limits (not documented)
- **Accuracy:** Translation quality depends on Google Translate

## Troubleshooting

### "Connection error" when translating
- Check your internet connection (Google Translate requires online access)
- The free API may have rate limits if too many requests are made
- Wait a few minutes and try again

### Docker build fails
- Ensure you have Docker installed: `docker --version`
- Check that the requirements.txt is correct

### Port already in use
- Change the port in `server.py` (line: `app.run(..., port=5000)`)
- Or stop the process using port 5000

## License

MIT License - Feel free to use, modify, and deploy!
