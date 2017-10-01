import pyrebase
import urllib3
import requests
import json
import Authentication
### Example with email and password
## With validation of email and password

class Database():
    def __init__(self):
        self.manager = Authentication.Authentication()

    def pushDatabase(self, key, data, user):
        self.manager.database.child(key).push(data, user)

    def testDatabase(self, key, user):
        all_users = self.manager.database.child(key).get(user)
        for user in all_users.each():
            print(user.key()) # Morty
            print(user.val()) # {name": "Mortimer 'Morty' Smith"}

    def getDatabase(self, key, user):
        print( self.manager.database.get(key, user) )

database = Database()

login, password = input().split()
user = database.manager.login(login,password)

database.testDatabase("agents", user['idToken'])
