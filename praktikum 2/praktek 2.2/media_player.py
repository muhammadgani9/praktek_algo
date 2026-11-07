
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist


class SimpleMediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Media Player")
        self.setGeometry(300, 300, 500, 200)

        # Membuat media player dan playlist
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        # Widget utama
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Tombol kontrol
        btn_layout = QHBoxLayout()

        self.play_btn = QPushButton("▶ Play")
        self.pause_btn = QPushButton("⏸ Pause")
        self.stop_btn = QPushButton("⏹ Stop")
        self.add_btn = QPushButton("+ Add File")

        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.add_btn)

        # Slider untuk mengatur posisi audio
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        # Label informasi audio
        self.current_label = QLabel("No file playing")

        layout.addLayout(btn_layout)
        layout.addWidget(self.slider)
        layout.addWidget(self.current_label)

        # Menghubungkan tombol dengan fungsi
        self.play_btn.clicked.connect(self.player.play)
        self.pause_btn.clicked.connect(self.player.pause)
        self.stop_btn.clicked.connect(self.player.stop)
        self.add_btn.clicked.connect(self.add_file)

        # Menghubungkan sinyal media player
        self.player.positionChanged.connect(self.update_slider)
        self.player.durationChanged.connect(self.set_duration)
        self.player.currentMediaChanged.connect(self.update_label)

    # Fungsi untuk menambahkan file audio
    def add_file(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Audio Files",
            "",
            "Audio Files (*.mp3 *.wav)"
        )

        for file in files:
            self.playlist.addMedia(
                QMediaContent(QUrl.fromLocalFile(file))
            )

            self.current_label.setText(
                f"Added: {os.path.basename(file)}"
            )

        # Memilih audio pertama jika playlist belum memiliki pilihan
        if self.playlist.currentIndex() == -1 and files:
            self.playlist.setCurrentIndex(0)

    # Fungsi mengatur posisi audio
    def set_position(self, position):
        self.player.setPosition(position)

    # Fungsi memperbarui slider
    def update_slider(self, position):
        self.slider.setValue(position)

    # Fungsi mengatur batas slider
    def set_duration(self, duration):
        self.slider.setRange(0, duration)

    # Fungsi memperbarui nama audio
    def update_label(self, media):
        if media.isNull():
            self.current_label.setText("No file playing")
        else:
            self.current_label.setText(
                f"Playing: {media.canonicalUrl().fileName()}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SimpleMediaPlayer()
    window.show()

    sys.exit(app.exec_())
