from core import loader, auth, net, user
from annotated_text import annotated_text
import streamlit as st, json

ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

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
            st.info(ui["info"]["first_registration"])
            _createClientAccount(email, token["refresh_token"])
        else:
            try:
                data_client = json.loads(response)
                st.title(f"{data_client[2]} {data_client[1]} {data_client[3]}")
                annotated_text((f"{data_client[5]}", "Почта", "#afa"))
                annotated_text((f"{data_client[6]}", "Номер телефона", "#afa"))
                annotated_text((f"{data_client[4]}", "Врач", "#afa"))
            except Exception as e:
                print(e)
                st.warning("Ошибка загрузки данных аккаунта")
    controller()

def controller():
    foother()

def foother():
    st.divider()
    exit, remove_account = st.columns(2)
    if exit.button(label="Выход", type="primary", use_container_width=True):
        st.switch_page("home.py")
    if remove_account.button("Удалить аккаунт", type="primary"):
        pass

def _createClientAccount(email,refresh_token):
    with st.form(ui["form_title"]["registration"]):
        firstname = st.text_input(label=ui["user"]["firstname"])
        lastname = st.text_input(label=ui["user"]["lastname"])
        surname = st.text_input(label=ui["user"]["surname"])
        phone_number = st.text_input(label=ui["user"]["phone_number"])
        doctor_id = st.text_input(label=ui["user"]["doctor_id"])

        all_fields = all([firstname, lastname, surname, phone_number, doctor_id])
        if st.form_submit_button(label=ui["button"]["crete_account_btn"], type="primary"):
            if all_fields:
                response = net.Client.create_account(
                    user.Client(firstname, lastname, surname, phone_number, int(doctor_id), email, str(refresh_token)))
                if response == "true":
                    st.write("Вошел")
                elif response == "false":
                    st.error(ui["error"]["account_exists"])
            else:
                st.error(ui["error"]["fields_incomplete"])

if __name__ == '__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()