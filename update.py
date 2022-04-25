# ************************** man hinh loai 2 *************************
import os
import shutil
import sys
import zipfile

import requests
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui1 import Ui_MainWindow

dest_dir = os.getcwd()
the_filepath = f"{dest_dir}/update/update_file.zip"
the_url = 'https://codeload.github.com/kyoko9000/update/zip/refs/heads/main'


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.progressBar.setValue(0)
        self.uic.pushButton.clicked.connect(self.process_update)
        self.Update_Lable("ready for update")

    # Download button event
    def process_update(self):
        try:
            self.Update_Lable("update process..")
            print(requests.get(the_url, stream=True).headers['Content-Length'])
            the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
            the_fileobj = open(the_filepath, 'wb')
            #### Create a download thread
            self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=1024)
            self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
            self.downloadThread.start()

        except:
            self.Update_Lable("connecting...")
            self.process_update()
            # self.update_if_fail()

    def Update_Lable(self, lable):
        self.uic.label.setText(lable)

    # def update_if_fail(self):
    #     with requests.get(the_url) as r:
    #         r.raise_for_status()
    #         with open(the_filepath, 'wb') as f:
    #             for chunk in r.iter_content(chunk_size=1024):
    #                 if chunk:  # filter out keep-alive new chunks
    #                     f.write(chunk)
    #     self.set_progressbar_value(100)

    # Setting progress bar
    def set_progressbar_value(self, value):
        self.uic.progressBar.setValue(value)
        if value == 100:
            # unzip files...................................
            with zipfile.ZipFile(the_filepath, 'r') as h:
                h.extractall()

            # copy file to folder...........................
            # path to source directory
            src_dir = 'update-main'
            # path to destination directory
            dest_dir = os.getcwd()
            # getting all the files in the source directory
            # files = os.listdir(src_dir)
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)

            # show message complete
            QMessageBox.information(self, "Tips", "Update success!")
            self.close()


##################################################################
# Download thread
##################################################################
class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)  # Create signal

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)  # Streaming download mode
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)  # Setting Pointer Position
                self.fileobj.write(chunk)  # write file
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))  # Sending signal
            #######################################################################
            self.fileobj.close()  # Close file
            self.exit(0)  # Close thread


        except Exception as e:
            # print(e)
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
