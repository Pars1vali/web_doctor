from core import loader, auth, net, user
from annotated_text import annotated_text
from PIL import Image
import streamlit as st, json, io
import streamlit_antd_components as sac, base64, datetime



ui, ui_images = None, None
def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def get_client_id(response):
    client_data = json.loads(response)
    client_id = client_data[0]
    return client_id

def _createClientAccount(email,refresh_token):
    def _take_photo_profile():
        image = st.camera_input("Фото профиля")
        if image is not None:
            image_bytes = image.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            return image_base64

    st.info(ui["info"]["first_registration"])
    with st.form(ui["form_title"]["registration"]):
        photo = _take_photo_profile()
        firstname = st.text_input(label=ui["user"]["firstname"])
        lastname = st.text_input(label=ui["user"]["lastname"])
        surname = st.text_input(label=ui["user"]["surname"])
        phone_number = st.text_input(label=ui["user"]["phone_number"])
        doctor_id = st.text_input(label=ui["user"]["doctor_id"])

        all_fields = all([firstname, lastname, surname, phone_number, doctor_id, photo])
        if st.form_submit_button(label=ui["button"]["crete_account_btn"], type="primary", use_container_width=True):
            if all_fields:
                response = net.Client.create_account(
                    user.Client(firstname, lastname, surname, phone_number, int(doctor_id), email, str(refresh_token), str(photo)))
                if response == "true":
                    return True
                elif response == "false":
                    st.info(response)
                    st.error(ui["error"]["account_exists"])
            else:
                st.error(ui["error"]["fields_incomplete"])
def create_account(email, refresh_token):
    if _createClientAccount(email, refresh_token):
        st.experimental_rerun()
        controller()
        show_client_info(net.Client.login_account(email))
@st.experimental_dialog("Удалить аккаунт")
def _delete_account():
    st.write(f"Why is  your favorite?")
    if st.button("Submit"):
        st.switch_page("home.py")

def show_photo(image):
    try:
        image_container = st.container(border=True)
        image_str = image[2:-1]
        image_data = base64.b64decode(image_str)
        image = Image.open(io.BytesIO(image_data))
        image_container.image(image, use_column_width="auto")
    except Exception as e:
        print(e)
        st.info("Фотография профиля не загружена")




def init():
    st.header(ui["topics"]["personal_account"])
    token = auth.get_token()
    access_token = token["access_token"]
    data_email = auth.get_email(access_token)
    if data_email is not None:
        email = data_email['email']
        with st.spinner("Загрузка данных..."):
            response = net.Client.login_account(email)
        if(response == 'false'):
            create_account(email, token["refresh_token"])
        else:
            controller(response, email)

def controller(response, email):
    show_client_info(net.Client.login_account(email))
    make_appeal(response)
    foother()

def show_doctor_info(doctor_id):
    doctor_info_json = net.Doctor.get_info(doctor_id)
    doctor_info = json.loads(doctor_info_json)
    with st.popover("Врач", use_container_width=True):
        st.markdown(f"{doctor_info[1]} {doctor_info[2]} {doctor_info[3]}")
        show_photo(doctor_info[12])
        annotated_text((f"{doctor_info[10]}", "Возраст", "#afa"))
        annotated_text((f"{doctor_info[5]}", "Организация", "#afa"))
        annotated_text((f"{doctor_info[4]}", "Должность", "#afa"))
        annotated_text((f"{doctor_info[11]}", "Стаж", "#afa"))
        annotated_text((f"{doctor_info[8]}", "Почта", "#afa"))
        annotated_text((f"{doctor_info[6]}", "Номер телефона", "#afa"))

def show_client_info(client_info):
    try:
        data_client = json.loads(client_info)
        st.title(f"{data_client[2]} {data_client[1]} {data_client[3]}")
        show_doctor_info(int(data_client[4]))
    except Exception as e:
        print(e)
        st.warning("Ошибка загрузки данных аккаунта")

def make_appeal(response):
    client_id = get_client_id(response)
    with st.expander("Сделать обращение врачу"):
        info_box = st.container()
        def take_photo():
            image = info_box.camera_input("Фотография")
            if image is not None:
                image_bytes = image.read()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                image_base64_str = str(image_base64)
                return image_base64_str

        image = take_photo()
        topic = info_box.text_input("Тема обращения")
        description = info_box.text_area("Описание")

        if st.button("Отправить врачу", use_container_width=True, type="primary"):
            datetime_now = datetime.datetime.now()
            datetime_now_str = str(datetime_now)
            response = net.Doctor.send_appeal(image, topic, description, datetime_now_str, client_id)
            if response == "true":
                st.info("Обращение доставленно доктору.")
            else:
                st.warning("Возникли ошибки при отправке. Сообщение не отправленно.")

def foother():
    sac.divider(icon=sac.BsIcon(name='bi bi-trash', size=20), align='center', color='gray')
    exit, remove_account = st.columns(2)
    if exit.button("Выйти", use_container_width=True):
        st.switch_page("home.py")
    if remove_account.button("Удалить аккаунт", type="primary", use_container_width=True):
        _delete_account()

if __name__ == '__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()