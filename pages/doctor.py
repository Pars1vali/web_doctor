from core import net, user, loader
import streamlit as st

ui, ui_images = None, None

def load_resourses():
    global ui, ui_images

    #TODO УБРАТЬ! БУдет только в классе centraln
    loader.set_resources(
        file_style="resources/style/style.css",
        file_localization="resources/ui/localization/localization_ru.json",
        file_images="resources/ui/image.json")

    st.markdown(loader.load_styles(), unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def init():
    st.image(image=ui_images["doctors_icon"], width=300)

    create, login = st.columns(2)
    if create.button(label=ui['button']['create_link_btn'], type="primary"):
        st.session_state['mode']='create'
    if login.button(label=ui['button']["login_link_btn"], type="primary"):
        st.session_state['mode']='login'

    controller()

def controller():
    if(st.session_state['mode']=='login'):
        _login()
    elif(st.session_state['mode']=='create'):
        _create()

def _login():
    with st.form(ui["form_title"]["login"]):
        login = st.text_input(label=ui["login"])
        password = st.text_input(label=ui["password"], type="password", key="login_password")

        if (st.form_submit_button(label=ui["button"]["login_account_btn"], type="primary")):
            response = net.Doctor.login_account(login, password)
            if response != "false":
                st.session_state['data_doctor']=response
                st.switch_page("pages/clients.py")
            else:
                st.error(ui["error"]["login_or_password_incorrect"])

def _create():
    with st.form(ui["form_title"]["registration"]):
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

        if st.form_submit_button(label=ui["button"]["crete_account_btn"], type="primary"):
            if all_fields:
                response = net.Doctor.create_account(
                    user.Doctor(firstname, lastname, surname, post, organization, phone_number, username, email, password))
                if response == "true":
                    st.switch_page('pages/account.py')
                elif response == "false":
                    st.error(ui["error"]["account_exists"])
            else:
                st.error(ui["error"]["fields_incomplete"])

def _createPassword():
    password = st.text_input(label=ui["user"]["password"], type="password")
    password_check = st.text_input(label=ui["user"]["password_chesk"], type="password")
    if (password == password_check):
        return password
    else:
        st.error(ui["error"]["passwords_mismatch"])



if __name__=='__main__':
    st.session_state['mode'] = 'login'
    load_resourses()
    init()
