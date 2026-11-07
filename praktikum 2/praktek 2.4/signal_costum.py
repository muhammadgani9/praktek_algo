
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject


# Custom signal class
class Communicator(QObject):
    message_sent = pyqtSignal(str, int)  # message, priority
    data_updated = pyqtSignal(dict)


# Sender Widget
class SenderWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sender")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Pesan...")

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])

        self.send_btn = QPushButton("Send Message")

        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Data value...")

        self.update_btn = QPushButton("Update Data")

        layout.addWidget(QLabel("Message System"))
        layout.addWidget(self.message_input)
        layout.addWidget(self.priority_combo)
        layout.addWidget(self.send_btn)

        layout.addWidget(QLabel("Data System"))
        layout.addWidget(self.data_input)
        layout.addWidget(self.update_btn)

        self.setLayout(layout)

        # Membuat communicator
        self.comm = Communicator()

        # Menghubungkan tombol
        self.send_btn.clicked.connect(self.send_message)
        self.update_btn.clicked.connect(self.send_data)

    def send_message(self):
        msg = self.message_input.text()

        priority = self.priority_combo.currentIndex() + 1

        if msg:
            self.comm.message_sent.emit(msg, priority)
            self.message_input.clear()

    def send_data(self):
        data = {
            "value": self.data_input.text(),
            "timestamp": "now"
        }

        self.comm.data_updated.emit(data)


# Receiver Widget
class ReceiverWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Receiver")
        self.setGeometry(450, 100, 350, 300)

        layout = QVBoxLayout()

        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)

        self.data_display = QLabel("No data received")

        layout.addWidget(QLabel("Received Messages:"))
        layout.addWidget(self.message_display)

        layout.addWidget(QLabel("Data Status:"))
        layout.addWidget(self.data_display)

        self.setLayout(layout)

    def connect_to_sender(self, sender):
        sender.comm.message_sent.connect(self.on_message)
        sender.comm.data_updated.connect(self.on_data)

    def on_message(self, message, priority):
        priority_text = {
            1: "Low",
            2: "Medium",
            3: "High"
        }

        self.message_display.append(
            f"[{priority_text[priority]}] {message}"
        )

    def on_data(self, data):
        self.data_display.setText(
            f"Data: {data['value']} at {data['timestamp']}"
        )


# Main Application
class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Signal Demo")
        self.setGeometry(100, 100, 800, 500)

        layout = QHBoxLayout()

        self.sender = SenderWidget()
        self.receiver = ReceiverWidget()

        # Menghubungkan Sender dengan Receiver
        self.receiver.connect_to_sender(self.sender)

        layout.addWidget(self.sender)
        layout.addWidget(self.receiver)

        self.setLayout(layout)


# Menjalankan aplikasi
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainApp()
    window.show()

    sys.exit(app.exec_())
