import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QTextEdit, QComboBox, QHBoxLayout, QMessageBox,
    QListWidget, QLineEdit
)
from PyQt6.QtCore import Qt
from database import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Umbra")
        self.resize(800, 600)
        self.db = DatabaseManager()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_screen = QWidget()
        self.diary_screen = QWidget()
        self.goals_screen = QWidget()
        self.settings_screen = QWidget()

        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.diary_screen)
        self.stack.addWidget(self.goals_screen)
        self.stack.addWidget(self.settings_screen)

        self.setup_menu_screen()
        self.setup_diary_screen()
        self.setup_goals_screen()
        self.setup_settings_screen()

        self.setup_settings_screen()
        self.load_notes()

# Главное меню
    def setup_menu_screen(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("Добро пожаловать в Umbra 🌒")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_diary = QPushButton("📖 Мой дневник")
        btn_goals = QPushButton("🎯 Мои цели")
        btn_settings = QPushButton("⚙️ Настройки")

        for btn in [btn_diary, btn_goals, btn_settings]:
            btn.setFixedSize(250, 50)

        layout.addWidget(btn_diary, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_goals, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_settings, alignment=Qt.AlignmentFlag.AlignCenter)

        self.menu_screen.setLayout(layout)

        btn_diary.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_goals.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(3))


# Дневник

    def setup_diary_screen(self):
        layout = QVBoxLayout()

        btn_back = QPushButton("← Назад в меню")
        btn_back.setFixedWidth(150)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Название записи (например,  'Мой день')...")
        layout.addWidget(self.title_input)

        mood_layout = QHBoxLayout()
        mood_layout.addWidget(QLabel("Настроение:"))

        self.mood_combo = QComboBox()
        self.mood_combo.addItems(
            ["Радость", "Грусть", "Вдохновение", "Злость"])
        mood_layout.addWidget(self.mood_combo)

        layout.addLayout(mood_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Напиши свои мысли здесь...")
        layout.addWidget(self.text_edit)

        btn_save = QPushButton("💾 Сохранить")
        btn_save.clicked.connect(self.save_note)
        layout.addWidget(btn_save)
        self.notes_list = QListWidget()
        layout.addWidget(self.notes_list)

        self.diary_screen.setLayout(layout)

# Цели
    def setup_goals_screen(self):
        layout = QVBoxLayout()

        btn_back = QPushButton("← Назад в меню")
        btn_back.setFixedWidth(150)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        layout.addWidget(QLabel("🎯 Здесь будут ваши цели и дедлайны."))

        self.goals_screen.setLayout(layout)

# Настройки
    def setup_settings_screen(self):
        layout = QVBoxLayout()

        btn_back = QPushButton("← Назад в меню")
        btn_back.setFixedWidth(150)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        layout.addWidget(
            QLabel("⚙️ Здесь будут настройки тем и экспорт данных."))

        self.settings_screen.setLayout(layout)

    def save_note(self):
        title = self.title_input.text().strip()
        text = self.text_edit.toPlainText().strip()
        mood = self.mood_combo.currentText()

        if not title or not text:
            QMessageBox.warning(
                self, "Ошибка", "Пожалуйста, заполни название и текст записи!")
            return

        self.db.cursor.execute(
            "INSERT INTO notes (title, text, mood) VALUES (?, ?, ?)",
            (title, text, mood)
        )
        self.db.connection.commit()

        self.title_input.clear()
        self.text_edit.clear()
        self.load_notes()
        QMessageBox.information(self, "Успех", "Запись сохранена в дневник!")

    def load_notes(self):
        self.notes_list.clear()

        notes = self.db.cursor.execute(
            "SELECT * FROM notes ORDER BY id DESC").fetchall()

        for note in notes:
            title = note[1]
            text = note[2]
            mood = note[3]

            text_preview = text[:30] + "..." if len(text) > 30 else text

            display_text = f"✍ {title} | {mood}\n{text_preview}"
            self.notes_list.addItem(display_text)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Выход', 'Вы уверены, что хотите закрыть Umbra?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
