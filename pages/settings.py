from core import loader
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
    theme = st.selectbox('Тема', ("Light", "Dark"))
    st.divider()
    if st.button("Удалить аккаунт", type="primary", use_container_width=True):
        pass


if __name__ == '__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()