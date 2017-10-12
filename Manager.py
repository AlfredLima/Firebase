import pyrebase
import urllib3
import requests
import json

class Manager():

    # Init class
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
        self.admin = self.auth.sign_in_with_email_and_password(login,password)
        self.nicks = {}
        self.setDictionary()

    #####################################################################

    ## Authetication
    # Login method
    def login(self, nick, password):
        print("- Log in:")
        try:
            user = self.auth.sign_in_with_email_and_password(nick, password)
            print("* Log in with sucess!")
            return user, self.getNick(nick)
        except requests.exceptions.HTTPError as e:
            v = json.loads(e.strerror)
            print("* Log in with:" , v["error"]["message"], "!")
            return None, None

    # Create user method
    def createUser(self,email,password,name):
        print( "- Creating user: ")
        nicks = self.getNicks()
        if name in nicks:
            print( "* Has the nick!" )
            return
        try:
            self.auth.create_user_with_email_and_password(email, password)
            data = {"email": email}
            self.database.child("nicks").child(name).set(data, self.admin)
            self.nicks[email] = name
            print("* Create account with sucess!")
        except requests.exceptions.HTTPError as e:
            v = json.loads(e.strerror)
            print("* Create account with" , v["error"]["message"])
            return

    # Get all nicks method
    def getNicks(self):
        nicks = self.getDatabase("nicks", self.admin)
        return nicks.val()

    # Get nick method
    def getNick(self,email):
        return self.nicks[email]

    # Setting nicks in dictiory method
    def setDictionary(self):
        nicks = self.getDatabase("nicks", self.admin)
        for value in nicks.each():
            self.nicks[value.val()['email']] = value.key()

    #####################################################################

    ## Database
    # Push database method
    def pushDatabase(self, key, data, user):
        self.database.child(key).push(data, user['idToken'])

    # Update database method
    def updateDatabase(self, key, data, user):
        self.database.child(key).update(data, user['idToken'])

    # Set database method
    def updateDatabase(self, key, data, user):
        self.database.child(key).set(data, user['idToken'])

    # Get database method
    def getDatabase(self, key, user):
        return self.database.child(key).get(user['idToken'])

    # Test method
    def testDatabase(self, key, user):
        all_users = self.getDatabase(key,user)
        for user in all_users.each():
            print(user.key())
            print(user.val())
            
    #####################################################################
