import os
import sys
import shutil
import pdfkit

from PySide2.QtWidgets import (QApplication, QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog)
from converter import decrypt_html, convert_html, convert_pdf


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.filename = ''

        self.open_button = QPushButton("open")
        self.open_button.clicked.connect(self.open_dialog)

        payroll_title = QLabel("selected file :")
        self.payroll_filename = QLabel("Nothing")

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("enter your password")

        self.pdf_check = QCheckBox("pdf convert")

        self.decrypt_button = QPushButton("decrypt")
        self.decrypt_button.clicked.connect(self.decrypt)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(payroll_title)
        hbox_layout.addWidget(self.payroll_filename)

        output_title = QLabel("output dir :")
        self.output_directory = QLabel(os.getenv("HOME"))
        self.output_button = QPushButton("select")
        self.output_button.clicked.connect(self.select_output_directory)

        output_layout = QHBoxLayout()
        output_layout.addWidget(output_title)
        output_layout.addWidget(self.output_directory)
        output_layout.addWidget(self.output_button)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.open_button)
        vbox_layout.addLayout(hbox_layout)
        vbox_layout.addWidget(self.password_edit)
        vbox_layout.addLayout(output_layout)
        vbox_layout.addWidget(self.pdf_check)
        vbox_layout.addWidget(self.decrypt_button)

        self.setLayout(vbox_layout)

    def open_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)

        if dialog.exec_():
            selected_list = dialog.selectedFiles()
            self.filename = next(iter(selected_list))
            self.payroll_filename.setText(os.path.basename(self.filename))
            print(selected_list)

    def select_output_directory(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)

        if dialog.exec_():
            selected_list = dialog.selectedFiles()
            directory = next(iter(selected_list))
            # print(f"selected dir : {directory}")
            self.output_directory.setText(directory)

    def decrypt(self):
        try:
            title, decrypted_html = decrypt_html(self.filename, self.password_edit.text())
        except UnicodeDecodeError as e:
            show_message(e)
            return

        title = title.replace(' ', '_')
        output_path = self.output_directory.text()

        if self.pdf_check.isChecked():
            new_file_name = f"{output_path}/{title}.pdf"

            print("filename : " + new_file_name)
            path_wkhtmltopdf = shutil.which('wkhtmltopdf')
            if not path_wkhtmltopdf:
                show_message(f"not found wkhtmltopdf.\ninstall wkhtmltopdf : https://wkhtmltopdf.org/downloads.html")
                return

            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            try:
                result = convert_pdf(decrypted_html, new_file_name, config=config)
            except IOError as e:
                show_message(e)
                return

            if result:
                print("pdf converted")
                self.show_converted_dialog('pdf')
        else:
            basename, ext = os.path.splitext(self.filename)
            new_file_name = f"{output_path}/{title}{ext}"
            convert_html(decrypted_html, new_file_name)
            self.show_converted_dialog('html')

    @staticmethod
    def show_converted_dialog(target):
        msg_box = QMessageBox()
        msg_box.setText(f"{target} successfully converted!")
        if msg_box.exec_():
            pass


def show_message(message):
    msg_box = QMessageBox()
    msg_box.setText(f"{message}")
    msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()

    os.environ["PATH"] += os.pathsep + '/usr/local/bin'

    sys.exit(app.exec_())
