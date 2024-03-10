from core import loader, auth
from streamlit.components.v1 import html
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
    st.title(ui["topics"]["welcome_client"])
    st.image(ui_images['client_icon'], width=350)
    #<script src="https://apis.google.com/js/platform.js" async defer></script>
    html("""
    <html>
      <body>
        <script src="https://accounts.google.com/gsi/client" async></script>
        <div id="g_id_onload"
            data-client_id="169068403601-tubkif2prt01v1la1ecspr2me96mvi9s.apps.googleusercontent.com"
            data-login_uri="https://web-doctor.streamlit.app/client-account"
            data-auto_prompt="false">
        </div>
        <div class="g_id_signin"
            data-type="standard"
            data-size="large"
            data-theme="outline"
            data-text="sign_in_with"
            data-shape="rectangular"
            data-logo_alignment="left">
        </div>
      <body>
    </html>""")

    st.link_button(label=ui["link_button"]["login_google"], url=auth.get_login_str(), type="primary")

if(__name__ == '__main__'):
    load_resourses()
    init()