from core import loader
import streamlit_antd_components as sac
import streamlit as st
import streamlit_shadcn_ui as ui

ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def init():
    st.title("Настройки")
    language = st.selectbox('Язык',('Русский', 'English', '中國人'))
    loader.set_language(language)
    theme = sac.segmented(
        items=['Светлая', 'Темная'],
        index=0,
        format_func='title',
        align='center',
        direction='horizontal',
        radius='lg',
        use_container_width=True
    )
    sac.divider(icon=sac.BsIcon(name='bi bi-trash', size=20), align='center', color='gray')
    if st.button("Удалить аккаунт", type="primary", use_container_width=True):
        pass
    # sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='bi bi-arrow-left-square', size=25))], align='center', variant='text', index=None)


if __name__ == '__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()