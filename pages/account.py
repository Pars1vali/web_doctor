from core import loader
from annotated_text import annotated_text
from PIL import Image
from io import BytesIO
import streamlit_antd_components as sac
import streamlit as st, json, base64, io

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
def load_doctor_info():
    try:
        doctor_info_json = st.session_state.get("data_doctor")
        doctor_info = json.loads(doctor_info_json)
        return doctor_info
    except Exception as e:
        return None
def controller():
    st.divider()
    foother()

def init():
    # st.header("Личный кабинет специалиста")
    doctor_info = load_doctor_info()
    if doctor_info is not None:
        show_bio(doctor_info)
    else:
        st.info("Сессия разорвана. Пожалуйста перезайдите.")
    controller()


def show_bio(info):
    st.title(f"{info[1]} {info[2]} {info[3]}")
    show_photo(info[12])
    annotated_text((f"{info[10]}", "Возраст", "#afa"))
    annotated_text((f"{info[11]}", "Стаж", "#afa"))
    annotated_text((f"{info[5]}", "Организация", "#afa"))
    annotated_text((f"{info[4]}", "Должность", "#afa"))
    annotated_text((f"{info[8]}", "Почта", "#afa"))
    annotated_text((f"{info[6]}", "Номер телефона", "#afa"))
def show_photo(image):
    try:
        image_container = st.container(border=True)
        image_str = image[2:-1]
        image_data = base64.b64decode(image_str)
        image = Image.open(io.BytesIO(image_data))
        image_container.image(image, use_column_width="auto")
    except Exception as e:
        print(e)
        st.info("Фотографии профиля не загружена")

def foother():
    clients, remove_account = st.columns(2)
    if clients.button("Назад", use_container_width=True):
        st.switch_page("pages/clients.py")
    if remove_account.button("Удалить аккаунт", type="primary", use_container_width=True):
        pass

if __name__=='__main__':
    load_resourses()
    init()