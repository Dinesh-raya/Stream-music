import streamlit as st
import requests
from urllib.parse import urljoin

st.set_page_config(page_title="Music Player", layout="wide")
API_BASE = "https://musicapi.x007.workers.dev"

# Sidebar controls
st.sidebar.title("🎵 Music Player Settings")
theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)
query = st.sidebar.text_input("Search for a song or artist", value="Arijit Singh")
search_engine = st.sidebar.selectbox(
    "Music Source", ["gaama", "seevn", "hunjama", "mtmusic", "wunk"], index=0
)
search_btn = st.sidebar.button("Search")

# Apply theme
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; color: #E6EEF3; }
        .stSidebar { background-color: #0B0D10; color: #E6EEF3; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def api_search(q, engine):
    endpoint = urljoin(API_BASE, "search")
    r = requests.get(endpoint, params={"q": q, "searchEngine": engine}, timeout=15)
    r.raise_for_status()
    return r.json()


@st.cache_data(show_spinner=False)
def api_fetch(song_id):
    endpoint = urljoin(API_BASE, "fetch")
    r = requests.get(endpoint, params={"id": song_id}, timeout=20)
    r.raise_for_status()
    return r.json()


# Playlist memory
if "playlist" not in st.session_state:
    st.session_state.playlist = []

st.title("🎧 Streamlit Music Player")
st.caption("Audio-only playback with HLS (.m3u8) support. No downloads.")


def play_audio(audio_url: str):
    """Play audio inline (supports both MP3 and HLS .m3u8)."""
    if not isinstance(audio_url, str) or not audio_url:
        st.error("Invalid audio URL.")
        return

    if audio_url.lower().endswith(".m3u8"):
        # Use hls.js for HLS playback
        player_html = (
            '<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>'
            '<audio id="audio" controls autoplay style="width:100%"></audio>'
            '<script>'
            'var audio = document.getElementById("audio");'
            'if (window.Hls && Hls.isSupported()) {'
            '  var hls = new Hls();'
            '  hls.loadSource("%s");'
            '  hls.attachMedia(audio);'
            '} else if (audio.canPlayType("application/vnd.apple.mpegurl")) {'
            '  audio.src = "%s";'
            '} else {'
            '  audio.outerHTML = "<p>❌ Your browser does not support HLS playback.</p>";'
            '}'
            '</script>'
        ) % (audio_url, audio_url)
        st.components.v1.html(player_html, height=120)
    else:
        st.audio(audio_url)


def handle_play(song):
    """Fetch song from API and play."""
    try:
        resp = api_fetch(song.get("id"))
        if not isinstance(resp, dict):
            st.error("Unexpected fetch response format.")
            return
        if resp.get("status") == 200:
            audio_url = resp.get("response")
            if not audio_url:
                st.error("No audio URL returned for this track.")
                return
            play_audio(audio_url)
        else:
            st.error("API fetch returned non-200 status.")
    except requests.exceptions.RequestException as re:
        st.error(f"Network/API error: {re}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")


# Search and display
if search_btn and query.strip():
    st.info(f"Searching for **{query.strip()}** on **{search_engine}**...")
    try:
        data = api_search(query.strip(), search_engine)
        if not isinstance(data, dict) or data.get("status") != 200:
            st.warning("No results or unexpected API response.")
        else:
            items = data.get("response") or []
            if not items:
                st.info("No songs found.")
            else:
                cols = st.columns(3)
                for i, song in enumerate(items):
                    col = cols[i % 3]
                    with col:
                        img = song.get("img")
                        if img:
                            st.image(img, use_column_width=True)
                        st.markdown(f"**{song.get('title', 'Untitled')}**")
                        c1, c2 = st.columns([2, 1])
                        with c1:
                            if st.button("▶ Play", key=f"play_{song.get('id')}"):
                                handle_play(song)
                        with c2:
                            if st.button("➕ Add", key=f"add_{song.get('id')}"):
                                if all(s.get("id") != song.get("id") for s in st.session_state.playlist):
                                    st.session_state.playlist.append(song)
                                    st.success(f"Added: {song.get('title', 'Untitled')}")
    except requests.exceptions.RequestException as re:
        st.error(f"Search/network error: {re}")
    except Exception as e:
        st.error(f"Unexpected error during search: {e}")


# Playlist section
if st.session_state.playlist:
    st.markdown("---")
    st.subheader("🎶 Now Playing Queue")
    for idx, song in enumerate(list(st.session_state.playlist), 1):
        with st.expander(f"{idx}. {song.get('title', 'Untitled')}"):
            if song.get("img"):
                st.image(song.get("img"), width=120)
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(song.get("title", "Untitled"))
            with c2:
                if st.button("Play", key=f"queue_play_{song.get('id')}"):
                    handle_play(song)
            with c3:
                if st.button("Remove", key=f"queue_remove_{song.get('id')}"):
                    st.session_state.playlist = [
                        s for s in st.session_state.playlist if s.get("id") != song.get("id")
                    ]
                    st.experimental_rerun()
