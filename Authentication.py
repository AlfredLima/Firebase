import pyrebase
import urllib3
import requests
import json

config = {
    "apiKey": "AIzaSyBtqUQu14_YBqXOCrO5Rl8O6cpE-3mnPF0",
    "authDomain": "begin-3be7c.firebaseapp.com",
    "databaseURL": "https://begin-3be7c.firebaseio.com",
    "projectId": "begin-3be7c",
    "storageBucket": "begin-3be7c.appspot.com",
    "messagingSenderId": "38215806273"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

### Example with email and password
## With validation of email and password

while True:
    try:
        login, password = input().split(' ')
        user = auth.sign_in_with_email_and_password(login, password)
        break
    except requests.exceptions.HTTPError as e:
        print("Login errado")
        v = json.loads(e.strerror)
        print(v["error"]["message"])
    pass
