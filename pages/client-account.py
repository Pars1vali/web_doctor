from random import random

from core import loader, auth, net, user
from annotated_text import annotated_text
from PIL import Image
from io import BytesIO
import streamlit as st, json, io, pandas as pd
import streamlit_antd_components as sac, base64
from streamlit_extras.metric_cards import style_metric_cards

ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def _createClientAccount(email,refresh_token):
    st.info(ui["info"]["first_registration"])
    with st.form(ui["form_title"]["registration"]):
        firstname = st.text_input(label=ui["user"]["firstname"])
        lastname = st.text_input(label=ui["user"]["lastname"])
        surname = st.text_input(label=ui["user"]["surname"])
        phone_number = st.text_input(label=ui["user"]["phone_number"])
        doctor_id = st.text_input(label=ui["user"]["doctor_id"])

        all_fields = all([firstname, lastname, surname, phone_number, doctor_id])
        if st.form_submit_button(label=ui["button"]["crete_account_btn"], type="primary", use_container_width=True):
            if all_fields:
                response = net.Client.create_account(
                    user.Client(firstname, lastname, surname, phone_number, int(doctor_id), email, str(refresh_token)))
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
def show_client_info(client_info):
    try:
        data_client = json.loads(client_info)
        st.title(f"{data_client[2]} {data_client[1]} {data_client[3]}")
        show_doctor_info(int(data_client[4]))
    except Exception as e:
        print(e)
        st.warning("Ошибка загрузки данных аккаунта")
def show_doctor_info(doctor_id):
    doctor_info_json = net.Doctor.get_doctor_info(doctor_id)
    doctor_info = json.loads(doctor_info_json)
    with st.popover("Врач", use_container_width=True):
        st.markdown(f"{doctor_info[1]} {doctor_info[2]} {doctor_info[3]}")
        show_photo(doctor_info[12])
        annotated_text((f"{doctor_info[11]}", "Возраст", "#afa"))
        annotated_text((f"{doctor_info[5]}", "Организация", "#afa"))
        annotated_text((f"{doctor_info[4]}", "Должность", "#afa"))
        annotated_text((f"{doctor_info[10]}", "Стаж", "#afa"))
        annotated_text((f"{doctor_info[8]}", "Почта", "#afa"))
        annotated_text((f"{doctor_info[6]}", "Номер телефона", "#afa"))

def init():
    st.header(ui["topics"]["personal_account"])
    # access_token, refresh_token = auth.get_token()
    token = auth.get_token()
    access_token = token["access_token"]
    # data_email = auth.get_email(access_token, refresh_token)
    data_email = auth.get_email(access_token)
    if data_email is not None:
        email = data_email['email']
        response = net.Client.login_account(email)
        if(response == 'false'):
            create_account(email, token["refresh_token"])
        else:
            show_client_info(response)
            controller()
def controller():
    make_appeal()
    foother()


def get_metrics_personal():
    c1, c2 = st.columns(2)
    c11 = c1.text_input("Измерение",key=f"kc11{random()}",value="")
    c22 = c2.number_input("Значение",key=f"kc22{random()})",value=0)
    return c11, c22


def make_appeal():
    with st.form("ff"):
        image = st.camera_input("Сделайте фотографию")
        topic = st.text_input("Тема обращения")
        description = st.text_area("Описание")
        st.divider()
        df = pd.DataFrame(
            [
                {"Измерние":"","Значение":""}
            ]
        )
        df.index = range(1, len(df) + 1)
        st.data_editor(df,use_container_width=True)
        if st.form_submit_button("Послать врачу", use_container_width=True, type="primary"):pass
    # if  st.button("Сделать обращение", use_container_width=True, type="primary"):
    #     container_request_doctor = st.container(border=True)
    #     image = container_request_doctor.camera_input("Сделайте фотографию")
    #     topic = container_request_doctor.text_input("Тема обращения")
    #     description = container_request_doctor.text_area("Описание")
    #
    #
    #     if container_request_doctor.button("Послать врачу", use_container_width=True, type="primary"):
    #         pass

        # if container_request_doctor.button("Закрыть", use_container_width=True):
        #     pass


    # with st.popover("Обращение врачу", use_container_width=True):
    #     # photo_container, text_container = st.columns(2)
    #     # image = photo_container.camera_input("Сделайте фотографию")
    #     # topic = text_container.text_input("Тема обращения")
    #     # description =  text_container.text_area("Описание")
    #     image = st.camera_input("Сделайте фотографию")
    #     topic = st.text_input("Тема обращения")
    #     description = st.text_area("Описание")
    #     st.button("Послать врачу", use_container_width=True)
def foother():
    sac.divider(icon=sac.BsIcon(name='bi bi-trash', size=20), align='center', color='gray')
    if st.button("Удалить аккаунт", type="primary", use_container_width=True):
        pass

if __name__ == '__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()