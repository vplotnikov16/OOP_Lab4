from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow

from rendering import Canvas
from ..layouts.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.canvas = Canvas(self.dockWidgetContents_paintBox)
        self.canvas.setObjectName("canvas")
        self.dockWidgetContents_paintBox.layout().addWidget(self.canvas)
        self.checkBox_intersectedSeletion.stateChanged.connect(self.checkBox_intersectedSeletion_stateChanged)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        key = event.key()
        if key == Qt.Key_Delete:
            self.canvas.clear()
        elif key == Qt.Key_Control:
            if self.checkBox_ctrlEnabled.isChecked():
                self.canvas.multiple_selection = True

    def keyReleaseEvent(self, event: QKeyEvent):
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key_Control:
            self.isCtrlPressed = False
            self.canvas.multiple_selection = False

    def checkBox_intersectedSeletion_stateChanged(self):
        self.canvas.select_all_intersected = self.checkBox_intersectedSeletion.isChecked()
