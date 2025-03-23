import os
import yt_dlp
import streamlit as st
import subprocess

def ensure_ffmpeg():
    ffmpeg_path = "ffmpeg/ffmpeg"
    
    if not os.path.exists(ffmpeg_path):
        st.info("Baixando FFmpeg...")
        # baixando o FFmpeg
        ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"
        os.system(f"mkdir -p ffmpeg && wget {ffmpeg_url} -O ffmpeg.tar.xz && tar -xf ffmpeg.tar.xz -C ffmpeg --strip-components=1")
        
    return ffmpeg_path

def download_video(url, format):
    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    ffmpeg_path = ensure_ffmpeg()
    
    options = {
        'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_path,  # Aponta para o FFmpeg baixado
        'http_headers': headers,  # Cabeçalhos HTTP
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}] if format == 'mp3' else []
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            ydl.download([url])
            st.success(f"Download concluído ({format.upper()})! Arquivo salvo em '{output_path}'.")
        except Exception as e:
            st.error(f"Erro ao baixar: {str(e)}")

# interface do Streamlit
st.set_page_config(page_title="YouTube Downloader", page_icon="🎵", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-color: #1C1C1C;
        color: whitesmoke;
    }
    .stButton>button {
        background-color: #A52A2A;
        color: whitesmoke;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("YouTube Downloader ADB")
url = st.text_input("Cole o link do YouTube abaixo:")

col1, col2 = st.columns(2)
with col1:
    if st.button("Download MP3"):
        if url:
            download_video(url, 'mp3')
        else:
            st.warning("Por favor, insira um link do YouTube!")
with col2:
    if st.button("Download MP4"):
        if url:
            download_video(url, 'mp4')
        else:
            st.warning("Por favor, insira um link do YouTube!")
