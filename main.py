import os
import pandas as pd
from pytubefix import YouTube
from pytubefix.cli import on_progress

CSV_FILE_NAME = 'downloaded_files.csv'
AUD_CONTENT_DIR = 'downloaded_audios'
VID_CONTENT_DIR = 'downloaded_videos'
RESULT_MSG_AUDIO = 'Your music “{0}” has been downloaded'
RESULT_MSG_VIDEO = 'Your video “{0}” has been downloaded'
ERR_MSG_BAD_URL = 'This URL is not recognized. Please insert a URL from a YouTube video.'
ERR_MSG_PRIVATE = 'This video is set as private by its owner. Please select another video.'


def download_content(url: str, file_extension: str) -> (str, str, str):
    def is_mp3():
        return file_extension.casefold() == 'mp3'.casefold()

    destination_dir = AUD_CONTENT_DIR if is_mp3() else VID_CONTENT_DIR
    result_msg = RESULT_MSG_AUDIO if is_mp3() else RESULT_MSG_VIDEO
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    file_path = None
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        if is_mp3():
            ys = yt.streams.get_audio_only()
        else:
            ys = yt.streams.get_highest_resolution()
        file_path = ys.download(
            output_path=destination_dir,
            filename=f'{yt.title}.{file_extension.lower()}')
    except Exception as e:
        if 'mregex_search' in str(e):
            result_msg = ERR_MSG_BAD_URL
        result_msg = ERR_MSG_PRIVATE
    return result_msg, yt.title, file_path


def download_video(url):
    return download_content(url, file_extension='mp4')


def download_video_audio(url):
    return download_content(url, file_extension='mp3')


def log_downloaded_files(content_type, title, path):
    downloaded_files = pd.DataFrame(columns=['Type', 'Title', 'Path'])
    if os.path.exists(CSV_FILE_NAME):
        downloaded_files = pd.read_csv(CSV_FILE_NAME)
    df_tmp = pd.DataFrame({'Type': content_type,
                           'Title': title,
                           'Path': os.path.abspath(path)
                           }, index=[0])
    downloaded_files = pd.concat([downloaded_files, df_tmp],
                                 ignore_index=True,
                                 sort=False)
    downloaded_files.to_csv(CSV_FILE_NAME, index=False)
