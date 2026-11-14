import os
import sys
from PyQt5 import QtWidgets, uic
import db_helper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class KelolaBukuWindow(QtWidgets.QMainWindow):  # UI root = QMainWindow
    def __init__(self):
        super().__init__()
        # Load UI (path absolut, jadi aman dijalankan dari folder mana pun)
        uic.loadUi(os.path.join(BASE_DIR, 'kelola_buku.ui'), self)

        # Hubungkan tombol
        self.btnTambah.clicked.connect(self.add_book)
        self.btnEdit.clicked.connect(self.edit_book)
        self.btnHapus.clicked.connect(self.delete_book)
        self.btnBersihkan.clicked.connect(self.clear_fields)
        self.btnKembali.clicked.connect(self.close)

        # Hubungkan pemilihan baris tabel
        self.tableBuku.itemSelectionChanged.connect(self.on_table_select)

        # Lebar kolom tabel
        self.tableBuku.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

        # Muat data awal
        self.load_books()

    def load_books(self):
        self.tableBuku.setRowCount(0)
        books = db_helper.get_all_books()

        for row_number, row_data in enumerate(books):
            self.tableBuku.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tableBuku.setItem(row_number, column_number, item)

    def on_table_select(self):
        selected_rows = self.tableBuku.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()

        # Isi kolom input dari baris terpilih
        self.txtIdBuku.setText(self.tableBuku.item(row, 0).text())
        self.txtJudul.setText(self.tableBuku.item(row, 1).text())
        self.txtPengarang.setText(self.tableBuku.item(row, 2).text())
        self.txtPenerbit.setText(self.tableBuku.item(row, 3).text())
        self.txtTahun.setText(self.tableBuku.item(row, 4).text())
        self.txtStok.setText(self.tableBuku.item(row, 5).text())

        # ID buku (primary key) tidak boleh diubah saat edit
        self.txtIdBuku.setReadOnly(True)

    def validate_inputs(self):
        id_buku = self.txtIdBuku.text().strip()
        judul = self.txtJudul.text().strip()
        pengarang = self.txtPengarang.text().strip()
        penerbit = self.txtPenerbit.text().strip()
        tahun = self.txtTahun.text().strip()
        stok = self.txtStok.text().strip()

        if not (id_buku and judul and pengarang and penerbit and tahun and stok):
            QtWidgets.QMessageBox.warning(
                self, "Validasi Gagal", "Semua kolom harus diisi!")
            return None

        try:
            tahun_int = int(tahun)
            stok_int = int(stok)
            if tahun_int < 0 or stok_int < 0:
                raise ValueError()
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Validasi Gagal",
                "Tahun Terbit dan Stok harus berupa angka bulat positif!")
            return None

        return id_buku, judul, pengarang, penerbit, tahun_int, stok_int

    def add_book(self):
        # Jika ID terkunci, berarti baris tabel sedang dipilih (mode edit)
        if self.txtIdBuku.isReadOnly():
            QtWidgets.QMessageBox.warning(
                self, "Tambah Gagal",
                "Anda sedang memilih buku dari tabel.\n"
                "Klik 'Bersihkan' dulu untuk menambah buku baru.")
            return

        validated = self.validate_inputs()
        if not validated:
            return

        id_buku, judul, pengarang, penerbit, tahun, stok = validated
        success, message = db_helper.add_book(
            id_buku, judul, pengarang, penerbit, tahun, stok)

        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_books()
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)

    def edit_book(self):
        # ID terkunci = ada baris yang dipilih
        if not self.txtIdBuku.isReadOnly():
            QtWidgets.QMessageBox.warning(
                self, "Edit Gagal", "Pilih buku dari tabel terlebih dahulu untuk diedit!")
            return

        validated = self.validate_inputs()
        if not validated:
            return

        id_buku, judul, pengarang, penerbit, tahun, stok = validated

        reply = QtWidgets.QMessageBox.question(
            self, "Konfirmasi Edit",
            f"Apakah Anda yakin ingin memperbarui data buku dengan ID {id_buku}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return

        success, message = db_helper.update_book(
            id_buku, judul, pengarang, penerbit, tahun, stok)

        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_books()
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)

    def delete_book(self):
        id_buku = self.txtIdBuku.text().strip()
        if not id_buku or not self.txtIdBuku.isReadOnly():
            QtWidgets.QMessageBox.warning(
                self, "Hapus Gagal", "Pilih buku dari tabel terlebih dahulu untuk dihapus!")
            return

        reply = QtWidgets.QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus buku dengan ID {id_buku}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return

        success, message = db_helper.delete_book(id_buku)

        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_books()
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)

    def clear_fields(self):
        self.txtIdBuku.clear()
        self.txtJudul.clear()
        self.txtPengarang.clear()
        self.txtPenerbit.clear()
        self.txtTahun.clear()
        self.txtStok.clear()

        # Buka kembali kunci ID buku, lalu hapus pilihan tabel
        self.txtIdBuku.setReadOnly(False)
        self.tableBuku.clearSelection()


# Untuk uji coba jendela ini secara mandiri: python kelola_buku.py
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    db_helper.init_db()
    window = KelolaBukuWindow()
    window.show()
    sys.exit(app.exec_())
