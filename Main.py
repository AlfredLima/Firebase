import Manager

auth = Manager.Manager()
login, password = input().split()
print( login , password )
user = auth.login(login,password)
