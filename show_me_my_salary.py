import click
import os
import platform
import subprocess

from os import path
from converter import decrypt_html, convert_html, convert_pdf


@click.command('salary')
@click.argument("filename")
@click.option('-p', '--password', prompt=True, help="password")
@click.option('-c', '--pdf', is_flag=True, default='y', prompt=True, help="convert to pdf")
def main(filename, password, pdf):
    title, decrypted_html = decrypt_html(filename, password)

    dir_path, file_name = path.split(filename)
    dir_abs_path = path.join(os.getcwd(), dir_path)
    basename, ext = path.splitext(file_name)

    title = title.replace(' ', '_')

    if pdf:
        click.echo("convert to pdf")
        new_file_name = path.join(dir_abs_path, title + '.pdf')
        convert_pdf(decrypted_html, new_file_name)
    else:
        click.echo("convert to html")
        new_file_name = path.join(dir_abs_path, title + ext)
        convert_html(decrypted_html, new_file_name)

    try:
        if platform.system().lower() == 'darwin':
            subprocess.call(['open', '--reveal', new_file_name])
        elif platform.system().lower() == 'windows':
            subprocess.Popen(r'explorer /select,' + new_file_name)
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
