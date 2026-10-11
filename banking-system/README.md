# Terminal Banking System

An educational, local Python banking simulator for practising classes, input
validation, `Decimal`, JSON persistence, and password hashing. It does not use
real bank accounts or exchange-rate services.

## Run

Use Python 3.10 or newer:

```powershell
cd D:\it_projects\soft-skills\banking-system
python main.py
```

No third-party packages are required. The app creates its data file at
`storage/storage.json` when the first user registers. An empty file is treated
as an empty database.

## Menu

1. Register with an email, name, and password, then log in.
2. Select **Update/Get Card** to create a card. A new card
   expires 1 year and 3 months after the current month.
3. Enter that card's 16-digit number for deposits, withdrawals, currency
   changes, transfers, history, and card details.
4. **Update/Get Card** can add another card or renew an expired card by its
   number for 1 year and 3 months from the current month. A card remains valid
   through its printed expiration month.
5. **Log Out** returns to the main menu; **Exit** closes the app.

The simulator supports UZS, USD, and EUR. Its fixed learning rates are
`1 USD = 11800 UZS` and `1 EUR = 13100 UZS`. Currency changes convert the
existing balance through UZS and round to two decimal places. Transfers require
both cards to use the same currency.

## Saved data

The JSON root is a dictionary. Each key is the SHA-256 hash of a normalized
email address; its value is a dictionary of the user's name, password hash and
salt, card lists, balances, currencies, and operation history. Passwords use
PBKDF2-HMAC-SHA256 with a new random salt for each user. Plaintext email and
password are not saved. Balances are stored as strings so decimal values stay
exact when JSON is read and written.

`models.py` contains `User` and `ATM` logic. `security.py` handles email and
password hashing. `storage.py` handles JSON. `service.py` connects these parts
to the terminal menu. `main.py` starts the program.

The existing `storage/storage.json` file is already tracked by Git. The
`.gitignore` entry prevents tracking only after the file is removed from the
Git index. Before committing real practice data, run
`git rm --cached banking-system/storage/storage.json` from the repository root;
the file stays on your computer.
