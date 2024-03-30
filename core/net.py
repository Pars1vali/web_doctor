from core import user
import streamlit as st
import json, requests, os

# url = os.getenv('SERVER_PATH')
url = "https://d5dam91qvmi3s9e5ngo8.apigw.yandexcloud.net/authentication"
url_fit = "https://d5d3s1crlakbffikg0bu.apigw.yandexcloud.net/collect-fit-data"
headers = {'Content-Type': 'application/json'}

class Client:
    global headers

    @staticmethod
    def login_account(email):
        headers['X-Custom-Info'] = 'login_client'
        data = {
            'email': email
        }
        response = requests.post(url, json.dumps(data), headers=headers)
        return response.text

    @staticmethod
    def create_account(client: user.Client):
        headers['X-Custom-Info'] = 'new_client'
        response = requests.post(url, client.toJSON(), headers=headers)
        return response.text

class Doctor:
    global headers
    @staticmethod
    def login_account(login, password):
        headers['X-Custom-Info'] = 'login_doctor'
        data = {
            'login': login,
            'password': password
        }
        data_json = json.dumps(data)

        response = requests.post(url, data_json, headers= headers)
        return response.text

    @staticmethod
    def create_account(doctor: user.Doctor):
        headers['X-Custom-Info'] = 'new_doctor'
        response = requests.post(url, doctor.toJSON(), headers=headers)
        return response.text

    @staticmethod
    def get_client(id):
        headers['X-Custom-Info'] = 'get_client'
        data ={
            "id": id
        }
        response = requests.post(url, json.dumps(data), headers=headers)
        return response.text

    @staticmethod
    @st.cache_resource
    def get_client_data(email, date):
        headers['X-Custom-Info'] = 'DATA_COLLECT'
        data = {
            "email": email,
            "date": date
        }
        response = requests.post(url_fit, json.dumps(data), headers=headers)
        return response.text