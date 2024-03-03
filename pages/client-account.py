from core import loader, auth, net, user
import streamlit as st

ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

@st.cache_resource
def get_email():
    return auth.display_user()

def init():
    st.title(ui["topics"]["personal_account"])
    email = get_email()
    st.write(email)

    if(net.Client.login_account(email) == 'false'):
        st.info(ui["info"]["first_registration"])
        _createClientAccount(email)
    else:
        st.write("есть аккаунт")

def _createClientAccount(email):
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
                    user.Client(firstname, lastname, surname, phone_number, int(doctor_id), email))
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
    init()