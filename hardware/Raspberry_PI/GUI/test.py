import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

class CustomFontLabelApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Custom Font QLabel')

        layout = QVBoxLayout()

        custom_font = QFont('ONE DAY', 20)  # Replace with your font file path and size
        custom_font_label = QLabel('Hello, Custom Font!', self)
        custom_font_label.setFont(custom_font)
        layout.addWidget(custom_font_label)

        self.setLayout(layout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CustomFontLabelApp()
    sys.exit(app.exec_())
