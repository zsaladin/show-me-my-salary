import hashlib
from .rc2 import *


def get_decrypted(encrypted, iv, salt, password):
    password = password.encode('utf-16LE')

    key = hashlib.sha1(password + salt).digest()
    key = key[:16]

    rc2 = RC2(key)
    decrypted = rc2.decrypt(encrypted, MODE_CBC, IV=iv)
    decrypted = decrypted.decode('utf-16LE')
    return decrypted
