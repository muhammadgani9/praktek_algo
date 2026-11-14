import os
import sys
from PyQt5 import QtWidgets, uic
import db_helper
from kelola_buku import KelolaBukuWindow
from pinjam_buku import PinjamBukuWindow
from kembali_buku import KembaliBukuWindow
from laporan import LaporanWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load UI (path absolut, aman dijalankan dari folder mana pun)
        uic.loadUi(os.path.join(BASE_DIR, 'main.ui'), self)

        # Inisialisasi database
        db_helper.init_db()

        # Hubungkan tombol dashboard
        self.btnKelolaBuku.clicked.connect(self.open_kelola_buku)
        self.btnPinjamBuku.clicked.connect(self.open_pinjam_buku)
        self.btnKembaliBuku.clicked.connect(self.open_kembali_buku)
        self.btnLaporan.clicked.connect(self.open_laporan)
        self.btnKeluar.clicked.connect(self.close)

        # Referensi sub-jendela (dibuat saat pertama dibuka)
        self.kelola_buku_win = None
        self.pinjam_buku_win = None
        self.kembali_buku_win = None
        self.laporan_win = None

    def open_kelola_buku(self):
        if self.kelola_buku_win is None:
            self.kelola_buku_win = KelolaBukuWindow()
        else:
            self.kelola_buku_win.load_books()
        self._show(self.kelola_buku_win)

    def open_pinjam_buku(self):
        if self.pinjam_buku_win is None:
            self.pinjam_buku_win = PinjamBukuWindow()
        else:
            self.pinjam_buku_win.load_books_combo()
            self.pinjam_buku_win.load_active_loans()
        self._show(self.pinjam_buku_win)

    def open_kembali_buku(self):
        if self.kembali_buku_win is None:
            self.kembali_buku_win = KembaliBukuWindow()
        else:
            self.kembali_buku_win.load_active_loans()
        self._show(self.kembali_buku_win)

    def open_laporan(self):
        if self.laporan_win is None:
            self.laporan_win = LaporanWindow()
        else:
            self.laporan_win.load_report()
        self._show(self.laporan_win)

    @staticmethod
    def _show(win):
        win.show()
        win.raise_()
        win.activateWindow()

    def closeEvent(self, event):
        # Tutup sub-jendela yang masih terbuka saat dashboard ditutup
        for win in (self.kelola_buku_win, self.pinjam_buku_win,
                    self.kembali_buku_win, self.laporan_win):
            if win is not None:
                win.close()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
