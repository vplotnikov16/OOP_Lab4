from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPaintEvent, QPainter, QPen, QMouseEvent, QKeyEvent
from PyQt5.QtCore import Qt, QPoint


class CCircle:
    def __init__(self, center: QPoint, radius: float):
        self.center = center
        self.radius = radius
        self.selected = False

    def is_point_inside(self, point: QPoint) -> bool:
        return self.squared_dist_to(point) <= self.radius ** 2

    def squared_dist_to(self, point: QPoint) -> int:
        return (point.x() - self.center.x()) ** 2 + (point.y() - self.center.y()) ** 2

    def draw(self, qp: QPainter):
        qp.setRenderHint(QPainter.Antialiasing)
        if self.selected:
            pen = QPen(Qt.gray, 3, Qt.DashLine)
        else:
            pen = QPen(Qt.darkGray, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawEllipse(self.center, self.radius, self.radius)


class Canvas(QWidget):
    multiple_selection = False
    select_all_intersected = False

    def __init__(self, parent: QWidget | None = None):
        super(Canvas, self).__init__(parent=parent)
        self.circle_container: list[CCircle] = []

    def add_circle(self, event: QMouseEvent):
        circle = CCircle(center=event.pos(), radius=40)
        if not self.circle_container:
            circle.selected = True
        self.circle_container.append(circle)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        self.render_circles()

    def render_circles(self):
        qp = QPainter(self)
        for circle in self.circle_container:
            circle.draw(qp)

    def clear(self):
        self.circle_container.clear()
        self.update()

    def intersections(self, point: QPoint) -> list[CCircle]:
        result = []
        for circle in self.circle_container:
            if circle.is_point_inside(point):
                result.append(circle)
        return result

    def mousePressEvent(self, event: QMouseEvent):
        intersections = self.intersections(event.pos())
        new_selected_circles = []
        if intersections:
            if self.select_all_intersected:
                for circle in intersections:
                    circle.selected = True
                    new_selected_circles.append(circle)
            else:
                nearest_circle = intersections.pop()
                while intersections:
                    current_circle = intersections.pop()
                    if current_circle.squared_dist_to(event.pos()) < nearest_circle.squared_dist_to(event.pos()):
                        nearest_circle = current_circle
                nearest_circle.selected = True
                new_selected_circles.append(nearest_circle)
            if not self.multiple_selection:
                for circle in self.circle_container:
                    if circle not in new_selected_circles:
                        circle.selected = False
        else:
            self.add_circle(event)
        self.update()
