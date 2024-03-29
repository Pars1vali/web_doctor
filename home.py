from core import loader
import streamlit as st

ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()




def init():
    st.title(ui["topics"]["welcome"])
    st.image(ui_images['main_icon'], width=320)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(ui["button"]["client"], use_container_width=True):
            st.switch_page("pages/client.py")

    with col2:
        if st.button(ui["button"]["doctor"], type="primary", use_container_width=True):
            st.switch_page("pages/doctor.py")

if __name__ == '__main__':
    user_language = "ru"
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()