"""User data and card operations. No terminal input happens in this file."""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


CENT = Decimal("0.01")
RATES_IN_UZS = {"UZS": Decimal("1"), "USD": Decimal("11800"), "EUR": Decimal("13100")}


def add_months(day, count):
    """Return the first day of the month `count` months after `day`."""
    month_number = day.year * 12 + day.month - 1 + count
    return date(month_number // 12, month_number % 12 + 1, 1)


def money(value):
    """Accept a positive amount with at most two decimal places."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid amount.") from None
    if not amount.is_finite() or amount <= 0:
        raise ValueError("Amount must be positive with at most two decimal places.")
    try:
        rounded = amount.quantize(CENT)
    except InvalidOperation:
        raise ValueError("Amount is too large.") from None
    if amount != rounded:
        raise ValueError("Amount must be positive with at most two decimal places.")
    return amount


class User:
    def __init__(self, username, password_hash, password_salt,
                 card_number=None, expires=None, balances=None,
                 currencies=None, history=None):
        self.username = username
        self.password_hash = password_hash
        self.password_salt = password_salt
        # Matching indexes in these four lists describe the same card.
        self.card_number = list(card_number or [])
        self.expires = list(expires or [])
        self.balances = [Decimal(str(value)) for value in (balances or [])]
        self.currencies = list(currencies or [])
        self.history = list(history or [])
        if len({len(self.card_number), len(self.expires), len(self.balances),
                len(self.currencies)}) != 1:
            raise ValueError("Saved card lists have different lengths.")

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "password_salt": self.password_salt,
            "card_number": self.card_number,
            "expires": self.expires,
            "balances": [str(value) for value in self.balances],
            "currencies": self.currencies,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, record):
        try:
            return cls(
                username=record["username"],
                password_hash=record["password_hash"],
                password_salt=record["password_salt"],
                card_number=record.get("card_number", []),
                expires=record.get("expires", []),
                balances=record.get("balances", []),
                currencies=record.get("currencies", []),
                history=record.get("history", []),
            )
        except (KeyError, TypeError, InvalidOperation) as error:
            raise ValueError("Saved user data has an invalid format.") from error

    def card_index(self, number):
        try:
            return self.card_number.index(number.strip())
        except ValueError:
            raise ValueError("Card number was not found in this account.") from None


class ATM:
    def __init__(self, user: User):
        self.user = user

    def _active_index(self, number, today=None):
        index = self.user.card_index(number)
        current_month = (today or date.today()).strftime("%Y-%m")
        if self.user.expires[index] < current_month:
            raise ValueError("This card has expired. Use Update/Get Card first.")
        return index

    def _record(self, action, number, amount, currency, details=""):
        self.user.history.append({
            "time": datetime.now().isoformat(timespec="seconds"),
            "action": action,
            "card_number": number,
            "amount": str(amount),
            "currency": currency,
            "details": details,
        })

    def create_card(self, number, currency, today=None):
        currency = currency.upper()
        if currency not in RATES_IN_UZS:
            raise ValueError("Choose UZS, USD, or EUR.")
        if not number.isdigit() or len(number) != 16:
            raise ValueError("Card number must contain 16 digits.")
        if number in self.user.card_number:
            raise ValueError("Card number already exists in this account.")
        self.user.card_number.append(number)
        self.user.expires.append(add_months(today or date.today(), 15).strftime("%Y-%m"))
        self.user.balances.append(Decimal("0.00"))
        self.user.currencies.append(currency)
        self._record("card_created", number, Decimal("0.00"), currency)

    def updateCard(self, number, today=None):
        index = self.user.card_index(number)
        current_month = (today or date.today()).strftime("%Y-%m")
        if self.user.expires[index] >= current_month:
            raise ValueError(f"Card is valid through {self.user.expires[index]}.")
        self.user.expires[index] = add_months(today or date.today(), 15).strftime("%Y-%m")
        self._record("card_renewed", number, Decimal("0.00"), self.user.currencies[index])
        return self.user.expires[index]

    def deposit(self, number, amount):
        index = self._active_index(number)
        amount = money(amount)
        self.user.balances[index] += amount
        self._record("deposit", number, amount, self.user.currencies[index])
        return self.user.balances[index]

    def withdraw(self, number, amount):
        index = self._active_index(number)
        amount = money(amount)
        if self.user.balances[index] < amount:
            raise ValueError("Insufficient balance.")
        self.user.balances[index] -= amount
        self._record("withdraw", number, amount, self.user.currencies[index])
        return self.user.balances[index]

    def changeCurrency(self, number, new_currency):
        index = self._active_index(number)
        old_currency = self.user.currencies[index]
        new_currency = new_currency.upper()
        if new_currency not in RATES_IN_UZS:
            raise ValueError("Choose UZS, USD, or EUR.")
        if new_currency == old_currency:
            raise ValueError("The card already uses that currency.")
        old_balance = self.user.balances[index]
        new_balance = (old_balance * RATES_IN_UZS[old_currency]
                       / RATES_IN_UZS[new_currency]).quantize(CENT, rounding=ROUND_HALF_UP)
        self.user.currencies[index] = new_currency
        self.user.balances[index] = new_balance
        self._record("currency_changed", number, new_balance, new_currency,
                     f"From {old_balance} {old_currency}")
        return new_balance

    def transfer(self, number, recipient, recipient_number, amount):
        source_index = self._active_index(number)
        target_index = ATM(recipient)._active_index(recipient_number)
        amount = money(amount)
        if recipient is self.user and number == recipient_number:
            raise ValueError("Choose a different recipient card.")
        if self.user.currencies[source_index] != recipient.currencies[target_index]:
            raise ValueError("Transfer requires cards with the same currency.")
        if self.user.balances[source_index] < amount:
            raise ValueError("Insufficient balance.")
        currency = self.user.currencies[source_index]
        self.user.balances[source_index] -= amount
        recipient.balances[target_index] += amount
        self._record("transfer_sent", number, amount, currency,
                     f"To card ending {recipient_number[-4:]}")
        ATM(recipient)._record("transfer_received", recipient_number, amount, currency,
                               f"From card ending {number[-4:]}")
        return self.user.balances[source_index]

    def showData(self, number):
        index = self.user.card_index(number)
        return {
            "holder": self.user.username,
            "card": f"{number[:4]} **** **** {number[-4:]}",
            "expires": self.user.expires[index],
            "balance": self.user.balances[index],
            "currency": self.user.currencies[index],
        }

    def showHistory(self, number):
        self.user.card_index(number)
        return [entry for entry in self.user.history if entry["card_number"] == number]
