import json, requests, os
from core import user


class Client:

    url = os.getenv('SERVER_PATH')
    headers = {'Content-Type': 'application/json'}

    @staticmethod
    def loginPersonalAccount(login, password):
        Client.headers['X-Custom-Info'] = 'login_user'
        data={
            'login': login,
            'password': password
        }
        data_json = json.dumps(data)

        response = requests.post(url=Client.url, data=data_json, headers=Client.headers)
        return response.text

    @staticmethod
    def createPersonalAccount(user: user.Doctor):
        Client.headers['X-Custom-Info'] = 'new_user'
        response = requests.post(url=Client.url, data= user.toJSON(), headers=Client.headers )
        return  response.text

