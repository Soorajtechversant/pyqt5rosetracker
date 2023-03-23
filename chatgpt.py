from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

class LoginWidget(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        # Check the login credentials here
        if self.username_input.text() == "admin" and self.password_input.text() == "admin123":
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Widget")
        self.label = QLabel("Welcome!")
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_widget = LoginWidget()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.login_widget)
        self.login_widget.login_successful.connect(self.show_main_widget)

    def show_main_widget(self):
        self.setCentralWidget(self.main_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
