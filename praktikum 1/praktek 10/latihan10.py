
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal


class WorkerThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self, duration=5):
        super().__init__()
        self.duration = duration
        self.was_cancelled = False

    def run(self):
        self.was_cancelled = False

        for i in range(101):
            if self.isInterruptionRequested():
                self.was_cancelled = True
                break

            time.sleep(self.duration / 100)
            self.progress.emit(i)


class ProgressApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Progress Bar Demo")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        self.status_label = QLabel("Siap")

        self.start_btn = QPushButton("Mulai Proses")
        self.start_btn.clicked.connect(self.start_process)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_process)
        self.cancel_btn.setEnabled(False)

        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

        self.worker = None

    def start_process(self):
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress.setValue(0)
        self.status_label.setText("Memproses...")

        self.worker = WorkerThread(duration=3)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.process_finished)
        self.worker.start()

    def update_progress(self, value):
        self.progress.setValue(value)

    def process_finished(self):
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        if self.worker.was_cancelled:
            self.status_label.setText("Dibatalkan")
            self.progress.setValue(0)
        else:
            self.status_label.setText("Selesai!")
            QMessageBox.information(
                self, "Info", "Proses selesai!"
            )

    def cancel_process(self):
        if self.worker and self.worker.isRunning():
            self.status_label.setText("Membatalkan...")
            self.cancel_btn.setEnabled(False)
            self.worker.requestInterruption()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgressApp()
    window.show()
    sys.exit(app.exec_())
