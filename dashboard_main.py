import os
import pandas as pd
from main import download_video, download_video_audio, save_downloaded_files
import streamlit as st 

st.set_page_config(layout='wide', page_title='Youtube Video Downloader', page_icon="images/logo.png")
column1, column2 = st.columns([1,15])

with column1:
    st.image('images\\logo.png', width=100)

with column2:
    st.title("Youtube Video Downloader")

st.divider()
user_input = st.text_input("Youtube URL data", key="url")
st.divider()
column1, column2 = st.columns([1, 6])

message_placeholder = st.empty()

def handle_downloaded_video():
    if user_input:
        with st.spinner("Downloading video..."):
            result, file_path = download_video(user_input)
            message_placeholder.success(result)
            save_downloaded_files()
            return file_path

def handle_downloaded_audio():
    if user_input:
        with st.spinner("Downloading audio..."):
            result, file_path = download_video_audio(user_input)
            message_placeholder.success(result)
            return file_path

video_path = None
audio_path = None

with column1:
    if st.button("I want download a Video", help="Download your Youtube Video", use_container_width=False):
        video_path = handle_downloaded_video()

with column2:
    if st.button("I want download only the Audio", help="Download audio from your Youtube Video", use_container_width=False):
        audio_path = handle_downloaded_audio()

if video_path and os.path.exists(video_path):
    with open(video_path, 'rb') as file:
        st.download_button(
            label="Download Video",
            data=file.read(),
            file_name=os.path.basename(video_path),
            mime="video/mp4",
            use_container_width=True
        )

if audio_path and os.path.exists(audio_path):
    with open(audio_path, 'rb') as file:
        st.download_button(
            label="Download Audio",
            data=file.read(),
            file_name=os.path.basename(audio_path),
            mime="audio/mpeg",
            use_container_width=True
        )    




