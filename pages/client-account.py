from core import loader, auth, net, user
import streamlit as st

ui, ui_images = None, None
email = None
def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def init():
    global email
    st.title("Личный кабинет")
    #TODO при обновлении старницы идет еще раз запрос на email и второый раз токен истекает, нужно вызываь один раз
    if st.session_state['mode']=='login':
        print("FF")
        st.write("ff")
        email = auth.display_user()
        st.session_state['mode']='loged'


    if(net.Client.loginClientAccount(email) == 'false'):
        st.info("Первичная регистрация")
        _createClientAccount(email)


def _createClientAccount(email):
    global ui
    with st.form("Регистрация"):
        firstname = st.text_input("Имя")
        lastname = st.text_input("Фамилия")
        surname = st.text_input("Отчество")
        phone_number = st.text_input("Номер телефона")
        doctor_id = st.text_input("ID Доктора")

        all_fields = all([firstname, lastname, surname, phone_number, doctor_id])
        if st.form_submit_button(label=ui["button"]["crete_account_btn"], type="primary"):
            if all_fields:
                response = net.Client.createClientAccount(
                    user.Client(firstname, lastname, surname, phone_number, doctor_id, email))
                if response == "true":
                    st.write("Вошел")
                elif response == "false":
                    st.error(ui["error"]["account_exists"])
            else:
                st.error(ui["error"]["fields_incomplete"])

if __name__ == '__main__':
    user_language = "ru"
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    st.session_state['mode'] = 'login'
    init()