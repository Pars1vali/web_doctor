import json, streamlit as st

path_style, path_images, path_ui_localization = None, None, None
language = "ru"

# @st.cache_resource
def set_resources(file_style, file_localization, file_images):
    global path_style, path_images, path_ui_localization
    path_style, path_images, path_ui_localization = file_style, file_images, file_localization

# @st.cache_resource
def load_localization():
    global path_ui_localization
    with open(path_ui_localization, 'r', encoding='utf-8') as file:
        return json.load(file)
# @st.cache_resource
def load_images():
    global path_images
    with open(path_images, 'r', encoding='utf-8') as file:
        return json.load(file)
# @st.cache_resource
def load_styles():
    global path_style
    with open(path_style, encoding='utf-8') as f:
        return '<style>{}</style>'.format(f.read())


@staticmethod
def set_language(language_set):
    global language
    language_code = language
    match(language_set):
        case "Русский":
            language_code = "ru"
        case "English":
            language_code = "en"
        case "中國人":
            language_code = "ch"

    language = language_code

# @staticmethod
# def get_localization():
#     global path_ui_localization
#     with open(path_ui_localization, 'r', encoding='utf-8') as file:
#         ui = json.load(file)
#     return ui
# @staticmethod
# def get_images():
#     global path_images
#     with open(path_images, 'r', encoding='utf-8') as file:
#         ui_images = json.load(file)
#     return ui_images
#
# @staticmethod
# def set_style(file_name):
#     global path_style
#     path_style = file_name
