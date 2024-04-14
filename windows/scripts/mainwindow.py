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

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        key = event.key()
        if key == 16777223:  # del
            self.canvas.clear()
