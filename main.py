# ************************** man hinh loai 2 *************************
import os
import sys

import requests as requests
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolTip
from gui import Ui_MainWindow

_AppName_ = 'update'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.QMessageBox = QMessageBox
        self.uic.pushButton.clicked.connect(self.showtext)
        self.uic.pushButton_2.clicked.connect(self.run_app)
        self.uic.label_2.setText("Version: 1.0")
        self.uic.pushButton_2.hide()
        self.auto_check_update()

    def auto_check_update(self):
        version = self.uic.label_2.text()
        __version__ = version.split()[1]
        try:
            # -- Online Version File
            # -- Replace the url for your file online with the one below.
            response = requests.get(
                "https://raw.githubusercontent.com/kyoko9000/check_version/main/update_version.txt")
            data = response.text

            if float(data) > float(__version__):
                # show update button
                self.uic.pushButton_2.show()
                self.uic.pushButton_2.setToolTip(" New version available now "
                                                 "\n you can download and update")
                QToolTip.setFont(QFont('Times New Roman', 30))

                self.uic.label.setText(
                    f' {_AppName_} {__version__} needs to \n update to version {data}')

        except Exception as e:
            # print('The Error is here!')
            self.QMessageBox.information(self, 'Check Update', 'Unable to Check for Update, Error:' + str(e))

    def showtext(self):
        version = self.uic.label_2.text()
        __version__ = version.split()[1]
        try:
            # -- Online Version File
            # -- Replace the url for your file online with the one below.
            response = requests.get(
                "https://raw.githubusercontent.com/kyoko9000/check_version/main/update_version.txt")
            data = response.text

            if float(data) > float(__version__):
                # if your new version is active, it's show message "update available"
                self.QMessageBox.information(self, 'Check Update', 'Update Available!')

                # choose update or not update
                reply = QMessageBox()
                reply.setWindowTitle("Update Process")
                reply.setText(
                    f'{_AppName_} {__version__} needs to update to version {data}')
                reply.setStandardButtons(QMessageBox.StandardButton.Yes |
                                         QMessageBox.StandardButton.No)
                x = reply.exec()
                if x == QMessageBox.StandardButton.Yes:
                    self.run_app()
                elif x == QMessageBox.StandardButton.No:
                    pass
            else:
                # your version is not active
                self.QMessageBox.information(self, 'Check Update', 'No Updates are Available.')
        except Exception as e:
            # print('The Error is here!')
            self.QMessageBox.information(self, 'Check Update', 'Unable to Check for Update, Error:' + str(e))

    def run_app(self):
        try:
            path = os.getcwd()
            # print("open update app", path)
            os.startfile(path + f"/{_AppName_}.exe")
            self.close()

        except Exception as e:
            # print('The Error is here!')
            self.QMessageBox.information(self, 'Check Update', 'Unable to Check for Update, Error:' + str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
