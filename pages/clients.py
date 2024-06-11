from core import loader, net, fit_unit
from annotated_text import annotated_text
from PIL import Image
import streamlit as st, json, base64, io, time
try:
    st.set_page_config(page_icon="resources/images/icon.png",
                       page_title="Web doctor",
                       layout=st.session_state["mode_layout"],
                       menu_items=None,
                       initial_sidebar_state="collapsed")
except:
    st.set_page_config(page_icon="resources/images/icon.png",
                       page_title="Web doctor",
                       layout="centered",
                       menu_items=None,
                       initial_sidebar_state="collapsed")

ui, ui_images = None, None
clients = None


def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def load_clients():
    try:
        data_doctor_json = st.session_state.get("data_doctor")
        data_doctor = json.loads(data_doctor_json)
        doctor_id = data_doctor[0]
        clients_data = net.Client.get_id(doctor_id)
        return clients_data
    except Exception as e:
        return None
    # net.Doctor.get_client(json.loads(st.session_state.get("data_doctor"))[0])

def init():
    global clients
    clients = load_clients()
    # data_doctor = json.loads(st.session_state.get("data_doctor"))
    # st.header(f"{data_doctor[1]} {data_doctor[2]} {data_doctor[3]}")
    controller()

def controller():
    if clients is not None:
        show_clients()
    else:
        st.info("Сессеия разорвна. Пожалуйста перезайдите.")
        time.sleep(2)
        st.switch_page("home.py")
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
    def _show_client_photo(image):
        try:
            image_container = st.container(border=True)
            image_str = image[2:-1]
            image_data = base64.b64decode(image_str)
            image = Image.open(io.BytesIO(image_data))
            image_container.image(image, width=300)#, use_column_width="auto")
        except Exception as e:
            print(e)#
            image_container.info("Фотография не загружена")

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
            _show_client_photo(client[8])
            annotated_text((f"{client[5]}", "Почта", "#afa"))
            annotated_text((f"{client[6]}", "Номер телефона", "#afa"))
            # dt = st_ui.date_picker(key=f"{client[0]}", mode="single", label="Date Picker")
            if st.button(label="Данные о здоровье", type="primary", key=f"{client[0]}", use_container_width=True):
                # show_data(client[5])
                st.session_state['email'] = client[5]
                st.session_state['client_id'] = client[0]
                st.switch_page("pages/analitic.py")

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
