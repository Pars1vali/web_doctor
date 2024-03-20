import json


class Doctor:
    def __init__(self, firstname, lastname, surname, post, organization, phone_number, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.post = post
        self.organization = organization
        self.phone_number = phone_number
        self.username = username
        self.email = email
        self.password = password

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)



class Client:
    def __init__(self, firstname, lastname, surname, phone_number, doctor_id, email, refresh_token):
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.phone_number = phone_number
        self.doctor_id = doctor_id
        self.email = email
        self.refresh_token = refresh_token

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


