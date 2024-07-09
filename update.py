# ************************** man hinh loai 2 *************************
import os
import shutil
import sys
import zipfile

import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui1 import Ui_MainWindow

dest_dir = os.getcwd()
the_filepath = f"{dest_dir}/update/update_file.zip"
the_url = 'https://codeload.github.com/kyoko9000/update/zip/refs/heads/main'


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.downloadThread = None
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.progressBar.setValue(0)
        self.uic.pushButton.clicked.connect(self.process_update)
        self.Update_Lable("ready for update")

    # Download button event
    def process_update(self):
        # Create a download thread
        self.downloadThread = downloadThread()
        self.downloadThread.status_signal.connect(self.Update_Lable)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    def Update_Lable(self, signal):
        self.uic.label.setText(signal)

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
    status_signal = pyqtSignal(object)
    download_proess_signal = pyqtSignal(object)  # Create signal

    def __init__(self):
        super().__init__()
        self.fileobj = None
        self.filesize = None
        self.url = the_url

    def run(self):
        try:
            self.check_size()
            self.status_signal.emit("in process..")
            rsp = requests.get(self.url, stream=True)  # Streaming download mode
            offset = 0
            for chunk in rsp.iter_content(chunk_size=1024):
                if not chunk: break
                self.fileobj.seek(offset)  # Setting Pointer Position
                self.fileobj.write(chunk)  # write file
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))  # Sending signal
            #######################################################################
            self.fileobj.close()  # Close file
            self.exit(0)  # Close thread

        except:
            pass

    def check_size(self):
        try:
            self.status_signal.emit("start process..")
            self.filesize = requests.get(the_url, stream=True).headers['Content-Length']
            self.fileobj = open(the_filepath, 'wb')
        except:
            self.status_signal.emit("connecting...")
            self.check_size()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
