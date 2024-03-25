from core import loader, net, fit_unit
import  streamlit as st, json, datetime
import streamlit_antd_components as sac
import pandas as pd

ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()


def init():
    st.title("Даннные о здоровье")
    controller()
    st.divider()
    foother()


def controller():
    date = st.date_input("Выберите дату", max_value=datetime.datetime.now())
    email = st.session_state['email']
    mode = sac.segmented(
        items=['Показатели', 'Аналитика', 'Обращения','Чат', 'Помощник'],
        index=0,
        format_func='title',
        align='center',
        direction='horizontal',
        radius='lg',
        use_container_width=True)

    match(mode):
        case 'Показатели':
            show_data(email, date)
        case 'Аналитика':
            analitics(email, date)
        case 'Обращения':
            pass
        case 'Чат':
            chat_with_client()
        case 'Помощник':
            pass

def chat_with_client():
    pass


# @st.cache_resource(experimental_allow_widgets=True)
def analitics(email, date):
    response = net.Doctor.get_client_data(email)
    df = pd.read_json(response).fillna(0).transpose()
    df.columns = fit_unit.FitUnit.change_name_columns(df.columns.tolist())
    st.write(df.transpose())
    st.divider()
    metrics = st.multiselect(label="Метрики", options=df.columns.tolist(), placeholder="Выбрать")
    st.line_chart(df[metrics], use_container_width=True)




@st.cache_resource
def show_data(email, date):
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


def show_points(points):
    for num, point in enumerate(points):
        point_name, point_value, point_metric = fit_unit.FitUnit.get_data_unit(point, points[point])
        st.metric(f"{point_name}", f"{point_value}", point_metric)

def foother():
    if st.button("Назад", type="primary", use_container_width=True):
        st.switch_page("pages/clients.py")



if __name__=='__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()