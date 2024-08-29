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


if __name__ == '__main__':
    st.set_page_config(
        layout='centered', page_title='Youtube Video Downloader', page_icon='logo.png')

    logo_col, heading_col = st.columns([1, 10])

    with logo_col:
        st.image('logo.png', width=80)
    with heading_col:
        st.title('Youtube Video Downloader')

    st.divider()
    user_input = st.text_area(
        'Paste one or more YouTube URLs, one per line:', key='url')
    st.divider()
    dl_btn_cols = st.columns(2)
    with dl_btn_cols[0]:
        dl_as_vid = st.button('Download URLs as Video', help='Download the YouTube URLs as video', use_container_width=True)

    with dl_btn_cols[1]:
        dl_as_aud = st.button('Download URLs as Audio only', help='Download the YouTube URLs as audio', use_container_width=True)

    if dl_as_vid:
        download_all_urls_and_log(read_lines(user_input), file_extension='mp4')

    if dl_as_aud:
        download_all_urls_and_log(read_lines(user_input), file_extension='mp3')
