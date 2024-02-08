import streamlit as st
import json
import net, user

ui, ui_images = None, None

def _load_localization(file_name):
    global ui
    with open(file_name, 'r', encoding='utf-8') as file:
        ui = json.load(file)
def _load_images(file_name):
    global ui_images
    with open(file_name, 'r', encoding='utf-8') as file:
        ui_images = json.load(file)
def _local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
def load_resourses(file_css, file_localization, file_images):
    _local_css(file_css)
    _load_localization(file_localization)
    _load_images(file_images)
    pass
def _createPassword():
    password = st.text_input(label=ui["user"]["password"], type="password")
    password_chesk = st.text_input(label=ui["user"]["password_chesk"], type="password")
    if(password==password_chesk):
        return password
    else:
        st.error(ui["error"]["passwords_mismatch"])

def init():
    st.image(image=ui_images["main_icno"], width=200)
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

def controller():
    if st.session_state['mode'] == 'login':
        login = st.text_input(label=ui["login"])
        password = st.text_input(label=ui["password"], type="password", key="login_password")
        login_btn = st.button(label=ui["button"]["login_account_btn"], type="primary")
        if (login_btn):
            st.write(net.Client.loginPersonalAccount(login, password))
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
                if response == "false":
                    st.warning(ui["warning"]["successful_creating_account"])
                elif response == "true":
                    st.error(ui["error"]["account_exists"])
            else:
                st.error(ui["error"]["fields_incomplete"])


if __name__ == '__main__':
    user_language = "ru"
    load_resourses(file_css="resources/style/style.css",
                   file_localization=f"resources/ui/localization/localization_{user_language}.json",
                   file_images="resources/ui/image.json")
    init()
    controller()
