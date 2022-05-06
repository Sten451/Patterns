import hashlib
from components.source_data import salt


def salted_password(password):
    strong_password = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return strong_password

