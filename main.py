# ************************** man hinh loai 2 *************************
import os
import sys
# # app1.py
# import certifi
# print(certifi.where())

import requests as requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui import Ui_MainWindow

_AppName_ = 'update'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.QMessageBox = QMessageBox
        self.uic.pushButton.clicked.connect(self.showtext)
        self.uic.label_2.setText("Version: 1.0")

    def showtext(self):
        version = self.uic.label_2.text()
        __version__ = version.split()[1]
        try:
            # -- Online Version File
            # -- Replace the url for your file online with the one below.
            response = requests.get("https://raw.githubusercontent.com/kyoko9000/check_version/main/update_version.txt")
            data = response.text
            # self.uic.label.setText(str(data))
            # print("data", data)

            if float(data) > float(__version__):
                # if your new version is active, it's show message "update available"
                self.QMessageBox.information(self, 'Check Update', 'Update Available!')

                # choose update or not update
                reply = QMessageBox()
                reply.setWindowTitle("Update Process")
                reply.setText(f'{_AppName_} {__version__} needs to update to version {data}')
                reply.setStandardButtons(QMessageBox.StandardButton.Yes |
                                         QMessageBox.StandardButton.No)
                x = reply.exec()
                if x == QMessageBox.StandardButton.Yes:
                    path = os.getcwd()
                    # print("open update app", path)
                    os.startfile(path + f"/{_AppName_}.exe")
                    self.close()
                elif x == QMessageBox.StandardButton.No:
                    pass
            else:
                # your version is not active
                self.QMessageBox.information(self, 'Check Update', 'No Updates are Available.')
        except Exception as e:
            # print('The Error is here!')
            self.QMessageBox.information(self, 'Check Update', 'Unable to Check for Update, Error:' + str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
