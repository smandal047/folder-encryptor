import sys
import time
import multiprocessing as mp

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QRadioButton, QLineEdit, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from main import FernetEncrypter
from logger import logger as logging

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle('Encryptor')
        self.setGeometry(700, 300, 500, 250)

        self.logger = logging()
        self.encode = True
        self.code_lvl = False
        self.path = ''
        self.status = 'Not Set'

        self.init_ui()

    def init_ui(self):
        self.add_text('Recursively encrypts and decrypts the given path', QFont("Times", 10, QFont.Bold), 10, 35, Qt.AlignCenter)
        self.add_path_textbox()
        self.add_radio_button()
        self.add_checkbox()
        self.add_button()
        self.log_text = self.add_text('--------Check logs--------', QFont("Times", 10, QFont.Bold), 275, 200, Qt.AlignCenter, hidden=True)

    def add_text(self, text, qfont, left, top, qalign, hidden=False):
        label1 = QLabel(text, self)
        label1.setFont(qfont)
        label1.move(left, top)  # left, top
        label1.setAlignment(qalign)
        label1.setHidden(hidden)
        return label1

    def add_path_textbox(self):
        self.add_text('Encrption Path', QFont("Times", 8, QFont.System), 35, 105, Qt.AlignRight)
        self.t1 = QLineEdit(self)
        self.t1.setToolTip('Sets the path for recurive encryption')
        self.t1.move(150, 100)

        self.t1.setEnabled(True)

    def add_radio_button(self):
        # add tooltip
        self.r1 = QRadioButton('Encryption', self)
        self.r2 = QRadioButton('Decryption', self)
        self.r1.setChecked(True)
        self.r1.move(70, 150)
        self.r2.move(170, 150)

        self.r1.toggled.connect(lambda: self.button_state(self.r1))
        self.r2.toggled.connect(lambda: self.button_state(self.r2))

    def add_checkbox(self):
        self.c1 = QCheckBox('Rename Only', self)
        self.c1.setToolTip('If unchecked, only the file name gets encrypted;\nIf checked, the whole file is encrypted, making it unreadable')
        self.c1.setChecked(True)
        self.c1.move(300, 150)
        self.c1.toggled.connect(lambda: self.button_state(self.c1)) 

    def add_button(self):
        # buttons
        self.button = QPushButton('Start Cryption', self)
        self.button.move(150, 200)
        self.button.clicked.connect(lambda: self.on_click())
    
    # ---------- GUI states handler ----------
    def button_state(self, b):
        # for debugging
        # if b.isChecked():
        #     print(b.text() + " is selected")
        # else:
        #     print(b.text() + " is deselected")

        # make a provision to delete the content of widgets
        if b.text() == 'Encryption':
            self.encode = True
        
        if b.text() == 'Decryption':
            self.encode = False

        if b.text() == 'Rename Only' and b.isChecked():
            self.code_lvl = False
        
        if b.text() == 'Rename Only' and not b.isChecked():
            self.code_lvl = True

        self.logger.info(f'Button state change: {b.text()} to {b.isChecked()}')

    def on_click(self):
        
        if self.button.text() == 'Start Cryption':
            self.button.setText("Kill Task")
            self.logger.info(f'Cryption Started, encryption:{self.encode}, codeLvl:{self.code_lvl} for path:{self.t1.text()}')
            self.path = r'{}'.format(self.t1.text())
            self.t1.setEnabled(False)
            self.r1.setEnabled(False)
            self.r2.setEnabled(False)
            self.c1.setEnabled(False)

            self.start_encrypt_process()

            self.button.setText("Done")
            self.on_click()

        elif self.button.text() == 'Done':
            self.button.setEnabled(False)

            Succ = self.status['success']
            Fail = self.status['fail']
            self.log_text.setText(f'Succ:{Succ},Fail:{Fail}')
            self.log_text.setHidden(False)
            self.logger.info(f'Cryption Successful')
        else:
            self.button.setText("Restart App")
            self.button.setEnabled(False)
            self.log_text.setHidden(False)
            self.logger.warning(f'Cryption Killed in between')

    def start_encrypt_process(self):
        # run is as separate thread which can be killed via application

        enc = FernetEncrypter('key.k')
        path = self.path
        
        self.status = enc.folder_cryptor(path, encode=self.encode, code_lvl=self.code_lvl)
        self.logger.info(f'Encryption successfull, Status:{self.status}')


# Main function to run the application
def main():
    app = QApplication(sys.argv)  # Create an application instance
    window = MyWindow()           # Create an instance of the window
    window.show()                 # Show the window
    sys.exit(app.exec_())         # Start the application's event loop

# Run the main function if this script is executed
if __name__ == '__main__':
    main()
