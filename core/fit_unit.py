import streamlit


class FitUnit:
    @staticmethod
    def get_data_unit(metric_name, metric_value):
        metric_name_ru = "None"
        metric_unit = "None"
        match metric_name:
            case "calories":
                metric_name_ru = "Калории"
                metric_unit = "Ккал"
            case "distance":
                metric_name_ru = "Дистанция"
                metric_unit = "Метров"
            case "active_minutes":
                metric_name_ru = "Время активности"
                metric_unit = "Минут"
            case "activity":
                metric_name_ru = "Баллы аквтиности"
                metric_unit = "баллов"
            case "speed":
                metric_name_ru = "Скорость"
                metric_unit = "Метров в секунду"
            case "heart_minutes":
                metric_name_ru = "Пульс"
                metric_unit = "Ударов в минуту"
            case "step_count":
                metric_name_ru = "Счетчик шагов"
                metric_unit = "Шагов"

        return metric_name_ru, metric_value, metric_unit


    @staticmethod
    def change_name_columns(columns):
        columns_new = list()

        for column in columns:
            columns_name = None
            match column:
                case "calories":
                    columns_name = "Калории"
                case "distance":
                    columns_name = "Дистанция"
                case "active_minutes":
                    columns_name = "Время активности"
                case "activity":
                    columns_name = "Баллы аквтиности"
                case "speed":
                    columns_name = "Скорость"
                case "heart_minutes":
                    columns_name = "Пульс"
                case "step_count":
                    columns_name = "Счетчик шагов"
            columns_new.append(columns_name)

        return columns_new