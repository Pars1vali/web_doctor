from core import user
import json, requests, os

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
        response = requests.post(url=Client.url, data= user.toJSON(), headers=Client.headers)
        return response.text

    @staticmethod
    def loginClientAccount(email):
        Client.headers['X-Custom-Info'] = 'login_client'
        data = {
            'email': email
        }
        response = requests.post(url=Client.url, data=json.dumps(data), headers=Client.headers)
        return response.text

    @staticmethod
    def createClientAccount(user: user.Client):
        pass
