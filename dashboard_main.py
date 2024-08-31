import os
import re
import shutil
from time import time_ns
from util import (
    download_video, download_video_audio, log_downloaded_files, read_lines)
import streamlit as st


@st.fragment()
def insert_saving_options_ui(cnt_typ, title, tmp_file_path, uniq_key):
    if os.path.exists(tmp_file_path):
        mime_type = f'{cnt_typ.lower()}/{tmp_file_path.lower()[-3:]}'
        saving_options_cols = st.columns([10, 2])
        with saving_options_cols[0]:
            with open(tmp_file_path, 'rb') as file_bytes:
                save_locally_btn = st.download_button(
                    label=f'Save “{title}” {cnt_typ.lower()} on your device',
                    data=file_bytes.read(),
                    file_name=os.path.basename(tmp_file_path),
                    mime=mime_type,
                    use_container_width=True
                )
                if save_locally_btn:
                    os.remove(tmp_file_path)
                    st.rerun(scope='fragment')

        with saving_options_cols[1]:
            perm_file_path = re.sub(r'^/tmp', os.getcwd(), tmp_file_path)
            save_on_host_btn = st.button(
                key=uniq_key,
                label='or on host',
                use_container_width=True,
            )
            if save_on_host_btn:
                os.makedirs(os.path.dirname(perm_file_path), exist_ok=True)
                shutil.move(tmp_file_path, perm_file_path)
                log_downloaded_files(cnt_typ, title, perm_file_path)
                st.rerun(scope='fragment')


def download_all_urls_and_log(urls, *, file_extension):
    def is_mp3():
        return file_extension.casefold() == 'mp3'.casefold()

    callback_func = download_video_audio if is_mp3() else download_video
    content_type = 'Audio' if is_mp3() else 'Video'
    for url in urls:
        msg_placeholder = st.toast(f'Downloading {content_type.lower()}...')
        result_msg, title, tmp_file_path = callback_func(url.strip())
        if tmp_file_path is None:
            msg_placeholder.toast(result_msg, icon='❌')
            continue
        msg_with_data = result_msg.format(title)
        msg_placeholder.toast(msg_with_data, icon='✅')
        uniq_key = f'{time_ns()}'
        insert_saving_options_ui(content_type, title, tmp_file_path, uniq_key)


if __name__ == '__main__':
    st.set_page_config(
        layout='centered', page_title='Youtube Video Downloader', page_icon='logo.png')

    logo_col, heading_col = st.columns([1, 10])

    with logo_col:
        st.image('logo.png', width=80)
    with heading_col:
        st.title('Youtube Video Downloader')

    KEY_DL_MODE_CHOSEN = 'is_dl_mode_chosen'
    if KEY_DL_MODE_CHOSEN not in st.session_state:
        st.session_state[KEY_DL_MODE_CHOSEN] = False

    st.divider()
    user_input = st.text_area('Paste one or more YouTube URLs, one per line:',
                              key='urls',
                              disabled=st.session_state[KEY_DL_MODE_CHOSEN])
    urls = read_lines(user_input)
    st.divider()

    dl_btn_cols = st.columns(2)
    with dl_btn_cols[0]:
        dl_as_vid = st.button('Download URLs as Video', key='dl_as_vid',
                              disabled=st.session_state[KEY_DL_MODE_CHOSEN],
                              use_container_width=True)
    with dl_btn_cols[1]:
        dl_as_aud = st.button('Download URLs as Audio only', key='dl_as_aud',
                              disabled=st.session_state[KEY_DL_MODE_CHOSEN],
                              use_container_width=True)

    if dl_as_vid:
        if not st.session_state[KEY_DL_MODE_CHOSEN]:
            if not urls:
                st.toast('No URL provided, so nothing to download', icon='⚠️')
            else:
                st.session_state[KEY_DL_MODE_CHOSEN] = True
                download_all_urls_and_log(urls, file_extension='mp4')

    if dl_as_aud:
        if not st.session_state[KEY_DL_MODE_CHOSEN]:
            if not urls:
                st.toast('No URL provided, so nothing to download', icon='⚠️')
            else:
                st.session_state[KEY_DL_MODE_CHOSEN] = True
                download_all_urls_and_log(urls, file_extension='mp3')
