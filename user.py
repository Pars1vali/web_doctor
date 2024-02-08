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


