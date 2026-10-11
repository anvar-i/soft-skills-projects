"""Banking workflows and the terminal menu."""

import getpass
import secrets

from models import ATM, User
from security import email_key, hash_password, verify_password
from storage import JsonStorage, StorageError


class BankingService:
    def __init__(self, storage=None):
        self.storage = storage or JsonStorage()

    def register(self, email, username, password):
        key = email_key(email)
        username = username.strip()
        if not username:
            raise ValueError("Name cannot be empty.")
        users = self.storage.load()
        if key in users:
            raise ValueError("This email is already registered.")
        salt, digest = hash_password(password)
        users[key] = User(username, digest, salt).to_dict()
        self.storage.save(users)
        return key

    def login(self, email, password):
        key = email_key(email)
        record = self.storage.load().get(key)
        if record is None:
            raise ValueError("Incorrect email or password.")
        user = User.from_dict(record)
        if not verify_password(password, user.password_salt, user.password_hash):
            raise ValueError("Incorrect email or password.")
        return key

    def _user_and_data(self, key):
        data = self.storage.load()
        if key not in data:
            raise ValueError("Account was not found. Log in again.")
        return User.from_dict(data[key]), data

    def get_user(self, key):
        user, _ = self._user_and_data(key)
        return user

    def _save_user(self, key, user, data):
        data[key] = user.to_dict()
        self.storage.save(data)

    def create_card(self, key, currency):
        user, data = self._user_and_data(key)
        existing = {
            number for record in data.values()
            for number in record.get("card_number", [])
        }
        number = ""
        while not number or number in existing:
            number = f"{secrets.randbelow(10**16):016d}"
        ATM(user).create_card(number, currency)
        self._save_user(key, user, data)
        return ATM(user).showData(number), number

    def update_card(self, key, number):
        user, data = self._user_and_data(key)
        expiration = ATM(user).updateCard(number)
        self._save_user(key, user, data)
        return expiration

    def deposit(self, key, number, amount):
        user, data = self._user_and_data(key)
        balance = ATM(user).deposit(number, amount)
        self._save_user(key, user, data)
        return balance

    def withdraw(self, key, number, amount):
        user, data = self._user_and_data(key)
        balance = ATM(user).withdraw(number, amount)
        self._save_user(key, user, data)
        return balance

    def change_currency(self, key, number, currency):
        user, data = self._user_and_data(key)
        balance = ATM(user).changeCurrency(number, currency)
        self._save_user(key, user, data)
        return balance

    def recipient_info(self, number):
        data = self.storage.load()
        for record in data.values():
            user = User.from_dict(record)
            if number in user.card_number:
                return ATM(user).showData(number)
        raise ValueError("Recipient card was not found.")

    def transfer(self, key, source_number, recipient_number, amount):
        sender, data = self._user_and_data(key)
        recipient_key = None
        recipient = None
        for candidate_key, record in data.items():
            if recipient_number in record.get("card_number", []):
                recipient_key = candidate_key
                recipient = sender if candidate_key == key else User.from_dict(record)
                break
        if recipient is None:
            raise ValueError("Recipient card was not found.")
        balance = ATM(sender).transfer(source_number, recipient, recipient_number, amount)
        data[key] = sender.to_dict()
        data[recipient_key] = recipient.to_dict()
        self.storage.save(data)
        return balance

    def card_data(self, key, number):
        return ATM(self.get_user(key)).showData(number)

    def history(self, key, number):
        return ATM(self.get_user(key)).showHistory(number)


def ask_number(prompt, allowed):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and int(answer) in allowed:
            return int(answer)
        print(f"Choose one of: {', '.join(str(item) for item in sorted(allowed))}.")


def ask_card_number(prompt="Card number: "):
    number = input(prompt).strip()
    if not number.isdigit() or len(number) != 16:
        raise ValueError("Enter a 16-digit card number.")
    return number


def print_card(card):
    print(f"Holder: {card['holder']}")
    print(f"Card: {card['card']}")
    print(f"Expires: {card['expires']}")
    print(f"Balance: {card['balance']} {card['currency']}")


def account_menu(service, key):
    while True:
        print("\n0. Deposit  1. Withdraw  2. Change Currency  3. Transfer")
        print("4. Update/Get Card  5. Show History  6. Show Data  7. Log Out")
        choice = ask_number("Choose: ", set(range(8)))
        if choice == 7:
            print("Logged out.")
            return
        try:
            if choice == 4:
                has_cards = bool(service.get_user(key).card_number)
                selection = (input("Card number to renew, or NEW for another card: ").strip()
                             if has_cards else "new")
                if selection.lower() == "new":
                    currency = input("New card currency (UZS/USD/EUR): ").strip().upper()
                    card, number = service.create_card(key, currency)
                    print(f"New card number: {number}. Keep this number for future operations.")
                    print_card(card)
                else:
                    if not selection.isdigit() or len(selection) != 16:
                        raise ValueError("Enter a 16-digit card number or NEW.")
                    expiration = service.update_card(key, selection)
                    print(f"Card renewed. Valid through {expiration}.")
                continue

            number = ask_card_number()
            if choice == 0:
                balance = service.deposit(key, number, input("Amount: "))
                print(f"Deposit complete. Balance: {balance}")
            elif choice == 1:
                balance = service.withdraw(key, number, input("Amount: "))
                print(f"Withdrawal complete. Balance: {balance}")
            elif choice == 2:
                print("Currency table: 1 USD = 11800 UZS; 1 EUR = 13100 UZS.")
                currency = input("New currency (UZS/USD/EUR): ").strip().upper()
                balance = service.change_currency(key, number, currency)
                print(f"Currency changed. Balance: {balance} {currency}")
            elif choice == 3:
                target = ask_card_number("Recipient card number: ")
                amount = input("Amount: ")
                recipient = service.recipient_info(target)
                print(f"Recipient: {recipient['holder']}, {recipient['card']}")
                if input("Confirm transfer (yes/no): ").strip().lower() == "yes":
                    balance = service.transfer(key, number, target, amount)
                    print(f"Transfer complete. Balance: {balance}")
                else:
                    print("Transfer cancelled.")
            elif choice == 5:
                entries = service.history(key, number)
                if not entries:
                    print("No operations for this card yet.")
                for entry in entries:
                    print(f"{entry['time']} | {entry['action']} | "
                          f"{entry['amount']} {entry['currency']} | {entry['details']}")
            elif choice == 6:
                print_card(service.card_data(key, number))
        except (ValueError, StorageError) as error:
            print(f"Error: {error}")


def run_cli():
    service = BankingService()
    print("Welcome to the educational Banking System!")
    while True:
        print("\n0. Register  1. Log In  2. Exit")
        try:
            choice = ask_number("Choose: ", {0, 1, 2})
            if choice == 2:
                print("Thank you for using our system!")
                return
            email = input("Email: ")
            password = getpass.getpass("Password: ")
            if choice == 0:
                username = input("Name: ")
                service.register(email, username, password)
                print("Registration complete. You can now log in.")
            else:
                key = service.login(email, password)
                print(f"Welcome, {service.get_user(key).username}!")
                account_menu(service, key)
        except (ValueError, StorageError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
