import sys
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from form.main_form import Ui_MainWindow


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.configure()

    def configure(self):
        self.dateEditFrom.setDate(datetime.now())
        self.dateEditTo.setDate(datetime.now())
        self.dateEditFrom.dateChanged.connect(lambda e: self.dateEditTo.setMinimumDate(e))
        self.lineEditBrowse.mousePressEvent = lambda e: self.openFileDialog()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select sql file", "",
                                                  "All Files (*);;")
        if fileName:
            self.lineEditBrowse.setText(str(fileName))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainForm()
    ui.show()
    sys.exit(app.exec_())
