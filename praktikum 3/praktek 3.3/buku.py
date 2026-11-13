
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt, QDate


class LibrarySystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistem Peminjaman Buku")
        self.setGeometry(300, 300, 900, 600)

        self.init_db()
        self.setup_ui()

    # Database
    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("library.db")

        if not self.db.open():
            QMessageBox.critical(
                self, "Error", "Database gagal dibuka!"
            )
            sys.exit(1)

        self.db.exec("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                stock INTEGER DEFAULT 1
            )
        """)

        self.db.exec("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                borrower TEXT,
                loan_date TEXT,
                return_date TEXT,
                status TEXT DEFAULT 'active'
            )
        """)

    # Setup UI
    def setup_ui(self):
        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # TAB 1: KELOLA BUKU
        books_tab = QWidget()
        tabs.addTab(books_tab, "Kelola Buku")

        books_layout = QVBoxLayout(books_tab)
        form_layout = QGridLayout()

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()

        self.stock_input = QSpinBox()
        self.stock_input.setRange(1, 100)

        form_layout.addWidget(QLabel("Judul:"), 0, 0)
        form_layout.addWidget(self.title_input, 0, 1)

        form_layout.addWidget(QLabel("Penulis:"), 1, 0)
        form_layout.addWidget(self.author_input, 1, 1)

        form_layout.addWidget(QLabel("Stok:"), 2, 0)
        form_layout.addWidget(self.stock_input, 2, 1)

        btn_layout = QHBoxLayout()

        self.add_book_btn = QPushButton("Tambah Buku")
        self.update_book_btn = QPushButton("Update Buku")
        self.delete_book_btn = QPushButton("Hapus Buku")

        btn_layout.addWidget(self.add_book_btn)
        btn_layout.addWidget(self.update_book_btn)
        btn_layout.addWidget(self.delete_book_btn)

        self.book_model = QSqlTableModel(self, self.db)
        self.book_model.setTable("books")
        self.book_model.select()

        self.book_table = QTableView()
        self.book_table.setModel(self.book_model)
        self.book_table.setSelectionBehavior(
            QTableView.SelectRows
        )

        books_layout.addLayout(form_layout)
        books_layout.addLayout(btn_layout)
        books_layout.addWidget(self.book_table)

        # TAB 2: PINJAM BUKU
        borrow_tab = QWidget()
        tabs.addTab(borrow_tab, "Pinjam Buku")

        borrow_layout = QVBoxLayout(borrow_tab)

        borrow_layout.addWidget(QLabel("Pilih Buku:"))

        self.book_combo = QComboBox()
        self.load_books_to_combo()

        borrow_layout.addWidget(self.book_combo)

        borrow_layout.addWidget(QLabel("Nama Peminjam:"))

        self.borrower_input = QLineEdit()
        borrow_layout.addWidget(self.borrower_input)

        self.borrow_btn = QPushButton("Pinjam Buku")
        borrow_layout.addWidget(self.borrow_btn)

        # TAB 3: KEMBALIKAN BUKU
        return_tab = QWidget()
        tabs.addTab(return_tab, "Kembalikan Buku")

        return_layout = QVBoxLayout(return_tab)

        self.loan_model = QSqlTableModel(self, self.db)
        self.loan_model.setTable("loans")
        self.loan_model.setFilter("status='active'")
        self.loan_model.select()

        self.loan_table = QTableView()
        self.loan_table.setModel(self.loan_model)
        self.loan_table.setSelectionBehavior(
            QTableView.SelectRows
        )

        self.return_btn = QPushButton("Kembalikan Buku")

        return_layout.addWidget(
            QLabel("Peminjaman Aktif:")
        )
        return_layout.addWidget(self.loan_table)
        return_layout.addWidget(self.return_btn)

        # TAB 4: LAPORAN
        reports_tab = QWidget()
        tabs.addTab(reports_tab, "Laporan")

        reports_layout = QVBoxLayout(reports_tab)

        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignTop)

        self.refresh_btn = QPushButton("Refresh Laporan")

        reports_layout.addWidget(self.stats_label)
        reports_layout.addWidget(self.refresh_btn)

        # SIGNAL CONNECTIONS
        self.add_book_btn.clicked.connect(self.add_book)
        self.update_book_btn.clicked.connect(self.update_book)
        self.delete_book_btn.clicked.connect(self.delete_book)

        self.book_table.clicked.connect(self.on_book_select)

        self.borrow_btn.clicked.connect(self.borrow_book)
        self.return_btn.clicked.connect(self.return_book)
        self.refresh_btn.clicked.connect(self.refresh_stats)

        self.refresh_stats()

    # Load books to combo box
    def load_books_to_combo(self):
        self.book_combo.clear()

        query = self.db.exec(
            "SELECT id, title FROM books WHERE stock > 0"
        )

        while query.next():
            self.book_combo.addItem(
                str(query.value(1)),
                query.value(0)
            )

    # Add book
    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()

        if title.strip():
            query = QSqlQuery(self.db)
            query.prepare("""
                INSERT INTO books (title, author, stock)
                VALUES (?, ?, ?)
            """)

            query.addBindValue(title)
            query.addBindValue(author)
            query.addBindValue(self.stock_input.value())

            if query.exec_():
                self.book_model.select()
                self.load_books_to_combo()
                self.clear_book_form()

                QMessageBox.information(
                    self, "Sukses", "Buku berhasil ditambahkan!"
                )
            else:
                QMessageBox.warning(
                    self, "Error", query.lastError().text()
                )
        else:
            QMessageBox.warning(
                self, "Peringatan", "Judul buku harus diisi!"
            )

    # Update book
    def update_book(self):
        current = self.book_table.currentIndex()

        if current.isValid():
            row = current.row()

            book_id = self.book_model.data(
                self.book_model.index(row, 0)
            )

            query = QSqlQuery(self.db)
            query.prepare("""
                UPDATE books
                SET title=?, author=?, stock=?
                WHERE id=?
            """)

            query.addBindValue(self.title_input.text())
            query.addBindValue(self.author_input.text())
            query.addBindValue(self.stock_input.value())
            query.addBindValue(book_id)

            if query.exec_():
                self.book_model.select()
                self.load_books_to_combo()

                QMessageBox.information(
                    self, "Sukses", "Data buku berhasil diperbarui!"
                )

    # Delete book
    def delete_book(self):
        current = self.book_table.currentIndex()

        if current.isValid():
            reply = QMessageBox.question(
                self,
                "Konfirmasi",
                "Hapus buku ini?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                row = current.row()

                book_id = self.book_model.data(
                    self.book_model.index(row, 0)
                )

                query = QSqlQuery(self.db)
                query.prepare(
                    "DELETE FROM books WHERE id=?"
                )
                query.addBindValue(book_id)

                if query.exec_():
                    self.book_model.select()
                    self.load_books_to_combo()

                    QMessageBox.information(
                        self, "Sukses", "Buku berhasil dihapus!"
                    )

    # Select book
    def on_book_select(self, index):
        row = index.row()

        self.title_input.setText(
            str(self.book_model.data(
                self.book_model.index(row, 1)
            ))
        )

        self.author_input.setText(
            str(self.book_model.data(
                self.book_model.index(row, 2)
            ))
        )

        self.stock_input.setValue(
            int(self.book_model.data(
                self.book_model.index(row, 3)
            ))
        )

    # Clear form
    def clear_book_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.stock_input.setValue(1)

    # Borrow book
    def borrow_book(self):
        book_id = self.book_combo.currentData()
        borrower = self.borrower_input.text()

        if not borrower.strip():
            QMessageBox.warning(
                self, "Peringatan", "Nama peminjam harus diisi!"
            )
            return

        if book_id is None:
            QMessageBox.warning(
                self, "Peringatan", "Tidak ada buku tersedia!"
            )
            return

        today = QDate.currentDate().toString("yyyy-MM-dd")

        query = QSqlQuery(self.db)
        query.prepare("""
            INSERT INTO loans
            (book_id, borrower, loan_date, status)
            VALUES (?, ?, ?, 'active')
        """)

        query.addBindValue(book_id)
        query.addBindValue(borrower)
        query.addBindValue(today)

        if query.exec_():
            self.db.exec(
                f"UPDATE books SET stock=stock-1 "
                f"WHERE id={int(book_id)} AND stock>0"
            )

            self.book_model.select()
            self.loan_model.select()
            self.load_books_to_combo()

            self.borrower_input.clear()
            self.refresh_stats()

            QMessageBox.information(
                self,
                "Sukses",
                f"Buku dipinjam oleh {borrower}"
            )

    # Return book
    def return_book(self):
        current = self.loan_table.currentIndex()

        if current.isValid():
            row = current.row()

            loan_id = self.loan_model.data(
                self.loan_model.index(row, 0)
            )

            book_id = self.loan_model.data(
                self.loan_model.index(row, 1)
            )

            today = QDate.currentDate().toString("yyyy-MM-dd")

            query = QSqlQuery(self.db)
            query.prepare("""
                UPDATE loans
                SET return_date=?, status='returned'
                WHERE id=? AND status='active'
            """)

            query.addBindValue(today)
            query.addBindValue(loan_id)

            if query.exec_():
                if query.numRowsAffected() > 0:
                    self.db.exec(
                        f"UPDATE books SET stock=stock+1 "
                        f"WHERE id={int(book_id)}"
                    )

                    self.book_model.select()
                    self.loan_model.select()
                    self.load_books_to_combo()
                    self.refresh_stats()

                    QMessageBox.information(
                        self,
                        "Sukses",
                        "Buku telah dikembalikan!"
                    )
        else:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Pilih data peminjaman terlebih dahulu!"
            )

    # Refresh reports
    def refresh_stats(self):
        # Count books
        query = self.db.exec(
            "SELECT COUNT(*) FROM books"
        )
        query.next()
        total_books = query.value(0)

        # Count total stock
        query = self.db.exec(
            "SELECT SUM(stock) FROM books"
        )
        query.next()
        total_stock = query.value(0) or 0

        # Count active loans
        query = self.db.exec(
            "SELECT COUNT(*) FROM loans WHERE status='active'"
        )
        query.next()
        active_loans = query.value(0)

        # Count returned books
        query = self.db.exec(
            "SELECT COUNT(*) FROM loans WHERE status='returned'"
        )
        query.next()
        returned_books = query.value(0)

        self.stats_label.setText(
            f"""
            <h2>Laporan Sistem Perpustakaan</h2>
            <hr>
            <h3>Total Jenis Buku: {total_books}</h3>
            <h3>Total Stok Buku: {total_stock}</h3>
            <h3>Peminjaman Aktif: {active_loans}</h3>
            <h3>Buku Dikembalikan: {returned_books}</h3>
            """
        )


# Main program
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LibrarySystem()
    window.show()

    sys.exit(app.exec_())
