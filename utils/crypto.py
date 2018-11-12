import hashlib
from .rc2 import *


def get_decrypted(encrypted, iv, salt, password):
    encoded_password = password.encode('utf-16LE')

    key = hashlib.sha1(encoded_password + salt).digest()
    key = key[:16]

    rc2 = RC2(key)
    decrypted = rc2.decrypt(encrypted, MODE_CBC, IV=iv)
    try:
        decrypted = decrypted.decode('utf-16LE')
    except UnicodeDecodeError as e:
        print(f'decode failed. check your password : {password}')
        raise e

    return decrypted
