import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Umbra")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        central_widget.setLayout(layout)

        welcome_label = QLabel("Добро пожаловать")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        diary_button = QPushButton("Мой дневник")
        goals_button = QPushButton("Мои цели")
        settings_button = QPushButton("Настройки")

        for button in [diary_button, goals_button, settings_button]:
            button.setFixedHeight(45)
            button.setSizePolicy(
                button.sizePolicy().horizontalPolicy(),
                button.sizePolicy().verticalPolicy().Preferred
            )

        layout.addWidget(welcome_label)
        layout.addWidget(diary_button)
        layout.addWidget(goals_button)
        layout.addWidget(settings_button)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
