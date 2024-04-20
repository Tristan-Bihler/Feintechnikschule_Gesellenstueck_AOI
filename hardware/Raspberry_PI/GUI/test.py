import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap(r'hardware\\Raspberry_PI\\GUI\\9121424.jpg').scaled(QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height()))  # Set your image path
        self.showMessage('Your weather information',  # Set your weather information
                         Qt.AlignBottom | Qt.AlignCenter,
                         Qt.black)

    def mousePressEvent(self, event):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    main_win = MainWindow()

    # Show main window after splash screen is clicked
    QTimer.singleShot(0, lambda: splash.close() or main_win.show())

    sys.exit(app.exec_())
