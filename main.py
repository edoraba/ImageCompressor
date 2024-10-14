import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl
import subprocess
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Imposta il profilo per gestire i download
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

        # Serve il frontend dal server Flask
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))

    def handle_download(self, download):
        # Mostra una finestra di dialogo per selezionare dove salvare il file
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path(), options=options)

        if save_path:
            download.setPath(save_path)
            download.accept()


def start_flask_server():
    # Avvia il server Flask in background
    subprocess.call(["python", "backend/app.py"])


if __name__ == "__main__":
    # Avvia il server Flask in un thread separato
    threading.Thread(target=start_flask_server, daemon=True).start()

    # Inizializza l'applicazione PyQt5
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Image Compressor")  # Imposta il titolo della finestra
    window.show()
    sys.exit(app.exec_())
