class FitUnit:
    @staticmethod
    def get_data_unit(point_name, point_value):
        point_name_ru = "None"
        point_metric = "None"
        match point_name:
            case "calories":
                point_name_ru = "Калории"
                point_metric = "Ккал"
            case "distance":
                point_name_ru = "Дистанция"
                point_metric = "Метров"
            case "active_minutes":
                point_name_ru = "Время активности"
                point_metric = "Минут"
            case "activity":
                point_name_ru = "Баллы аквтиности"
                point_metric = "баллов"
            case "speed":
                point_name_ru = "Скорость"
                point_metric = "Метров в секунду"
            case "heart_minutes":
                point_name_ru = "Пульс"
                point_metric = "Ударов в минуту"
            case "step_count":
                point_name_ru = "Счетчик шагов"
                point_metric = "Шагов"

        return point_name_ru, point_value, point_metric