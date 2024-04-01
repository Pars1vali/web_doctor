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

    @staticmethod
    def get_id(doctor_id):
        headers['X-Custom-Info'] = 'get_client'
        data = {
            "id": doctor_id
        }
        response = requests.post(url, json.dumps(data), headers=headers)
        return response.text

    @staticmethod
    @st.cache_resource
    def get_data(email, date):
        headers['X-Custom-Info'] = 'DATA_COLLECT'
        data = {
            "email": email,
            "date": date
        }
        response = requests.post(url_fit, json.dumps(data), headers=headers)
        return response.text

    @staticmethod
    def get_appeal(client_id, date):
        headers['X-Custom-Info'] = 'APPEAL_GET'
        data = {
            "client_id": client_id,
            "date": date
        }
        response = requests.post(url_fit, json.dumps(data), headers=headers)
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
    def get_info(doctor_id):
        headers['X-Custom-Info'] = 'DOCTOR_DATA_COLLECT'
        data = {
            "doctor_id": doctor_id
        }
        response = requests.post(url, json.dumps(data), headers=headers)
        return response.text

    @staticmethod
    def send_appeal(image, topic, description, date, client_id):
        headers['X-Custom-Info'] = 'APPEAL_SEND'
        data = {
            "image": image,
            "topic": topic,
            "description": description,
            "date": date,
            "client_id": client_id
        }
        response = requests.post(url_fit, json.dumps(data), headers=headers)
        return response.text

