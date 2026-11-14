"""Letakkan file ini di folder proyek lalu jalankan: python cek_proyek.py
Mengecek file, nama class, dan file .ui tanpa membuka GUI."""
import ast
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
HARUS_ADA_CLASS = {
    "kelola_buku.py": "KelolaBukuWindow",
    "pinjam_buku.py": "PinjamBukuWindow",
    "kembali_buku.py": "KembaliBukuWindow",
    "laporan.py": "LaporanWindow",
    "main.py": "MainWindow",
}
HARUS_ADA_FILE = ["db_helper.py", "main.ui", "kelola_buku.ui", "pinjam_buku.ui"]

print("Folder :", BASE)
print("Python :", sys.executable)
print()

for nama, kelas in HARUS_ADA_CLASS.items():
    path = os.path.join(BASE, nama)
    if not os.path.exists(path):
        print(f"[HILANG] {nama}")
        continue
    try:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except SyntaxError as e:
        print(f"[SYNTAX ERROR] {nama} baris {e.lineno}: {e.msg}")
        continue
    top = [n.name for n in tree.body if isinstance(n, ast.ClassDef)]
    status = "OK" if kelas in top else "CLASS TIDAK ADA"
    print(f"[{status}] {nama} -> class di level atas: {top}")

print()
for nama in HARUS_ADA_FILE:
    print(f"[{'OK' if os.path.exists(os.path.join(BASE, nama)) else 'HILANG'}] {nama}")

print()
print("File .py/.ui lain di folder (cek sufiks acak / salinan):")
for nama in sorted(os.listdir(BASE)):
    if nama.endswith((".py", ".ui")) and nama not in HARUS_ADA_CLASS and nama not in HARUS_ADA_FILE:
        print("  ", nama)
