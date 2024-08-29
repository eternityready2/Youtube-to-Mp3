import os
from main import download_video, download_video_audio, log_downloaded_files
import streamlit as st


@st.fragment
def insert_btn_to_save_media_locally(content_type, mime_type, title, file_path):
    with open(file_path, 'rb') as file_bytes:
        st.download_button(
            label=f'Download “{title}” as {content_type}',
            data=file_bytes.read(),
            file_name=os.path.basename(file_path),
            mime=f'{mime_type}',
            use_container_width=True
        )


def download_all_urls_and_log(urls, *, file_extension):
    def is_mp3():
        return file_extension.casefold() == 'mp3'.casefold()

    if not urls:
        st.toast('No URL provided, so nothing to download', icon='⚠️')
        return
    callback_func = download_video_audio if is_mp3() else download_video
    content_type = 'Audio' if is_mp3() else 'Video'
    for url in urls:
        msg_placeholder = st.toast(f'Downloading {content_type.lower()}...')
        result_msg, title, file_path = callback_func(url.strip())
        if file_path is None:
            msg_placeholder.toast(result_msg, icon='❌')
            continue
        msg_with_data = result_msg.format(title)
        msg_placeholder.toast(msg_with_data, icon='✅')
        log_downloaded_files(content_type, title, file_path)
        mime_type = 'audio/mp3' if is_mp3() else 'video/mp4'
        insert_btn_to_save_media_locally(content_type.lower(), mime_type, title, file_path)


def read_lines(s):
    """s: any multiline string"""
    return [url.strip() for url in s.split('\n') if url.strip() != '']


def download_all_urls_as_video():
    download_all_urls_and_log(read_lines(user_input), file_extension='mp4')


def download_all_urls_as_audio():
    download_all_urls_and_log(read_lines(user_input), file_extension='mp3')


if __name__ == '__main__':
    st.set_page_config(
        layout='wide', page_title='Youtube Video Downloader', page_icon='logo.png')

    column1, column2 = st.columns([1, 15])

    with column1:
        st.image('logo.png', width=80)
    with column2:
        st.title('Youtube Video Downloader')

    st.divider()
    user_input = st.text_area(
        'Paste one or more YouTube URLs, one per line:', key='url')
    st.divider()
    column1, column2 = st.columns([1, 6])

    with column1:
        st.button('I want download a Video', help='Download your Youtube Video',
                  on_click=download_all_urls_as_video, use_container_width=False)

    with column2:
        st.button('I want download only the Audio', help='Download audio from your Youtube Video',
                  on_click=download_all_urls_as_audio, use_container_width=False)
