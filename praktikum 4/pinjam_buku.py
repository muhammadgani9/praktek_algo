import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import db_helper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class PinjamBukuWindow(QtWidgets.QWidget):  # UI root = QWidget (FormPeminjaman)
    def __init__(self):
        super().__init__()
        # Load UI (path absolut, jadi aman dijalankan dari folder mana pun)
        uic.loadUi(os.path.join(BASE_DIR, 'pinjam_buku.ui'), self)

        # Tanggal default = hari ini
        self.datePinjam.setDate(QDate.currentDate())

        # Hubungkan tombol
        self.btnPinjam.clicked.connect(self.borrow_book)
        self.btnBersihkan.clicked.connect(self.clear_fields)
        self.btnKembali.clicked.connect(self.close)

        # Siapkan tabel: 7 kolom sesuai hasil db_helper.get_active_loans()
        self.tableWidgetPinjam.setColumnCount(7)
        self.tableWidgetPinjam.setHorizontalHeaderLabels([
            "ID Pinjam", "Nama Peminjam", "ID Buku", "Judul Buku",
            "Tanggal Pinjam", "Durasi (hari)", "Status"
        ])
        self.tableWidgetPinjam.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

        # Muat data awal
        self.load_books_combo()
        self.load_active_loans()

    def load_books_combo(self):
        self.cmbBuku.clear()
        books = db_helper.get_all_books()
        for book in books:
            id_buku, judul, _, _, _, stok = book
            # Hanya tampilkan buku yang stoknya > 0
            if stok > 0:
                self.cmbBuku.addItem(f"{id_buku} - {judul} (Stok: {stok})", id_buku)

    def load_active_loans(self):
        self.tableWidgetPinjam.setRowCount(0)
        loans = db_helper.get_active_loans()

        for row_number, row_data in enumerate(loans):
            self.tableWidgetPinjam.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidgetPinjam.setItem(row_number, column_number, item)

    def borrow_book(self):
        id_pinjam = self.txtIdPinjam.text().strip()
        nama_peminjam = self.txtNamaPeminjam.text().strip()

        if not id_pinjam or not nama_peminjam:
            QtWidgets.QMessageBox.warning(
                self, "Validasi Gagal", "ID Pinjam dan Nama Peminjam harus diisi!")
            return

        if self.cmbBuku.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(
                self, "Validasi Gagal", "Buku harus dipilih! (Stok semua buku mungkin habis)")
            return

        # Ambil ID buku dari itemData combo box
        id_buku = self.cmbBuku.currentData()
        tanggal_pinjam = self.datePinjam.date().toString("yyyy-MM-dd")
        durasi = self.spinDurasi.value()

        # Simpan transaksi peminjaman
        success, message = db_helper.add_loan(
            id_pinjam, nama_peminjam, id_buku, tanggal_pinjam, durasi)

        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_active_loans()
            self.load_books_combo()  # refresh tampilan stok
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)

    def clear_fields(self):
        self.txtIdPinjam.clear()
        self.txtNamaPeminjam.clear()
        self.datePinjam.setDate(QDate.currentDate())
        self.spinDurasi.setValue(7)
        if self.cmbBuku.count() > 0:
            self.cmbBuku.setCurrentIndex(0)


# Untuk uji coba jendela ini secara mandiri: python pinjam_buku.py
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    db_helper.init_db()
    window = PinjamBukuWindow()
    window.show()
    sys.exit(app.exec_())
