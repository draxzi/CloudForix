import base64
import hashlib
from cryptography.fernet import Fernet
import getpass

def generate_key_from_password(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def load_key():
    password = getpass.getpass("Enter Investigator Password: ")
    key = generate_key_from_password(password)
    return Fernet(key)