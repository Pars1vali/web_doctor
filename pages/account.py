from core import loader
from annotated_text import annotated_text
import streamlit as st, json

# from st_pages import Page, show_pages, hide_pages
#
# show_pages([
#     Page("pages/account.py", "Личный кабинет"),
#     Page("pages/clients.py", "Клиенты")
# ])

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

def foother():
    st.divider()
    clients, settings = st.columns(2)
    # if remove_account.button("Удалить аккаунт", type="primary", use_container_width=True):
    #     pass
    if clients.button("Клиенты", use_container_width=True):
        st.switch_page("pages/clients.py")
    if settings.button("Настройки", type="primary", use_container_width=True):
        st.switch_page("pages/settings.py")
    # if exit.button(label="Выход", type="primary", use_container_width=True):
    #     st.switch_page("home.py")

def controller():
    foother()

def init():
    # st.header("Личный кабинет специалиста")
    data_doctor = json.loads(st.session_state.get("data_doctor"))
    st.title(f"{data_doctor[1]} {data_doctor[2]} {data_doctor[3]}")
    image_container = st.container(border=True)
    image_container.image("experiment/doctor.png", use_column_width="auto")
    annotated_text((f"{data_doctor[5]}", "Организация", "#afa"))
    annotated_text((f"{data_doctor[4]}", "Должность", "#afa"))
    annotated_text((f"{data_doctor[8]}", "Почта", "#afa"))
    annotated_text((f"{data_doctor[6]}", "Номер телефона", "#afa"))
    controller()

if __name__=='__main__':
    load_resourses()
    init()