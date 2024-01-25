import sys
from PyQt5.QtCore import Qt, QTimer, QDate, QTime
from PyQt5.QtGui import QPixmap, QFont, QColor, QFontDatabase
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import requests

class Screensaver(QWidget):
    def __init__(self):
        super().__init__()


        self.init_ui()

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screensaver)
        self.timer.start(1000)  # Update screensaver every second

        self.show()

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update_screensaver(self):
        current_date = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
        current_time = QTime.currentTime().toString(Qt.DefaultLocaleShortDate)
        self.day_label.setText(f'{current_date} - {current_time.upper()}')

        try:
            params = {
                'q': "Villingen-Schwenningen",
                'appid': "c736057682224bf2b58105011232312",
                'units': 'metric'  # You can use 'imperial' for Fahrenheit
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                main_weather = data['weather'][0]['main']
                description = data['weather'][0]['description']
                temperature = data['main']['temp']
            else:
                print(f"Error: {data['message']}")

        except Exception as e:
            print(f"Error: {e}")
    
        weather_data = {'condition': main_weather}
        test = f'Weather: {weather_data["condition"]}'
        self.weather_label.setText(test.upper())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Screensaver()
    sys.exit(app.exec_())
