from core import loader, auth
import streamlit as st

ui, ui_images = None, None


def load_resourses():
    global ui, ui_images

    # TODO УБРАТЬ! БУдет только в классе centralf
    loader.set_resources(
        file_style="resources/style/style.css",
        file_localization="resources/ui/localization/localization_ru.json",
        file_images="resources/ui/image.json")

    st.markdown(loader.load_styles(), unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()


def init():
    st.title(ui["topics"]["welcome_client"])
    st.image(ui_images['client_icon'], width=350)
    st.link_button(label=ui["link_button"]["login_google"], url=auth.get_login(), type="primary", use_container_width=True)


if __name__ == '__main__':
    load_resourses()
    init()
