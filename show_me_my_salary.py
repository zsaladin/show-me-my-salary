import click
import platform
import subprocess
import pdfkit

from os import path
from utils import get_parsed_data, get_encrypted, get_decrypted


def convert_html(decrypted_html, new_html_file):
    with open(new_html_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_html)

    print(f"'{new_html_file}' was created.")


def convert_pdf(decrypted_html, new_pdf_file):
    pdfkit.from_string(decrypted_html, new_pdf_file)


def decrypt_html(file_path, password):
    with open(file_path, encoding='utf-8') as f:
        data = ''.join(f.readlines())
        title, data = get_parsed_data(data)
        iv, salt, encrypted = get_encrypted(data)

    decrypted = get_decrypted(encrypted, iv, salt, password)

    return title, decrypted


@click.command('salary')
@click.argument("filename")
@click.option('-p', '--password', prompt=True, help="password")
@click.option('-c', '--pdf', is_flag=True, default='y', prompt=True, help="convert to pdf")
def main(filename, password, pdf):
    title, decrypted_html = decrypt_html(filename, password)

    dir_path, file_name = path.split(filename)
    basename, ext = path.splitext(file_name)

    if pdf:
        click.echo("convert to pdf")
        new_file_name = title + '.pdf'
        convert_pdf(decrypted_html, new_file_name)
    else:
        click.echo("convert to html")
        new_file_name = title + ext
        convert_html(decrypted_html, new_file_name)

    new_file_path = path.join(dir_path, new_file_name)

    try:
        abs_file_path = path.abspath(new_file_path)

        if platform.system().lower() == 'darwin':
            subprocess.call(['open', '--reveal', abs_file_path])
        elif platform.system().lower() == 'windows':
            subprocess.Popen(r'explorer /select,' + abs_file_path)
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
