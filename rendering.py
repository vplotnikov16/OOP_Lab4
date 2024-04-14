from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPaintEvent, QPainter, QPen, QMouseEvent
from PyQt5.QtCore import Qt, QPoint


class CCircle:
    def __init__(self, center: tuple[int, int], radius: float):
        self.center = QPoint(center[0], center[1])
        self.radius = radius
        self.selected = False


def draw_circle(circle: CCircle, qp: QPainter):
    qp.setRenderHint(QPainter.Antialiasing)
    if circle.selected:
        pen = QPen(Qt.gray, 3, Qt.DashLine)
    else:
        pen = QPen(Qt.darkGray, 3, Qt.SolidLine)
    qp.setPen(pen)
    qp.drawEllipse(circle.center, circle.radius, circle.radius)


class Canvas(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super(Canvas, self).__init__(parent=parent)
        self.circle_container = []

    def add_circle(self, event: QMouseEvent):
        circle = CCircle(center=(event.x(), event.y()), radius=40)
        self.circle_container.append(circle)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        self.render_circles()

    def render_circles(self):
        qp = QPainter(self)
        for circle in self.circle_container:
            draw_circle(circle, qp)

    def mousePressEvent(self, event: QMouseEvent):
        self.add_circle(event)
        self.update()
