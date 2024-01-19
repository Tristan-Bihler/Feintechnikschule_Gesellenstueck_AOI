import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QFormLayout, QMessageBox
import pyrebase
from PyQt5.QtCore import pyqtSignal

class LoginScreen(QWidget):
    login_success = pyqtSignal()

    def __init__(self, firebase, parent=None):
        super(LoginScreen, self).__init__(parent)
        self.firebase = firebase

        self.layout = QFormLayout()
        self.email_edit = QLineEdit(self)
        self.email_edit.setPlaceholderText("Enter your email")
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Enter your password")
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_clicked)

        self.layout.addRow(QLabel("Email:"), self.email_edit)
        self.layout.addRow(QLabel("Password:"), self.password_edit)
        self.layout.addRow(self.login_button)

        self.setLayout(self.layout)

    def login_clicked(self):
        email = self.email_edit.text()
        password = self.password_edit.text()

        try:
            user = self.firebase.auth().sign_in_with_email_and_password(email, password)
            print(f"Successfully logged in as {user['localId']}")
            self.login_success.emit()
        except Exception as e:
            print(f"Login failed: {e}")
            QMessageBox.critical(self, "Login failes", QMessageBox.Ok)

class MachineScreen(QWidget):
    def __init__(self, firebase, parent=None):
        super(MachineScreen, self).__init__(parent)
        self.firebase = firebase
        self.db = self.firebase.database()

        self.layout = QVBoxLayout()
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_button_clicked)

        self.layout.addWidget(QLabel("Machine Screen"))
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def start_button_clicked(self):
        print("Start button clicked on Machine Screen")
        # Update the value in the Realtime Database to 1 when the Start button is clicked
        machine_ref = self.db.child("machines").child("lumina_mk1")
        machine_ref.update({"status": 1})

class MainWindow(QMainWindow):
    def __init__(self, firebase):
        super(MainWindow, self).__init__()

        self.firebase = firebase

        self.login_screen = LoginScreen(self.firebase)
        self.login_screen.login_success.connect(self.show_dashboard)

        self.dashboard_screen = QWidget(self)
        self.dashboard_layout = QVBoxLayout(self.dashboard_screen)

        self.machine_screen = MachineScreen(self.firebase, self)
        self.machine_screen.hide()

        self.setCentralWidget(self.login_screen)
        self.setWindowTitle("Login Screen")

    def show_dashboard(self):
        self.setCentralWidget(self.dashboard_screen)
        self.setWindowTitle("Dashboard Screen")

        # Add navigation buttons in the Dashboard Screen
        self.dashboard_layout.addWidget(QLabel("Navigation:"))
        machine_button = QPushButton("Machine Screen", self)
        machine_button.clicked.connect(self.show_machine_screen)
        self.dashboard_layout.addWidget(machine_button)

    def show_machine_screen(self):
        self.machine_screen.show()
        self.setCentralWidget(self.machine_screen)
        self.setWindowTitle("Machine Screen")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize Firebase
    firebase_config = {
                    "apiKey": "AIzaSyCst7QRNnFR9eC0YpiDYjYuAyjsrDdUtT4",
                    "authDomain": "tbstudios-aoi.firebaseapp.com",
                    "databaseURL": "https://tbstudios-aoi-default-rtdb.europe-west1.firebasedatabase.app",
                    "projectId": "tbstudios-aoi",
                    "storageBucket": "tbstudios-aoi.appspot.com",
                    "messagingSenderId": "875785319966",
                    "appId": "1:875785319966:web:8211d34038a1ed2d8a600f",
                    "measurementId": "G-G28PMSQPBE"
                }

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()


    window = MainWindow(firebase)
    window.show()
    sys.exit(app.exec_())
