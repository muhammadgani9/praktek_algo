import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, Qt
import db_helper

DENDA_PER_HARI_DEFAULT = 1000  # Rupiah per hari keterlambatan (bisa diubah di form)

KOLOM = ["ID Pinjam", "Nama Peminjam", "ID Buku", "Judul Buku",
         "Tanggal Pinjam", "Durasi (hari)", "Jatuh Tempo"]


class KembaliBukuWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pengembalian Buku")
        self.resize(900, 560)

        self._build_ui()

        # Hubungkan sinyal
        self.tableLoans.itemSelectionChanged.connect(self.update_info)
        self.dateKembali.dateChanged.connect(self.update_info)
        self.spinDenda.valueChanged.connect(self.update_info)
        self.btnProses.clicked.connect(self.process_return)
        self.btnRefresh.clicked.connect(self.load_active_loans)
        self.btnTutup.clicked.connect(self.close)

        self.load_active_loans()

    # ---------- Bangun tampilan ----------
    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("PENGEMBALIAN BUKU")
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addWidget(QtWidgets.QLabel("Pilih transaksi peminjaman yang akan dikembalikan:"))

        # Tabel pinjaman aktif
        self.tableLoans = QtWidgets.QTableWidget(0, len(KOLOM))
        self.tableLoans.setHorizontalHeaderLabels(KOLOM)
        self.tableLoans.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableLoans.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableLoans.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableLoans.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.tableLoans, 1)

        # Form pengembalian
        form = QtWidgets.QFormLayout()
        self.dateKembali = QtWidgets.QDateEdit(QDate.currentDate())
        self.dateKembali.setCalendarPopup(True)
        self.dateKembali.setDisplayFormat("yyyy-MM-dd")
        form.addRow("Tanggal Kembali:", self.dateKembali)

        self.spinDenda = QtWidgets.QSpinBox()
        self.spinDenda.setRange(0, 1000000)
        self.spinDenda.setSingleStep(500)
        self.spinDenda.setPrefix("Rp ")
        self.spinDenda.setValue(DENDA_PER_HARI_DEFAULT)
        form.addRow("Denda per hari:", self.spinDenda)

        self.lblInfo = QtWidgets.QLabel("Pilih salah satu baris pada tabel.")
        self.lblInfo.setWordWrap(True)
        form.addRow("Ringkasan:", self.lblInfo)
        layout.addLayout(form)

        # Tombol
        buttons = QtWidgets.QHBoxLayout()
        self.btnProses = QtWidgets.QPushButton("Proses Pengembalian")
        self.btnRefresh = QtWidgets.QPushButton("Refresh")
        self.btnTutup = QtWidgets.QPushButton("Tutup")
        buttons.addWidget(self.btnProses)
        buttons.addWidget(self.btnRefresh)
        buttons.addStretch(1)
        buttons.addWidget(self.btnTutup)
        layout.addLayout(buttons)

    # ---------- Data ----------
    def load_active_loans(self):
        self.tableLoans.setRowCount(0)
        loans = db_helper.get_active_loans()
        # row = (id_pinjam, nama, id_buku, judul, tgl_pinjam, durasi, status)

        for r, row in enumerate(loans):
            self.tableLoans.insertRow(r)
            jatuh_tempo = self._jatuh_tempo(row[4], row[5])
            tampil = list(row[:6]) + [jatuh_tempo.toString("yyyy-MM-dd") if jatuh_tempo.isValid() else "-"]
            for c, value in enumerate(tampil):
                self.tableLoans.setItem(r, c, QtWidgets.QTableWidgetItem(str(value)))

        self.update_info()

    @staticmethod
    def _jatuh_tempo(tanggal_pinjam, durasi):
        tgl = QDate.fromString(str(tanggal_pinjam), "yyyy-MM-dd")
        return tgl.addDays(int(durasi)) if tgl.isValid() else QDate()

    def _selected_loan(self):
        rows = self.tableLoans.selectionModel().selectedRows()
        if not rows:
            return None
        r = rows[0].row()
        return {
            "id_pinjam": self.tableLoans.item(r, 0).text(),
            "nama": self.tableLoans.item(r, 1).text(),
            "judul": self.tableLoans.item(r, 3).text(),
            "tgl_pinjam": self.tableLoans.item(r, 4).text(),
            "durasi": int(self.tableLoans.item(r, 5).text()),
        }

    def _hitung(self, loan):
        """Mengembalikan (jatuh_tempo, hari_telat, denda)."""
        jatuh_tempo = self._jatuh_tempo(loan["tgl_pinjam"], loan["durasi"])
        telat = max(0, jatuh_tempo.daysTo(self.dateKembali.date())) if jatuh_tempo.isValid() else 0
        return jatuh_tempo, telat, telat * self.spinDenda.value()

    def update_info(self):
        loan = self._selected_loan()
        if not loan:
            self.lblInfo.setText("Pilih salah satu baris pada tabel.")
            return
        jatuh_tempo, telat, denda = self._hitung(loan)
        self.lblInfo.setText(
            f"{loan['judul']} - dipinjam oleh {loan['nama']}\n"
            f"Jatuh tempo: {jatuh_tempo.toString('yyyy-MM-dd')}  |  "
            f"Terlambat: {telat} hari  |  Denda: Rp {denda:,.0f}"
        )

    # ---------- Aksi ----------
    def process_return(self):
        loan = self._selected_loan()
        if not loan:
            QtWidgets.QMessageBox.warning(
                self, "Validasi Gagal", "Pilih transaksi dari tabel terlebih dahulu!")
            return

        _, telat, denda = self._hitung(loan)
        tanggal_kembali = self.dateKembali.date().toString("yyyy-MM-dd")

        reply = QtWidgets.QMessageBox.question(
            self, "Konfirmasi Pengembalian",
            f"Kembalikan buku '{loan['judul']}' dari {loan['nama']}?\n"
            f"Terlambat {telat} hari, denda Rp {denda:,.0f}.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply != QtWidgets.QMessageBox.Yes:
            return

        success, message = db_helper.return_book(loan["id_pinjam"], tanggal_kembali, denda)
        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_active_loans()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)


# Uji coba mandiri: python kembali_buku.py
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    db_helper.init_db()
    window = KembaliBukuWindow()
    window.show()
    sys.exit(app.exec_())
