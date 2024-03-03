from core import loader, auth
import streamlit as st

ui, ui_images = None, None
def load_resourses():
    global ui, ui_images

    #TODO УБРАТЬ! БУдет только в классе central
    loader.set_resources(
        file_style="resources/style/style.css",
        file_localization="resources/ui/localization/localization_ru.json",
        file_images="resources/ui/image.json")

    st.markdown(loader.load_styles(), unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()


def init():
    st.title("Web-доктор для клиентов")
    st.image(ui_images['client_icon'], width=350)
    st.link_button(label="Войти в Google аккаунт", url=auth.get_login_str(), type="primary")



if(__name__ == '__main__'):
    load_resourses()
    init()