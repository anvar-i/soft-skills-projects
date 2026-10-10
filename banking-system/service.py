from models import ATM, User
from security import HASH, verify
from storage import readStorage, file

component = "\n------------------------------\n"

def Register():
    mail = input("Enter you email:\n>> ")
    mail = verify(mail)

    hashed_mail = HASH(mail)

    if not file.exists(): return "No json storage found!"

    if readStorage(hashed_mail):
        print("This email is already registered.\nPlease, use 'Log In' operation, or try another email!" + component)
        return

    name = input("Enter Name: ")
    surname = input("Enter Surname: ")
    username = name + surname

    temp = input("Enter password: ")
    password = HASH(temp)

    user = User(hashed_mail= hashed_mail, username=username , password=password, mail = mail)

    print("User registered successefully!\nYou may now login to your account!" + component)

# Log In with existing User Account ( working ...)
def LogIn():
    pass


def leave():
    pass


"""
Finished: Register()

Working: 

Not Finished: leave(), LogIn()
"""