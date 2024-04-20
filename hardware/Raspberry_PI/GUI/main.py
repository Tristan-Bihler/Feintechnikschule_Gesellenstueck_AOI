import sys
from PyQt5.QtWidgets import *
import pyrebase
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QColor, QFontDatabase
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


class Screensaver(QWidget):
    def __init__(self, firebase):
        self.firebase = firebase
        super().__init__()
        self.other_window = MainWindow(self.firebase)  # Create an instance of the other window
        self.init_ui()
    
    def mousePressEvent(self, event):
        self.close()
        self.other_window.showMaximized()
        
    def init_ui(self):
        self.setWindowTitle('Screensaver')
        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)
        self.set_background_image(r'hardware\\Raspberry_PI\\GUI\\9121424.jpg')  # Replace with your image path

        layout = QVBoxLayout()
        layout.addWidget(self.background_label)

        self.weather_label = QLabel(self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setFont(QFont("ONE DAY", 16))  # Replace with your font file path
        layout.addWidget(self.weather_label)

        self.day_label = QLabel(self)
        self.day_label.setAlignment(Qt.AlignCenter)
        self.day_label.setFont(QFont('ONE DAY', 16))  # Replace with your font file path
        layout.addWidget(self.day_label)

        self.setLayout(layout)

        self.show()

        self.timer = QTimer(self)
        self.timer.start(60000)  # Update screensaver every second
        self.timer.timeout.connect(self.update_screensaver)


    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update_screensaver(self):
        current_date = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
        current_time = QTime.currentTime().toString(Qt.DefaultLocaleShortDate)
        self.day_label.setText(f'{current_date} - {current_time.upper()}')

        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": 48.0623,
                "longitude": 8.4936,
                "current": ["temperature_2m", "is_day"],
                "forecast_days": 1
            }
            responses = openmeteo.weather_api(url, params=params)

            # Process first location. Add a for-loop for multiple locations or weather models
            response = responses[0]
            print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
            print(f"Elevation {response.Elevation()} m asl")
            print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
            print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

            # Current values. The order of variables needs to be the same as requested.
            current = response.Current()
            current_temperature_2m = current.Variables(0).Value()
            current_is_day = current.Variables(1).Value()

        except Exception as e:
            print(f"Error: {e}")
        
        Time = current.Time()
        temperature = round(current_temperature_2m,2)
        t = temperature
        if  current_is_day == 1:
            day = "Tag"
        else:
            day = "Nacht"
        

        test =  str(t) + "°C" + " " + day
        self.weather_label.setText(test.upper())


class LoginScreen(QWidget):                                        #Klasse für das Loginscreen
    login_success = pyqtSignal()                                    

    def __init__(self, firebase, parent=None):
        super(LoginScreen, self).__init__(parent)
        self.firebase = firebase                                    #das Firebase Objekt wurde in die Firebase klasse eingegliedert

        self.layout = QFormLayout()                                 # Für den Login screen wird ein Login Layout erstellt, sodass alles richtig gegliedert ist
        self.email_edit = QLineEdit(self)                           # Ein edit Feld wird für den Login Screen erstellt, in diesem kann dann die Email eingeschrieben werden
        self.email_edit.setPlaceholderText("Enter your email")      # Als Hintergrundtext für das Loginfeld steht "Enter your email", sodass der Nutzer das auch versteht, was er tun muss
        self.password_edit = QLineEdit(self)                        # Das gleiche wie bei der Email wird auch für das Passwort gemacht.
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Enter your password")
        self.login_button = QPushButton("Login", self)              # Bestätigungs Knopf für das Bestätigen der Email und das Passwort
        self.login_button.clicked.connect(self.login_clicked)       # Der Knopf wird mit der login_click funktion verbunden. Ist der Knopf gedrückt worden, dann wird auch die Funktion ausgeführt.

        self.layout.addRow(QLabel("Email:"), self.email_edit)       # Nun wird das Emailfeld in das Layout eingetragen und Email als Label Hinzugefügt
        self.layout.addRow(QLabel("Password:"), self.password_edit) # Das gleiche gilt auch für das Passwordfelt
        self.layout.addRow(self.login_button)                       # Auch wird der Knopf hinzugefügt

        self.setLayout(self.layout)

    def login_clicked(self):                                        #Wird ausgeführt wenn der Loginknopf  gedrückt wird.
        email = self.email_edit.text()                              #überschreibt die Variable email mit dem eingeschrieben email
        password = self.password_edit.text()                        #überschreibt die Variable password mit dem eingeschrieben password

        try:
            user = self.firebase.auth().sign_in_with_email_and_password(email, password)    #Die funktion für das Einloggen wird ausgeführt mit den Variablen email und password
            print(f"Successfully logged in as {user['localId']}")
            self.login_success.emit()                                                        # Falls der Einlogversuch funktioniert, dann ist der User eingeloggt und der User kann über das Programm Daten an den Server senden.
        except Exception as e:                                                               # Falls der Einlogversuch nicht funktioniert, dann wird der User darüber informiert und kann es erneut versuchen.
            print(f"Login failed: {e}")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Login failed")
            msgBox.setWindowTitle("Login")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msgBox.exec_() 


class Dashboard(QWidget):                                            #Klasse für das Dashboard    Das Dashboad soll den User über die Lage der Maschineberichten und dem User erlauben auf die Maschine einfluss zu haben.
    def __init__(self, firebase, parent=None):
        super(Dashboard, self).__init__(parent)
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
        self.login_screen.login_success.connect(self.show_start)

        self.start_screen = QWidget(self)
        self.start_layout = QVBoxLayout(self.start_screen)

        self.dashboard_screen = Dashboard(self.firebase, self)
        self.dashboard_screen.hide()

        self.setCentralWidget(self.login_screen)
        self.setWindowTitle("Login")

    def show_start(self):
        self.setCentralWidget(self.start_screen)
        self.setWindowTitle("Start")

        # Add navigation buttons in the Dashboard Screen
        self.start_layout.addWidget(QLabel("Navigation:"))
        dashboard_button = QPushButton("Dashboard", self)
        dashboard_button.clicked.connect(self.show_dashboard_screen)
        self.start_layout.addWidget(dashboard_button)

    def show_dashboard_screen(self):
        self.dashboard_screen.show()
        self.setCentralWidget(self.dashboard_screen)
        self.setWindowTitle("Dashboard")

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


    window = Screensaver(firebase)
    window.showMaximized()
    sys.exit(app.exec_())
