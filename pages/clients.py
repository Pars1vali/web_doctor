from core import loader, net, fit_unit
from annotated_text import annotated_text
from streamlit_modal import Modal
from streamlit import components
import streamlit as st, json


ui, ui_images = None, None
clients = net.Doctor.get_client(json.loads(st.session_state.get("data_doctor"))[0])


def show_points(points):
    for num, point in enumerate(points):
        point_name, point_value, point_metric = fit_unit.FitUnit.get_data_unit(point, points[point])
        st.metric(f"{point_name}", f"{point_value}", point_metric)



def show_data(email):
    response = json.loads(net.Doctor.get_client_data(email))
    number_bucket_list = [number_bucket for number_bucket in response]
    tabs = st.tabs(number_bucket_list)
    for number_bucket in response:
        with tabs[int(number_bucket)]:
            points = response[number_bucket]
            if(len(points)>0):
                show_points(points)
            else:
                st.subheader("Данных за это время не собрано")


def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()


def init():
    data_doctor = json.loads(st.session_state.get("data_doctor"))
    # st.header(f"{data_doctor[1]} {data_doctor[2]} {data_doctor[3]}")
    controller()

def controller():
    header()
    st.divider()
    show_clients()


def show_clients():
    st.subheader("Пациенты")
    if clients == "null":
        st.info("Нет клиентов")
        return

    clients_data = json.loads(clients)
    for client in clients_data:
        with st.expander(f"{client[2]} {client[1]} {client[3]}"):
            annotated_text((f"{client[5]}", "Почта", "#afa"))
            annotated_text((f"{client[6]}", "Номер телефона", "#afa"))
            # annotated_text((f"{client[4]}", "Врач", "#afa"))
            if st.button(label="Данные о здоровье", type="primary", key=f"{client[0]}"):
                # data_input = st.popover("vfvf")
                show_data(client[5])

def header():
    account, exit = st.columns(2)
    if account.button(label="Аккаунт", type="primary"):
        st.switch_page("pages/account.py")
    if exit.button(label="Выйти", type="primary"):
        st.switch_page("home.py")



if __name__ == '__main__':
    user_language = "ru"
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()