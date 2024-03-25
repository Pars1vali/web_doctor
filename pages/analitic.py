from core import loader, net, fit_unit
import  streamlit as st, json, datetime
import streamlit_antd_components as sac

ui, ui_images = None, None

def load_resourses(file_style,file_localization, file_images ):
    global ui, ui_images
    loader.set_resources(file_style, file_localization, file_images)

    st.markdown(loader.load_styles(),unsafe_allow_html=True)
    ui, ui_images = loader.load_localization(), loader.load_images()

def init():
    st.title("Даннные о здоровье")
    controller()


def chat_with_client():
    message = st.chat_message("assistant")
    message.write("Hello human")
    st.chat_input()


def controller():
    mode = sac.segmented(
        items=['Показатели', 'Аналитика', 'Обращения','Переписка', 'Анализы'],
        index=0,
        format_func='title',
        align='center',
        direction='horizontal',
        radius='lg',
        return_index=False,
        use_container_width=True
    )
    match(mode):
        case 'Показатели':
            current_date = datetime.datetime.now()
            email = st.session_state['email']
            date = st.date_input("Выберите дату", max_value=current_date)
            show_data(email, date)
        case 'Аналитика':
            pass
        case 'Обращения':
            pass
        case 'Переписка':
            chat_with_client()
        case  'Анализы':
            pass


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



if __name__=='__main__':
    user_language = loader.language
    load_resourses(
        file_style="resources/style/style.css",
        file_localization=f"resources/ui/localization/localization_{user_language}.json",
        file_images="resources/ui/image.json")
    init()