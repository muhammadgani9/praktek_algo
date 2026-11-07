
import sys
from PyQt5.QtWidgets import *

class DataMahasiswa(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Mahasiswa")
        self.setGeometry(300, 300, 700, 500)

        main_layout = QVBoxLayout()

        # Form input
        form_layout = QFormLayout()

        self.nim_input = QLineEdit()
        self.nama_input = QLineEdit()
        self.nilai_input = QSpinBox()
        self.nilai_input.setRange(0, 100)

        form_layout.addRow("NIM:", self.nim_input)
        form_layout.addRow("Nama:", self.nama_input)
        form_layout.addRow("Nilai:", self.nilai_input)

        # Tombol
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Tambah")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Hapus")
        self.clear_btn = QPushButton("Clear")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)

        # Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["NIM", "Nama", "Nilai"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        # Signal connections
        self.add_btn.clicked.connect(self.add_data)
        self.update_btn.clicked.connect(self.update_data)
        self.delete_btn.clicked.connect(self.delete_data)
        self.clear_btn.clicked.connect(self.clear_form)
        self.table.itemSelectionChanged.connect(self.on_select)

        self.data = []

    def add_data(self):
        nim = self.nim_input.text()
        nama = self.nama_input.text()
        nilai = self.nilai_input.value()

        if nim and nama:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(nim))
            self.table.setItem(row, 1, QTableWidgetItem(nama))
            self.table.setItem(row, 2, QTableWidgetItem(str(nilai)))

            self.clear_form()

    def update_data(self):
        current = self.table.currentRow()

        if current >= 0:
            self.table.setItem(
                current, 0, QTableWidgetItem(self.nim_input.text())
            )
            self.table.setItem(
                current, 1, QTableWidgetItem(self.nama_input.text())
            )
            self.table.setItem(
                current, 2, QTableWidgetItem(str(self.nilai_input.value()))
            )

    def delete_data(self):
        current = self.table.currentRow()

        if current >= 0:
            self.table.removeRow(current)

    def clear_form(self):
        self.nim_input.clear()
        self.nama_input.clear()
        self.nilai_input.setValue(0)

    def on_select(self):
        current = self.table.currentRow()

        if current >= 0:
            self.nim_input.setText(
                self.table.item(current, 0).text()
            )
            self.nama_input.setText(
                self.table.item(current, 1).text()
            )
            self.nilai_input.setValue(
                int(self.table.item(current, 2).text())
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataMahasiswa()
    window.show()
    sys.exit(app.exec_())
