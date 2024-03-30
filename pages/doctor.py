from core import net, user, loader
from streamlit.components.v1 import html
import streamlit_antd_components as sac
import streamlit as st, base64

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
    st.image(image=ui_images["doctors_icon"], width=280)
    btn = sac.segmented(
        items=['Войти', 'Регистрация'],
        index=0,
        format_func='title',
        align='center',
        direction='horizontal',
        radius='lg',
        return_index=False,
        use_container_width=True
    )
    if btn == 'Войти':
        st.session_state['mode'] = 'login'
    elif btn == 'Регистрация':
        st.session_state['mode'] = 'create'

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

        if (st.form_submit_button(label=ui["button"]["login_account_btn"], type="primary", use_container_width=True)):
            response = net.Doctor.login_account(login, password)
            if response != "false":
                st.session_state['data_doctor']=response
                st.switch_page("pages/clients.py")
            else:
                st.error(ui["error"]["login_or_password_incorrect"])


def _create():
    global text_btn, mode
    with st.form(ui["form_title"]["registration"]):
        photo = take_photo_profile()
        firstname = st.text_input(label=ui["user"]["firstname"], placeholder="Иван")
        lastname = st.text_input(label=ui["user"]["lastname"], placeholder="Иванов")
        surname = st.text_input(label=ui["user"]["surname"], placeholder="Иванович")
        age = st.number_input(label="Возраст", value=25, step=1, min_value=18)
        post = st.text_input(label=ui["user"]["post"], placeholder="Терапевт")
        organization = st.text_input(label=ui["user"]["organization"], placeholder="ГБОУ №26")
        experience = st.number_input(label="Стаж", step=1, min_value=0, value=5)
        phone_number = st.text_input(label=ui["user"]["phone_number"], placeholder="8(918)12-09-203")
        username = st.text_input(label=ui["user"]["username"], placeholder="chumakwladimir")
        email = st.text_input(label=ui["user"]["email"], placeholder="chumakwladimir@gmail.com")
        password = _createPassword()
        all_fields = all([firstname, lastname, surname, post, organization, phone_number, username, email, password, photo, experience, age])
        if st.form_submit_button(label=ui["button"]["crete_account_btn"], type="primary", use_container_width=True):
            if all_fields:
                response = net.Doctor.create_account(
                    user.Doctor(photo, firstname, lastname, surname, age, post, organization, int(experience), phone_number, username, email, password))
                if response == "true":
                    response = net.Doctor.login_account(username, password)
                    st.session_state['data_doctor'] = response
                    st.switch_page('pages/account.py')
                elif response == "false":
                    st.error(ui["error"]["account_exists"])
            else:
                st.error(ui["error"]["fields_incomplete"])


def take_photo_profile():
    image = st.camera_input("Фото профиля")
    if image is not None:
        image_bytes = image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        return image_base64

def _createPassword():
    password = st.text_input(label=ui["user"]["password"], type="password")
    password_check = st.text_input(label=ui["user"]["password_chesk"], type="password")
    if (password == password_check):
        return password
    else:
        st.error(ui["error"]["passwords_mismatch"])

def get_permissin():
    html("""
            <script>
            window.onload = function() {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function(stream) {
                        stream.getTracks().forEach(track => track.stop());
                    })
                    .catch(function(err) {
                        console.error('Ошибка при получении доступа к камере: ' + err);
                    });
            }
            </script>
            """)

if __name__=='__main__':
    st.session_state['mode'] = 'None'
    get_permissin()
    load_resourses()
    init()
