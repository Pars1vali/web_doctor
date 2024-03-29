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

def controller():
    st.divider()
    foother()

def init():
    # st.header("Личный кабинет специалиста")
    data_doctor = json.loads(st.session_state.get("data_doctor"))
    st.title(f"{data_doctor[1]} {data_doctor[2]} {data_doctor[3]}")
    show_photo(data_doctor[12])
    annotated_text((f"{data_doctor[5]}", "Организация", "#afa"))
    annotated_text((f"{data_doctor[4]}", "Должность", "#afa"))
    annotated_text((f"{data_doctor[8]}", "Почта", "#afa"))
    annotated_text((f"{data_doctor[6]}", "Номер телефона", "#afa"))
    controller()

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