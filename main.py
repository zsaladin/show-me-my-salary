import os
import sys

from PySide2.QtWidgets import (QApplication, QDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog)
from converter import decrypt_html, convert_html, convert_pdf


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.filename = ''

        self.open_button = QPushButton("open")
        self.open_button.clicked.connect(self.open_dialog)

        self.payroll_title = QLabel("selected file :")
        self.payroll_filename = QLabel("Nothing")

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("enter your password")

        self.pdf_check = QCheckBox("pdf convert")

        self.decrypt_button = QPushButton("decrypt")
        self.decrypt_button.clicked.connect(self.decrypt)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.payroll_title)
        hbox_layout.addWidget(self.payroll_filename)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.open_button)
        vbox_layout.addLayout(hbox_layout)
        vbox_layout.addWidget(self.password_edit)
        vbox_layout.addWidget(self.pdf_check)
        vbox_layout.addWidget(self.decrypt_button)

        self.setLayout(vbox_layout)

    def open_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)

        if dialog.exec_():
            filename_list = dialog.selectedFiles()
            self.filename = next(iter(filename_list))
            self.payroll_filename.setText(os.path.basename(self.filename))
            print(filename_list)

    def decrypt(self):
        title, decrypted_html = decrypt_html(self.filename, self.password_edit.text())

        if self.pdf_check.isChecked():
            new_file_name = title + '.pdf'
            if convert_pdf(decrypted_html, new_file_name):
                print("pdf converted")
                self.show_pdf_converted_dialog()
        else:
            basepath, ext = os.path.splitext(self.filename)
            new_file_name = title + ext
            convert_html(decrypted_html, new_file_name)

    @staticmethod
    def show_pdf_converted_dialog():
        msg_box = QMessageBox()
        msg_box.setText("pdf successfully converted!")
        if msg_box.exec_():
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()

    sys.exit(app.exec_())
