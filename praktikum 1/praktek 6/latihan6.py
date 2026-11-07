import sys
from PyQt5.QtWidgets import *

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Data")
        self.setModal(True)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nama")
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 100)
        self.age_input.setPrefix("Umur: ")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(QLabel("Masukkan Data Diri:"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(buttons)
        
        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text(), self.age_input.value()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo Dialog")
        self.setGeometry(300, 300, 300, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.btn_input = QPushButton("Input Data")
        self.btn_input.clicked.connect(self.show_input_dialog)

        self.label_info = QLabel("Belum ada data")

        layout.addWidget(self.btn_input)
        layout.addWidget(self.label_info)

    def show_input_dialog(self):
        dialog = InputDialog()
        if dialog.exec_() == QDialog.Accepted:
            name, age = dialog.get_data()
            self.label_info.setText(f"Nama: {name}, Umur: {age}")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Konfirmasi',
                        "Yakin ingin keluar?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())