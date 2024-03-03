import json

path_style, path_images, path_ui_localization = None, None, None

@staticmethod
def set_resources(file_style, file_localization, file_images):
    global path_style, path_images, path_ui_localization
    path_style, path_images, path_ui_localization = file_style, file_images, file_localization

@staticmethod
def load_localization():
    global path_ui_localization
    with open(path_ui_localization, 'r', encoding='utf-8') as file:
        return json.load(file)

@staticmethod
def load_images():
    global path_images
    with open(path_images, 'r', encoding='utf-8') as file:
        return json.load(file)

@staticmethod
def load_styles():
    global path_style
    with open(path_style, encoding='utf-8') as f:
        return '<style>{}</style>'.format(f.read())


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
