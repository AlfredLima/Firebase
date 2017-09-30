import pyrebase
import urllib3
import requests
import json

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

auth = firebase.auth()

### Example with email and password
## With validation of email and password

while True:
    try:
        login, password = input().split(' ')
        user = auth.sign_in_with_email_and_password(login, password)
        print("Login com sucesso!")
    except requests.exceptions.HTTPError as e:
        print("Login errado")
        v = json.loads(e.strerror)
        print(v["error"]["message"])
    pass
