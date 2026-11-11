import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QTextEdit, QComboBox, QHBoxLayout, QMessageBox,
    QListWidget, QLineEdit, QDateEdit, QTableWidget, QTableWidgetItem, QFileDialog
)
from PyQt6.QtCore import Qt, QDate, QSettings
from database import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Umbra")
        self.resize(800, 600)
        self.db = DatabaseManager()

        self.settings = QSettings("UmbraDev", "UmbraApp")

        saved_index = int(self.settings.value("theme_index", 0))

        self.apply_theme(saved_index)

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
        self.load_goals()

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

        self.goal_input = QLineEdit()
        self.goal_input.setPlaceholderText("Введите название цели...")
        layout.addWidget(self.goal_input)

        goal_controls = QHBoxLayout()

        self.goal_date = QDateEdit()
        self.goal_date.setCalendarPopup(True)
        self.goal_date.setDate(QDate.currentDate())
        goal_controls.addWidget(self.goal_date)

        btn_add_goal = QPushButton("🖋 Добавить цель")
        btn_add_goal.clicked.connect(self.save_goal)
        goal_controls.addWidget(btn_add_goal)

        layout.addLayout(goal_controls)

        self.goals_table = QTableWidget()
        self.goals_table.setColumnCount(3)
        self.goals_table.setHorizontalHeaderLabels(["ID", "Цель", "Дедлайн"])
        self.goals_table.setColumnHidden(0, True)
        layout.addWidget(self.goals_table)

        self.goals_screen.setLayout(layout)

# Настройки
    def setup_settings_screen(self):
        layout = QVBoxLayout()

        btn_back = QPushButton("← Назад в меню")
        btn_back.setFixedWidth(150)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        layout.addWidget(QLabel("<b>Сохранение данных:</b>"))
        self.btn_export = QPushButton("📨Экспорт дневника в TXT")
        self.btn_export.setFixedHeight(40)
        self.btn_export.clicked.connect(self.export_to_txt)
        layout.addWidget(self.btn_export)

        layout.addSpacing(20)
        layout.addWidget(QLabel("<b>Внешний вид и язык:</b>"))

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "English", "Espanol"])
        layout.addWidget(QLabel("Язык интерфейса:"))
        layout.addWidget(self.lang_combo)

        self.theme_combo = QComboBox()
        self, self.theme_combo.addItems(
            ["Темная тема", "Светлая тема", "Красная тема", "Синяя тема", "Розовая тема", "Коричневая тема"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(QLabel("Тема офрмления:"))
        layout.addWidget(self.theme_combo)

        layout.addSpacing(20)
        self.btn_about = QPushButton("🚨О программе")
        self.btn_about.clicked.connect(self.show_about)
        layout.addWidget(self.btn_about)

        layout.addStretch()
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

    def save_goal(self):
        text = self.goal_input.text().strip()
        deadline = self.goal_date.date().toString("yyyy-MM-dd")
        if not text:
            QMessageBox.warning(self, "Ошибка ввода",
                                "Пожалйста, введите название цели!")
            return

        if len(text) > 100:
            QMessageBox.warning(
                self, "Ошибка", "Название цели слишком длинное (макс. 100 символов)!")
            return

        is_saved = self.db.add_goal(text, deadline)

        if is_saved:
            self.goal_input.clear()
            self.load_goals()
            QMessageBox.information(
                self, "Успех", "Новая цель успешно добавлена в трекер!")
        else:
            QMessageBox.critical(
                self, "Ошибка БД", "Не удалось сохранить цель. Проверьте поделючение к базе.")

    def load_goals(self):
        self.goals_table.setRowCount(0)

        goals = self.db.get_goals()

        self.goals_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self.goals_table.horizontalHeader().setStretchLastSection(True)
        self.goals_table.setColumnWidth(1, 250)

        for row_number, goal in enumerate(goals):
            self.goals_table.insertRow(row_number)

            goal_id = str(goal[0])
            goal_text = goal[1]
            goal_deadline = goal[2]

            id_item = QTableWidgetItem(goal_id)
            text_item = QTableWidgetItem(goal_text)
            deadline_item = QTableWidgetItem(goal_deadline)

            self.goals_table.setItem(row_number, 0, id_item)
            self.goals_table.setItem(row_number, 1, text_item)
            self.goals_table.setItem(row_number, 2, deadline_item)

    def export_to_txt(self):
        notes = self.db.get_notes()
        if not notes:
            QMessageBox.warning(self, "Ошибка", "Дневник пуст!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить дневник", "my_diary.txt", "(*.txt)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    for note in notes:
                        file.write(
                            f"Дата: {note[4]}\nЗаголовок: {note[1]}\nНастроение: {note[3]}\nТекст: {note[2]}\n")
                        file.write("-" * 40 + "\n\n")
                QMessageBox.information(
                    self, "Успех", "Дневник сохаренен в TXT!")
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Не удалось сохранить: {e}")

    def show_about(self):
        QMessageBox.about(self, "О программе Umbra",
                          "☯ Umbra (Эстетичный дневник)\n\n"
                          "Версия: 1.0\n"
                          "Автор: Eva August\n\n"
                          "Технологии: Python, PyQt6, SQLite3.")

    def apply_theme(self, theme_index):
        if theme_index == 0:
            self.setStyleSheet("background-color: #2b2b2b; color: white;")

        elif theme_index == 1:
            self.setStyleSheet("background-color: #f0f0f0; color: black;")

        elif theme_index == 2:
            self.setStyleSheet("background-color: #4a1515; color: #ffcccc;")

        elif theme_index == 3:
            self.setStyleSheet("background-color: #1a2a40; color: #d0e0f0;")

        elif theme_index == 4:
            self.setStyleSheet("background-color: #f4e1e1; color: #4a2c2c;")

        elif theme_index == 5:
            self.setStyleSheet("background-color: #3e2a20; color: #f0e6d2;")

        self.settings.setValue("theme_index", theme_index)

    def change_theme(self, index):
        self.apply_theme(index)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Выход', 'Вы уверены, что хотите закрыть Umbra?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
