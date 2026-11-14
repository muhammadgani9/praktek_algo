import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import db_helper

KOLOM = ["No", "ID Buku", "Judul", "Pengarang", "Jumlah Dipinjam"]


class LaporanWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laporan Statistik Perpustakaan")
        self.resize(800, 520)

        self._build_ui()

        self.btnRefresh.clicked.connect(self.load_report)
        self.btnTutup.clicked.connect(self.close)

        self.load_report()

    # ---------- Bangun tampilan ----------
    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("LAPORAN STATISTIK")
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Ringkasan umum
        box = QtWidgets.QGroupBox("Ringkasan Umum")
        form = QtWidgets.QFormLayout(box)
        self.lblTotalBuku = QtWidgets.QLabel("-")
        self.lblDipinjam = QtWidgets.QLabel("-")
        self.lblDenda = QtWidgets.QLabel("-")
        form.addRow("Total buku (semua eksemplar):", self.lblTotalBuku)
        form.addRow("Sedang dipinjam:", self.lblDipinjam)
        form.addRow("Total denda terkumpul:", self.lblDenda)
        layout.addWidget(box)

        # Buku terpopuler
        layout.addWidget(QtWidgets.QLabel("Buku paling sering dipinjam:"))
        self.tablePopuler = QtWidgets.QTableWidget(0, len(KOLOM))
        self.tablePopuler.setHorizontalHeaderLabels(KOLOM)
        self.tablePopuler.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tablePopuler.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tablePopuler.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.tablePopuler, 1)

        # Tombol
        buttons = QtWidgets.QHBoxLayout()
        self.btnRefresh = QtWidgets.QPushButton("Refresh")
        self.btnTutup = QtWidgets.QPushButton("Tutup")
        buttons.addWidget(self.btnRefresh)
        buttons.addStretch(1)
        buttons.addWidget(self.btnTutup)
        layout.addLayout(buttons)

    # ---------- Data ----------
    def load_report(self):
        stat = db_helper.get_general_statistics()
        self.lblTotalBuku.setText(str(stat['total_buku']))
        self.lblDipinjam.setText(str(stat['active_loans']))
        self.lblDenda.setText(f"Rp {stat['total_denda']:,.0f}")

        self.tablePopuler.setRowCount(0)
        # row = (id_buku, judul, pengarang, jumlah_dipinjam)
        for r, row in enumerate(db_helper.get_most_borrowed_books()):
            self.tablePopuler.insertRow(r)
            for c, value in enumerate((r + 1,) + tuple(row)):
                item = QtWidgets.QTableWidgetItem(str(value))
                if c in (0, 4):
                    item.setTextAlignment(Qt.AlignCenter)
                self.tablePopuler.setItem(r, c, item)


# Uji coba mandiri: python laporan.py
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    db_helper.init_db()
    window = LaporanWindow()
    window.show()
    sys.exit(app.exec_())
