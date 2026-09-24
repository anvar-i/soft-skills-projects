# Terminal Banking System

Terminal Banking System is an educational Python application that simulates basic banking operations for one local user. It is designed to strengthen practical understanding of object-oriented programming, exception handling, file handling, authentication, and automated testing.

The user can register and log in, create checking and savings accounts, deposit and withdraw money, transfer money between accounts, and view transaction history. Application data is stored locally in JSON format, while passwords are protected with a salt and a password-hashing algorithm rather than being saved as plain text.

## Learning objectives

This project provides practice with:

- Designing classes with clear responsibilities
- Encapsulation, inheritance, and composition
- Creating and handling custom exceptions
- Reading, validating, and safely writing JSON files
- Hashing and verifying passwords
- Working safely with money using `decimal.Decimal`
- Separating terminal, business, domain, and storage logic
- Writing unit and integration tests

## Main features

- Local user registration and authentication
- Secure password hashing
- Checking and savings accounts
- Deposits and withdrawals
- Transfers between accounts
- Transaction history
- JSON data persistence
- Input validation
- Custom banking and storage exceptions
- Automated tests

> This application is a learning project and not a production banking system. It must not be used to store real financial information or real passwords.