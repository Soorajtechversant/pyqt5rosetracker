from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import time

class Worker(QThread):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        # Do some long-running work
        for i in range(10):
            print(i)
            time.sleep(1)

        # Emit a signal to indicate that the work is done
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a button to start the worker thread
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_worker)
        self.start_button.move(50, 50)

        # Create a button to stop the worker thread
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_worker)
        self.stop_button.move(150, 50)

        # Create a worker thread to do some long-running work
        self.worker = Worker()
        self.worker.finished.connect(self.on_worker_finished)

    def start_worker(self):
        # Start the worker thread
        self.worker.start()

    def stop_worker(self):
        # Stop the worker thread
        self.worker.terminate()

    def on_worker_finished(self):
        # Handle the worker thread finishing
        print('Worker finished')

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()