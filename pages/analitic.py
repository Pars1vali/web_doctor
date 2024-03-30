from core import loader, net, fit_unit
from datetime import datetime, timedelta
import  streamlit as st, json
import streamlit_antd_components as sac
import pandas as pd, time


ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def get_email():
    try:
        email = st.session_state.get('email')
        return email
    except Exception as e:
        st.info("Сеанс разорван. Перезайдите на платформу")
        time.sleep(1)
        st.switch_page("pages/doctor.py")

def init():
    st.title("Даннные о здоровье")
    controller()
    st.divider()
    foother()


def controller():
    date = str(st.date_input("Выберите дату", max_value=datetime.now()))
    mode = sac.segmented(
        items=['Показатели', 'Аналитика', 'Обращения','Помощник'],
        index=0,
        format_func='title',
        align='center',
        direction='horizontal',
        radius='lg',
        use_container_width=True)

    email = get_email()

    match(mode):
        case 'Показатели':
            show_data(email, date)
        case 'Аналитика':
            analitics(email, date)
        case 'Обращения':
            pass
        case 'Помощник':
            ai_helper()

def ai_helper():
    pass

# @st.cache_resource(experimental_allow_widgets=True)
def analitics(email, date):
    response = net.Doctor.get_client_data(email, date)
    df = pd.read_json(response).fillna(0).transpose()
    df.columns = fit_unit.FitUnit.change_name_columns(df.columns.tolist())
    default_metrics = list(['Калории','Счетчик шагов'])
    metrics = st.multiselect(label="Метрики", options=df.columns.tolist(), placeholder="Выбрать", default=default_metrics)
    st.line_chart(df[metrics], use_container_width=True)
    st.divider()
    st.write(df.transpose())

# @st.cache_resource
def show_data(email, date):
    try:
        response_json = net.Doctor.get_client_data(email, date)
        response = json.loads(response_json)
        number_bucket_list = [number_bucket for number_bucket in response]
        tabs = st.tabs(number_bucket_list)
        for number_bucket in response:
            with tabs[int(number_bucket)]:
                points = response[number_bucket]
                if(len(points)>0):
                    show_points(points)
                else:
                    st.subheader("Данных за это время не собрано")
    except Exception as e:
        st.info("Данные за это время не собирались.")

def show_points(points):
    for num, point in enumerate(points):
        point_name, point_value, point_metric = fit_unit.FitUnit.get_data_unit(point, points[point])
        st.metric(label=f"{point_name}", value=f"{point_value}")#, delta=point_metric)

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