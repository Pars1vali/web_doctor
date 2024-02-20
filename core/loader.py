import json


@staticmethod
def load_localization(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        ui = json.load(file)
    return ui
@staticmethod
def load_images(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        ui_images = json.load(file)
    return ui_images