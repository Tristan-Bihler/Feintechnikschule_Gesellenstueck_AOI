import sys
from PyQt5.QtCore import Qt, QTimer, QDate, QTime
from PyQt5.QtGui import QPixmap, QFont, QColor, QFontDatabase
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from main import LoginScreen  # Import the other window

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


class Screensaver(QWidget):
    def __init__(self):
        super().__init__()
        self.other_window = LoginScreen()  # Create an instance of the other window
        self.init_ui()
    
    def mousePressEvent(self, event):
        self.close()
        self.other_window.show()
        
    def init_ui(self):
        self.setGeometry(100, 100, 800, 400)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Screensaver()
    sys.exit(app.exec_())
