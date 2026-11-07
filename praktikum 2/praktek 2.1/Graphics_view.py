
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drawing App")
        self.setGeometry(300, 300, 800, 600)

        # Scene and View
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 500)

        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Toolbar
        toolbar = self.addToolBar("Tools")

        self.rect_btn = QAction("Rectangle", self)
        self.rect_btn.triggered.connect(self.add_rectangle)

        self.ellipse_btn = QAction("Ellipse", self)
        self.ellipse_btn.triggered.connect(self.add_ellipse)

        self.line_btn = QAction("Line", self)
        self.line_btn.triggered.connect(self.add_line)

        self.clear_btn = QAction("Clear", self)
        self.clear_btn.triggered.connect(self.clear_scene)

        toolbar.addAction(self.rect_btn)
        toolbar.addAction(self.ellipse_btn)
        toolbar.addAction(self.line_btn)
        toolbar.addAction(self.clear_btn)

        self.current_shape = None
        self.start_point = None

        # Mouse tracking
        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)

    def add_rectangle(self):
        self.current_shape = "rect"
        self.statusBar().showMessage(
            "Mode: Rectangle - Klik dan drag di canvas"
        )

    def add_ellipse(self):
        self.current_shape = "ellipse"
        self.statusBar().showMessage(
            "Mode: Ellipse - Klik dan drag di canvas"
        )

    def add_line(self):
        self.current_shape = "line"
        self.statusBar().showMessage(
            "Mode: Line - Klik dan drag di canvas"
        )

    def clear_scene(self):
        self.scene.clear()

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:
            self.start_point = self.view.mapToScene(event.pos())
            return True

        elif event.type() == event.MouseButtonRelease and self.start_point:
            end_point = self.view.mapToScene(event.pos())

            pen = QPen(Qt.black, 2)
            brush = QBrush(QColor(100, 150, 200, 100))

            if self.current_shape == "rect":
                rect = QRectF(self.start_point, end_point)
                self.scene.addRect(rect, pen, brush)

            elif self.current_shape == "ellipse":
                rect = QRectF(self.start_point, end_point)
                self.scene.addEllipse(rect, pen, brush)

            elif self.current_shape == "line":
                self.scene.addLine(
                    self.start_point.x(),
                    self.start_point.y(),
                    end_point.x(),
                    end_point.y(),
                    pen
                )

            self.start_point = None
            return True

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()
    sys.exit(app.exec_())
