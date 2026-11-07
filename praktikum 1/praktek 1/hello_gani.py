import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

class HelloWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Pertama")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()
        label = QLabel("Hello, Gani!")
        label.setStyleSheet("font-size: 20px;color blue;")
        layout.addWidget(label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelloWindow()
    window.show()
    sys.exit(app.exec_())        