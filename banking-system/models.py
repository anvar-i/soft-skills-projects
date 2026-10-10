# User class that stores information if user (cards, username, ...)
class User:
    def __init__(self, mail, username, password, hashed_mail):
        self.username = username
        self.password= password
        self.mail = mail
        self.hashed_mail = hashed_mail
        self.salt = None

        self.expires = []
        self.card_number = []
        self.balances = []
        self.currencies = []

    def cardDetails():
        # show card numbers with covered middle numbers (123* **** **** *456, and card Holder username)
        pass

    def dump(): 
        # stores a dict form of user to json file
        pass

    def load():
        # retrieves a dict form of user from json file
        pass


# Class ATM manipulates data from User class(deposit, withdraw, ...). Operations are true, if card number is not expired(except updateCard, showData, showHistory)
class ATM:  
    def withdraw():     
        # withdraw money (if enough money). choose card from card_number from User object
        pass

    def deposit():
        # deposit money. ask additional clarification question about true card holder( username, card_number, currency)
        pass

    def changeCurrency():
        # change currency with currencyTable of card
        pass

    def transfer():
        # search database users with another card number to transfer. Show attention message, username and card number of reciever.
        # invalid if currency of cards differ
        pass

    def updateCard():
        pass

    def showData():
        pass

    def showExData():
        pass

    def showHistory():
        pass


"""
Completed: file

Working:

Not Finished: User, ATM, 
"""