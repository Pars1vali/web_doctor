import os

import streamlit as st
from core import net, user, loader

ui, ui_images = None, None

def load_resourses(file_css, file_localization, file_images):
    global ui, ui_images
    with open(file_css) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    ui = loader.load_localization(file_localization)
    ui_images = loader.load_images(file_images)

def init():
    st.image(image=ui_images["main_icon"], width=200)
    if 'mode' not in st.session_state:
        st.session_state['mode'] = 'none'

    col1, col2 = st.columns(2)
    with col1:
        create_link_btn = st.button(label=ui['button']['create_link_btn'], type="primary")
    with col2:
        login_link_btn = st.button(label=ui['button']["login_link_btn"], type="primary")

    if create_link_btn:
        st.session_state['mode'] = 'create'
    if login_link_btn:
        st.session_state['mode'] = 'login'

    controller()

def controller():
    if st.session_state['mode'] == 'login':
        login = st.text_input(label=ui["login"])
        password = st.text_input(label=ui["password"], type="password", key="login_password")
        login_btn = st.button(label=ui["button"]["login_account_btn"], type="primary")
        if (login_btn):
           if net.Client.loginPersonalAccount(login, password) == "true":
               st.switch_page('pages/account.py')
           else:
               st.error(ui["error"]["login_or_password_incorrect"])
    elif st.session_state['mode'] == 'create':
        firstname = st.text_input(label=ui["user"]["firstname"])
        lastname = st.text_input(label=ui["user"]["lastname"])
        surname = st.text_input(label=ui["user"]["surname"])
        post = st.text_input(label=ui["user"]["post"])
        organization = st.text_input(label=ui["user"]["organization"])
        phone_number = st.text_input(label=ui["user"]["phone_number"])
        username = st.text_input(label=ui["user"]["username"])
        email = st.text_input(label=ui["user"]["email"])
        password = _createPassword()

        all_fields = all([firstname, lastname, surname, post, organization, phone_number, username, email, password])
        crete_account_btn = st.button(label=ui["button"]["crete_account_btn"], type="primary")
        if crete_account_btn:
            if all_fields:
                new_user = user.Doctor(firstname, lastname, surname, post, organization, phone_number, username, email, password)
                response = net.Client.createPersonalAccount(new_user)
                if response == "true":
                    st.switch_page('pages/account.py')
                elif response == "false":
                    st.error(ui["error"]["account_exists"])
            else:
                st.error(ui["error"]["fields_incomplete"])

def _createPassword():
    password = st.text_input(label=ui["user"]["password"], type="password")
    password_check = st.text_input(label=ui["user"]["password_chesk"], type="password")
    if(password==password_check):
        return password
    else:
        st.error(ui["error"]["passwords_mismatch"])

if __name__ == '__main__':
    user_language = "ru"
    load_resourses(file_css="resources/style/style.css",
                   file_localization=f"resources/ui/localization/localization_{user_language}.json",
                   file_images="resources/ui/image.json")
    init()
