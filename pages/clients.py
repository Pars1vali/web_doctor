from core import loader, net, fit_unit
from annotated_text import annotated_text
import streamlit_shadcn_ui as st_ui
import streamlit as st, json


ui, ui_images = None, None
clients = net.Doctor.get_client(json.loads(st.session_state.get("data_doctor"))[0])


def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()


def init():
    # data_doctor = json.loads(st.session_state.get("data_doctor"))
    # st.header(f"{data_doctor[1]} {data_doctor[2]} {data_doctor[3]}")
    controller()


def controller():
    show_clients()
    st.divider()
    foother()


def search_client(search_query):
    st.markdown("Найдено:")
    is_found = False
    clients_data = json.loads(clients)
    for client in clients_data:
        first_and_lastname = f"{client[2]} {client[1]}"
        if first_and_lastname == search_query or search_query==client[2] or search_query==client[1]:
            is_found = True
            with st.expander(f"{client[2]} {client[1]} {client[3]}"):
                annotated_text((f"{client[5]}", "Почта", "#afa"))
                annotated_text((f"{client[6]}", "Номер телефона", "#afa"))
                if st.button(label="Данные о здоровье", type="primary", key=f"{client[0]}_search"):
                    # show_data(client[5])
                    st.session_state['email'] = client[5]
                    st.switch_page("pages/analitic.py")
                    

    if is_found is False:
        st.info("Не найдено")


def show_clients():
    st.header("Клиенты")
    search = st.text_input(label="Найти", placeholder="Иванов Иван")
    if search is not None and search != "":
        search_client(search)

    if clients == "null":
        st.info("Нет клиентов")
        return
    st.markdown("Все клиенты")

    clients_data = json.loads(clients)
    for client in clients_data:
        with st.expander(f"{client[2]} {client[1]} {client[3]}"):
            annotated_text((f"{client[5]}", "Почта", "#afa"))
            annotated_text((f"{client[6]}", "Номер телефона", "#afa"))
            # dt = st_ui.date_picker(key=f"{client[0]}", mode="single", label="Date Picker")
            if st.button(label="Данные о здоровье", type="primary", key=f"{client[0]}", use_container_width=True):
                # show_data(client[5])
                st.session_state['email'] = client[5]
                st.switch_page("pages/analitic.py")


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



def foother():
    account, exit = st.columns(2)
    if account.button(label="Аккаунт", use_container_width=True):
        st.switch_page("pages/account.py")
    if exit.button(label="Выйти", type="primary", use_container_width=True):
        st.switch_page("home.py")




if __name__ == '__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()
