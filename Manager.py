import pyrebase
import urllib3
import requests
import json

### Example with email and password
## With validation of email and password

class Manager():
    def __init__(self):

        try:
            fileKeys = open("key.txt", 'r')
        except FileNotFoundError as e:
            print("Arquivo não encontrado!")
            quit()
        except "IOError" as e:
            print("Arquivo corrompido!")
            quit()

        try:
            adminKeys = open("admin.txt", 'r')
        except FileNotFoundError as e:
            print("Arquivo não encontrado!")
            quit()
        except "IOError" as e:
            print("Arquivo corrompido!")
            quit()

        login , password = adminKeys.read().split()
        keys = fileKeys.read()
        config = json.loads(keys)
        firebase = pyrebase.initialize_app(config)
        self.auth = firebase.auth()
        self.database = firebase.database()
        self.storage = firebase.storage()
        self.admin = self.login(login,password)

    def login(self, nick, password):
        print("- Log in:")
        try:
            user = self.auth.sign_in_with_email_and_password(nick, password)
            print("* Log in with sucess!")
            return user
        except requests.exceptions.HTTPError as e:
            v = json.loads(e.strerror)
            print("* Log in with:" , v["error"]["message"], "!")
            return None

    def createUser(self,email,password,name):
        print( "- Creating user: ")
        nicks = self.getNicks()
        if name in nicks:
            print( "* Has the nick!" )
            return
        try:
            self.auth.create_user_with_email_and_password(email, password)
            data = {"email": email}
            self.database.child("nicks").child(name).set(data, self.admin['idToken'])
            print("* Create account with sucess!")
        except requests.exceptions.HTTPError as e:
            v = json.loads(e.strerror)
            print("* Create account with" , v["error"]["message"])
            return

    def pushDatabase(self, key, data, user):
        self.database.child(key).push(data, user)

    def testDatabase(self, key, user):
        all_users = self.database.child("").get(user)
        for user in all_users.each():
            print(user.key()) # Morty
            print(user.val()) # {name": "Mortimer 'Morty' Smith"}

    def getDatabase(self, key, user):
        return self.database.child(key).get(user)

    def getNicks(self):
        nicks = self.getDatabase("nicks", self.admin['idToken'])
        return nicks.val()
