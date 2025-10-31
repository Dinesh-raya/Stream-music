# Streamlit Music Player (Final)

This project is a standalone Streamlit application that searches and plays music using the Music API.
It supports both direct audio files and HLS (.m3u8) streams using hls.js injected into the page.

## How to run
1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Open the URL shown by Streamlit (usually http://localhost:8501)

## Notes on behavior and safety
- The app intentionally does not allow downloads — playback only.
- HLS playback requires a modern browser (Chrome/Firefox/Edge/Safari).
- If an HLS stream fails to play, the page will show a friendly message.
