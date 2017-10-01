import pyrebase
import urllib3
import requests
import json

### Example with email and password
## With validation of email and password

class Authentication():
    def __init__(self):
        try:
            fileKeys = open("key.txt", 'r')
        except FileNotFoundError as e:
            print("Arquivo não encontrado!")
            quit()
        except "IOError" as e:
            print("Arquivo corrompido!")
            quit()

        keys = fileKeys.read()
        config = json.loads(keys)
        firebase = pyrebase.initialize_app(config)
        self.auth = firebase.auth()
        self.database = firebase.database()

    def login(self, nick, password):
        try:
            user = self.auth.sign_in_with_email_and_password(nick, password)
            print("Login com sucesso!")
            return user
        except requests.exceptions.HTTPError as e:
            v = json.loads(e.strerror)
            print("Login errado:" , v["error"]["message"])
            return None

    def createUser(self,email,password):
        self.auth.create_user_with_email_and_password(email, password)
