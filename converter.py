import pdfkit

from utils import get_parsed_data, get_encrypted, get_decrypted


def convert_html(decrypted_html, new_html_file):
    with open(new_html_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_html)

    print(f"'{new_html_file}' was created.")


def convert_pdf(decrypted_html, new_pdf_file, config=None):
    return pdfkit.from_string(decrypted_html, new_pdf_file, configuration=config)


def decrypt_html(file_path, password):
    with open(file_path, encoding='utf-8') as f:
        data = ''.join(f.readlines())
        title, data = get_parsed_data(data)
        iv, salt, encrypted = get_encrypted(data)

    try:
        decrypted = get_decrypted(encrypted, iv, salt, password)
    except UnicodeDecodeError as e:
        raise e

    return title, decrypted
