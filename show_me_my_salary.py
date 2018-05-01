import hashlib
import sys

from os import path
from utils import get_parsed_data, get_encrypted, get_decrypted


file_path = sys.argv[1]
password = sys.argv[2]

with open(file_path, encoding='utf-8') as f:
    data = ''.join(f.readlines())
    title, data = get_parsed_data(data)
    iv, salt, encrypted = get_encrypted(data)

decrypted = get_decrypted(encrypted, iv, salt, password)

dir_path, file_name = path.split(file_path)
basename, ext = path.splitext(file_name)
new_file_name = title + ext
new_file_path = path.join(dir_path, new_file_name)

with open(new_file_path, 'w', encoding='utf-8') as f:
    f.write(decrypted)

