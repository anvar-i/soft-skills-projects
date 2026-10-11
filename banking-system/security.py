"""Email lookup and password verification for the local simulator."""

import hashlib
import hmac
import secrets


PASSWORD_ITERATIONS = 600_000


def normalize_email(email):
    """Return one stable email spelling for registration and login."""
    email = email.strip().lower()
    local, separator, domain = email.partition("@")
    if not separator or not local or not domain or "." not in domain:
        raise ValueError("Enter a valid email address, for example name@example.com.")
    if any(character.isspace() for character in email):
        raise ValueError("An email address cannot contain spaces.")
    return email


def email_key(email):
    """A deterministic key lets login find a record without storing the email."""
    normalized = normalize_email(email)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def hash_password(password):
    if not password:
        raise ValueError("Password cannot be empty.")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    return salt.hex(), digest.hex()


def verify_password(password, salt_hex, digest_hex):
    try:
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    return hmac.compare_digest(actual, expected)
