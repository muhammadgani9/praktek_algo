
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Application")
        self.setGeometry(300, 300, 500, 400)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        label = QLabel("Welcome to the Main Application!")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 16))
        layout.addWidget(label)

        # Simulate loading some data
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.status_label = QLabel("Loading data...")
        layout.addWidget(self.status_label)

        self.load_timer = QTimer()
        self.load_timer.timeout.connect(self.load_data)

        self.load_counter = 0
        self.load_timer.start(50)

    def load_data(self):
        self.load_counter += 1

        self.progress.setValue(self.load_counter)

        if self.load_counter >= 100:
            self.load_timer.stop()
            self.status_label.setText(
                "Data loaded successfully!"
            )


def show_splash_and_start():
    app = QApplication(sys.argv)

    # Create splash screen
    splash_pixmap = QPixmap(400, 300)
    splash_pixmap.fill(Qt.white)

    splash = QSplashScreen(splash_pixmap)
    splash.show()

    splash.showMessage(
        "Initializing...",
        Qt.AlignCenter,
        Qt.black
    )

    # Simulate initialization
    for i in range(1, 6):
        time.sleep(0.3)

        splash.showMessage(
            f"Loading module {i}/5...",
            Qt.AlignCenter,
            Qt.black
        )

        app.processEvents()

    # Create main window
    main_window = MainApplication()

    splash.showMessage(
        "Starting application...",
        Qt.AlignCenter,
        Qt.black
    )

    time.sleep(0.5)

    splash.finish(main_window)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    show_splash_and_start()
