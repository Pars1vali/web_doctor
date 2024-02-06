import json
import requests



class Client:

    url = 'https://d5dam91qvmi3s9e5ngo8.apigw.yandexcloud.net/authentication'
    headers = {'Content-Type': 'application/json'}

    @staticmethod
    def authentication(login, password):
        data={
            'login': login,
            'password': password
        }
        data_json = json.dumps(data)

        response = requests.post(url=Client.url, data=data_json, headers=Client.headers)
        return response.text
