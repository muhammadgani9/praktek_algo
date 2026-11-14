
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt


class ContactApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contact Manager")
        self.setGeometry(300, 300, 600, 400)

        # Setup database
        self.init_db()

        # Setup UI
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Table view
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("contacts")
        self.model.select()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(
            QTableView.SelectRows
        )

        # Form input
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        form_layout.addRow("Nama:", self.name_input)
        form_layout.addRow("Telepon:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)

        # Buttons
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Tambah")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Hapus")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addWidget(self.table_view)
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)

        # Signals
        self.add_btn.clicked.connect(self.add_contact)
        self.update_btn.clicked.connect(self.update_contact)
        self.delete_btn.clicked.connect(self.delete_contact)

        self.table_view.clicked.connect(self.on_select)

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("contacts.db")

        if not self.db.open():
            QMessageBox.critical(
                self, "Error", "Database tidak bisa dibuka!"
            )
            return

        self.db.exec("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )
        """)

    def add_contact(self):
        if self.name_input.text():
            record = self.model.record()

            record.setValue("name", self.name_input.text())
            record.setValue("phone", self.phone_input.text())
            record.setValue("email", self.email_input.text())

            self.model.insertRecord(-1, record)
            self.model.submitAll()
            self.model.select()

            self.clear_form()

    def update_contact(self):
        current = self.table_view.currentIndex()

        if current.isValid():
            row = current.row()

            self.model.setData(
                self.model.index(row, 1),
                self.name_input.text()
            )

            self.model.setData(
                self.model.index(row, 2),
                self.phone_input.text()
            )

            self.model.setData(
                self.model.index(row, 3),
                self.email_input.text()
            )

            self.model.submitAll()
            self.model.select()

            self.clear_form()

    def delete_contact(self):
        current = self.table_view.currentIndex()

        if current.isValid():
            self.model.removeRow(current.row())
            self.model.submitAll()
            self.model.select()

            self.clear_form()

    def on_select(self, index):
        row = index.row()

        self.name_input.setText(
            str(self.model.data(self.model.index(row, 1)) or "")
        )

        self.phone_input.setText(
            str(self.model.data(self.model.index(row, 2)) or "")
        )

        self.email_input.setText(
            str(self.model.data(self.model.index(row, 3)) or "")
        )

    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ContactApp()
    window.show()

    sys.exit(app.exec_())
