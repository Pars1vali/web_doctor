from PIL import Image
from core import loader, net, fit_unit
from datetime import datetime, timedelta
from streamlit_extras.metric_cards import style_metric_cards
import base64, io
import  streamlit as st, json
import streamlit_antd_components as sac
import pandas as pd, time, re


ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def get_client_email():
    try:
        email = st.session_state.get('email')
        return email
    except Exception as e:
        st.info("Сеанс разорван. Перезайдите на платформу")
        time.sleep(1)
        st.switch_page("pages/doctor.py")

def get_client_id():
    try:
        client_id = st.session_state.get('client_id')
        return client_id
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
        items=['Показатели', 'Аналитика', 'Обращения'],
        index=0,
        format_func='title',
        align='center',
        direction='horizontal',
        radius='lg',
        use_container_width=True)

    email = get_client_email()
    client_id = get_client_id()

    match(mode):
        case 'Показатели':
            with st.spinner("Загрузка измерений..."):
                metrics(email, date)
        case 'Аналитика':
            with st.spinner("Анализируем..."):
                analitics(email, date)
        case 'Обращения':
            with st.spinner("Загрузка обращений..."):
                appeal(client_id, date)
        case 'Помощник':
            ai_helper()

def ai_helper():
    pass


# @st.cache_resource(experimental_allow_widgets=True)
def analitics(email, date):
    try:
        response = net.Client.get_data(email, date)
        df = pd.read_json(response).fillna(0).transpose()
        df.columns = fit_unit.FitUnit.change_name_columns(df.columns.tolist())
        default_metrics = list(['Калории','Счетчик шагов'])
        metrics = st.multiselect(label="Метрики", options=df.columns.tolist(), placeholder="Выбрать", default=default_metrics)
        st.line_chart(df[metrics], use_container_width=True)
        st.divider()
        st.write(df.transpose())
    except Exception as e:
        st.info("Данных за это время не собрано.")


# @st.cache_resource
def metrics(email, date):

    def _metrics_show(metrics):
        for name in metrics:
            metric_name, metric_value, metric_unit = fit_unit.FitUnit.get_data_unit(name, metrics[name])
            st.metric(label=f"{metric_name}", value=f"{metric_value}", delta=metric_unit, delta_color="off")
            style_metric_cards(border_color="#65C368", border_left_color="#65C368", box_shadow=False)

    response_json = net.Client.get_data(email, date)
    response = json.loads(response_json)
    metrics_list = [metrics for metrics in response]
    tabs = st.tabs(metrics_list)
    try:
        for metrics_number in response:
            with tabs[int(metrics_number)]:
                metric = response[metrics_number]
                if(len(metric)>0):
                    _metrics_show(metric)
                else:
                    st.subheader("Данных за это время не собрано")
    except Exception as e:
        print(e)
        st.warning("Сеанс разорван. Перезайдите...")
        time.sleep(2)
        st.switch_page("home.py")



def appeal(client_id, date):
    try:
        response_json = net.Client.get_appeal(client_id, date)
        response = json.loads(response_json)
        _appeal_show(response)
    except Exception as e:
        print(e)
        st.warning("Произошла ошибка загрузки данных")

def _appeal_show(appeals):
    for appeal in appeals:

        def _photo_show(image):
            try:
                image_box = appeal_box.container()
                image_str = image[2:-1]
                image_data = base64.b64decode(image_str)
                image = Image.open(io.BytesIO(image_data))
                image_box.image(image, use_column_width="auto")
            except Exception as e:
                print(e)
                appeal_box.info("Фотография не загружена")

        def _metrics_search(text):
            pattern = r"[а-я]* \d+\.?\d+?"
            matches = re.findall(pattern, text, re.IGNORECASE)
            for i in range(int(len(matches)/2)):
                metric_first = matches[i].split(" ")
                metric_second = matches[i + 1].split(" ")
                _metric_show(metric_first, metric_second)

            if len(matches)%2 != 0:
                _metric_show(matches[len(matches)-1].split(" "), None)

        def _metric_show(metric_first, metric_second:None):
                col_first, col_second = appeal_box.columns(2)
                col_first.metric(label=metric_first[0], value=metric_first[1])
                if metric_second is not None:
                    col_second.metric(label=metric_second[0], value=metric_second[1])
                style_metric_cards(border_color="#65C368", border_left_color="#65C368", box_shadow=False)

        topics, datetime = appeal[2], appeal[4]
        time = datetime.split(" ")[1]
        with st.expander(f"{topics} - {time}"):
            appeal_box = st.container(border=True)
            _photo_show(appeal[1])
            appeal_box.text(f"{appeal[3]}")
            _metrics_search(appeal[3])


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