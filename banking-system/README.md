# Terminal Banking System

An educational Python banking simulator for one local user. This is a small portfolio project for practising object-oriented programming, file handling, authentication, and automated tests. It runs through a terminal menu and uses only the Python standard library.

**Status:** planning stage. The application code has not been implemented yet. See [struct.md](struct.md) for the architecture and a step-by-step build and GitHub checklist.

## Planned features

- Register one local user and log in with a salted, hashed password.
- Create checking and savings accounts. The account types are labels; interest and fees are outside the project scope.
- Deposit, withdraw, and transfer money between the user's accounts.
- View transaction history and export it to CSV.
- Save users, accounts, balances, and transactions in a local JSON file.
- Reject invalid amounts, insufficient funds, and transfers to the same account.

## Design

The terminal menu will call a `BankingService` class. The service will apply banking rules to `User`, `Account`, and `Transaction` objects. A JSON storage class will load and save application state; a separate exporter will write transaction rows to CSV. Money will use `decimal.Decimal` in Python and strings in JSON to avoid floating-point rounding errors.

JSON will be the source of truth. CSV will be an export that can be regenerated from the saved transactions. Runtime files in `data/` and `exports/` will be ignored by Git.

## Planned project layout

```text
banking-system/
├── README.md
├── struct.md
├── .gitignore
├── main.py             # Terminal menu and input/output
├── models.py           # User, Account, Transaction
├── security.py         # Password hashing and verification
├── storage.py          # JSON loading and saving
├── service.py          # Banking operations and validation
├── export.py           # CSV transaction export
└── tests/              # Standard-library unittest tests
```

## How to run after implementation

From the `banking-system` directory, with Python 3 installed:

```powershell
py -3 main.py
```

Run the planned test suite with:

```powershell
py -3 -m unittest discover -s tests -v
```

On systems without the Windows `py` launcher, use `python` in the same commands. These commands are targets for the finished application; they will not work until the Python files are created.

## Learning goals

- Give each class a clear responsibility and keep terminal input outside the banking rules.
- Read and write JSON safely with Python's `json` module.
- Write CSV with the `csv` module, including a header row.
- Validate money with `Decimal` and test both successful and rejected operations.
- Use Git to make small, reviewable commits and publish the finished project to GitHub.

This is a learning simulator, not a real banking system. Use fictional data only.
