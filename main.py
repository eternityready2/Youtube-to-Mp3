import os
import pandas as pd
from pytubefix import YouTube
from pytubefix.cli import on_progress
 
download_video_folder = 'download_videos'
download_audio_folder = 'download_audios'

if not os.path.exists(download_video_folder):
     os.makedirs(download_video_folder)
    
if not os.path.exists(download_audio_folder):
     os.makedirs(download_audio_folder)

downloaded_files = pd.DataFrame(columns=['Type', 'Title', 'Path'])


def download_video(url):
    file = ""
    try:
        yt = YouTube(url, on_progress_callback = on_progress)        
        ys = yt.streams.get_highest_resolution()
        file = ys.download(output_path=download_video_folder)
        file_path = os.path.join(download_video_folder, f"{yt.title}.mp4")
        downloaded_files.loc[len(downloaded_files)]=['Video', yt.title, file_path]
        save_downloaded_files()
        return f"Your video is ready to download.", file
    except Exception as e:
        if "mregex_search" in str(e):
            return f"This url is not recognized. Please insert a url from a Youtube video.", file
        return f"This video is set as private by its owner. Please select another video.", file

def download_video_audio(url):
    file = ""
    try:
        yt = YouTube(url, on_progress_callback = on_progress)
        ys = yt.streams.get_audio_only()
        file = ys.download(output_path=download_audio_folder, filename=f"{yt.title}.mp3")
        file_path = os.path.join(download_audio_folder, f"{yt.title}.mp3")
        downloaded_files.loc[len(downloaded_files)]=['Audio', yt.title, file_path]
        save_downloaded_files()
        return f"Your music is ready do download.", file
    except Exception as e:
        if "mregex_search" in str(e):
            return f"This url is not recognized. Please insert a url from a Youtube video.", file
        return f"This video is set as private by its owner. Please select another video.", file
    

def save_downloaded_files():
     downloaded_files.to_csv('downloaded_files.csv', index=False)
