import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
 # ← Import loadUi

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI langsung dari file .ui
        loadUi('log.ui', self) # ← Load langsung, tidak perlu konversi

        # Hubungkan signal dengan slot
        self.btnLogin.clicked.connect(self.handle_login)
        self.btnClear.clicked.connect(self.clear_form)
        # Set focus
        self.txtUsername.setFocus()

    def handle_login(self):
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text()

        if username == "admin" and password == "123":
            QMessageBox.information(self, "Login Sukses", f"Selamat datang Admin!")
            self.labelStatus.setText("✓ Login berhasil!")
            self.labelStatus.setStyleSheet("color: green; font-weight: bold;")

        else:
            QMessageBox.warning(self, "Login Gagal", "Username atau password salah!")
            self.labelStatus.setText("✗ Username atau password salah!")
            self.labelStatus.setStyleSheet("color: red; font-weight: bold;")
            self.txtPassword.clear()
            self.txtPassword.setFocus()

    def clear_form(self):
        self.txtUsername.clear()
        self.txtPassword.clear()
        self.labelStatus.clear()
        self.txtUsername.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())