import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QTextEdit, QComboBox, QHBoxLayout, QMessageBox,
    QListWidget, QLineEdit, QDateEdit, QTableWidget, QTableWidgetItem, QFileDialog, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate, QSettings
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from database import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Umbra")
        self.resize(800, 600)
        self.db = DatabaseManager()


# Ctrl+S-сохранить запись
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_save.activated.connect(self.save_note)

# Ctrl+E-экспорт дневника
        self.shortcut_export = QShortcut(QKeySequence("Ctrl+E"), self)
        self.shortcut_export.activated.connect(self.export_to_txt)

# Esc-вернуться в меню
        self.shortcut_back = QShortcut(QKeySequence("Esc"), self)
        self.shortcut_back.activated.connect(
            lambda: self.stack.setCurrentIndex(0))

        self.settings = QSettings("UmbraDev", "UmbraApp")

        saved_index = int(self.settings.value("theme_index", 0))

        self.apply_theme(saved_index)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_screen = QWidget()
        self.diary_list_screen = QWidget()
        self.diary_edit_screen = QWidget()
        self.goals_screen = QWidget()
        self.settings_screen = QWidget()

        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.diary_list_screen)
        self.stack.addWidget(self.diary_edit_screen)
        self.stack.addWidget(self.goals_screen)
        self.stack.addWidget(self.settings_screen)

        self.setup_menu_screen()
        self.setup_diary_list_screen()
        self.setup_diary_edit_screen()
        self.setup_goals_screen()
        self.setup_settings_screen()

        self.load_notes()
        self.load_goals()
        saved_theme = self.db.get_settings("theme_index", "0")
        self.theme_combo.setCurrentIndex(int(saved_theme))
        self.change_theme(int(saved_theme))

        self.menu_screen.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground, True)
        self.menu_screen.setStyleSheet("""
            QWidget {
                background-image: url(resources/bg_menu.png);
                background-position: center;
                }
        """)

        screens_with_smoke = [
            self.diary_list_screen,
            self.diary_edit_screen,
            self.goals_screen,
            self.settings_screen
        ]

        for screen in screens_with_smoke:
            screen.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            screen.setStyleSheet("""
            QWidget {
                background-image: url(resources/bg_smoke.png);
                background-position: center;
                }
            """)


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
        btn_goals.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(4))

    def setup_diary_list_screen(self):
        layout = QVBoxLayout()

        btn_back = QPushButton("← Назад в меню")
        btn_back.setFixedWidth(150)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        btn_new = QPushButton("📑Создать новую запись")
        btn_new.setFixedHeight(40)
        btn_new.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        layout.addWidget(btn_new)

        self.notes_list = QListWidget()

        self.notes_list.itemClicked.connect(self.read_note)
        layout.addWidget(self.notes_list)

        self.diary_list_screen.setLayout(layout)


# Дневник

    def setup_diary_edit_screen(self):
        layout = QVBoxLayout()

        btn_cancel = QPushButton("← Отмена")
        btn_cancel.setFixedWidth(150)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn_cancel)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Название записи (например,  'Мой день')...")
        layout.addWidget(self.title_input)

        self.mood_combo = QComboBox()
        self.mood_combo.addItems(
            ["Радость", "Грусть", "Вдохновение", "Злость"])
        layout.addWidget(self.mood_combo)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Напиши свои мысли здесь...")
        layout.addWidget(self.text_edit)

        btn_save = QPushButton("💾 Сохранить запись")
        btn_save.setFixedHeight(40)
        btn_save.clicked.connect(self.save_note)
        layout.addWidget(btn_save)

        btn_delete = QPushButton("🗑️Удалить запись")
        btn_delete.setStyleSheet("background-color: #8b0000; color: white;")
        btn_delete.clicked.connect(self.delete_current_note)
        layout.addWidget(btn_delete)

        self.diary_edit_screen.setLayout(layout)

    def delete_current_note(self):
        if hasattr(self, 'current_note_id') and self.current_note_id is not None:
            self.db.delete_note(self.current_note_id)
            self.current_note_id = None
            self.title_input.clear()
            self.text_edit.clear()
            self.load_notes()
            self.stack.setCurrentIndex(1)


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

        btn_delete_goal = QPushButton("❗Удалить выбранную цель")
        btn_delete_goal.setFixedHeight(40)
        btn_delete_goal.setStyleSheet(
            "background-color: #8b0000; color: white; border-radius: 5px;")
        btn_delete_goal.clicked.connect(self.delete_selected_goal)
        layout.addWidget(btn_delete_goal)

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
                self, "Ошибка", "Заполни название и текст!")
            return

        if hasattr(self, 'current_note_id') and self.current_note_id is not None:
            self.db.update_note(self.current_note_id, title, text, mood)
            self.current_note_id = None
        else:
            self.db.cursor.execute(
                "INSERT INTO notes (title, text, mood) VALUES (?, ?, ?)",
                (title, text, mood)
            )
        self.db.connection.commit()

        self.title_input.clear()
        self.text_edit.clear()
        self.load_notes()
        self.stack.setCurrentIndex(1)
        QMessageBox.information(self, "Успех", "Запись сохранена в дневник!")

    def load_notes(self):
        self.notes_list.clear()

        notes = self.db.get_notes()

        for note in notes:
            display_text = f"✍ {note[1]} | {note[3]}"
            item = QListWidgetItem(display_text)

            item.setData(Qt.ItemDataRole.UserRole, note)
            self.notes_list.addItem(item)

    def read_note(self, item):
        note = item.data(Qt.ItemDataRole.UserRole)

        self.current_note_id = note[0]

        self.title_input.setText(note[1])
        self.text_edit.setText(note[2])
        index = self.mood_combo.findText(note[3])
        if index >= 0:
            self.mood_combo.setCurrentIndex(index)

        self.stack.setCurrentIndex(2)

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

    def delete_selected_goal(self):
        current_row = self.goals_table.currentRow()

        if current_row < 0:
            QMessageBox.warning(
                self, "Ошибка", "Пожалуйста,сначала выберите цель в таблице!")
            return

        goal_id = int(self.goals_table.item(current_row, 0).text())
        goal_text = self.goals_table.item(current_row, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы уверены, что хотите удалить цель:\n'{goal_text}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_goal(goal_id):
                self.load_goals()
                QMessageBox.information(self, "Успех", "Цель удалена!")
            else:
                QMessageBox.critical(
                    self, "Ошибка", "Не удалось удалить цель из базы.")

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
        if index == 0:
            self.setStyleSheet("background-color: #2b2b2b; color: white;")
            self.setWindowIcon(QIcon("resources/icon_dark.png"))

        elif index == 1:
            self.setStyleSheet("background-color: #f0f0f0; color: black;")
            self.setWindowIcon(QIcon("resources/icon_light.png"))

        elif index == 2:
            self.setStyleSheet("background-color: #4a1515; color: #ffcccc;")
            self.setWindowIcon(QIcon("resources/icon_red.png"))

        elif index == 3:
            self.setStyleSheet("background-color: #1a2a40; color: #d0e0f0;")
            self.setWindowIcon(QIcon("resources/icon_blue.png"))

        elif index == 4:
            self.setStyleSheet("background-color: #f4e1e1; color: #4a2c2c;")
            self.setWindowIcon(QIcon("resources/icon_pink.png"))

        elif index == 5:
            self.setStyleSheet("background-color: #3e2a20; color: #f0e6d2;")
            self.setWindowIcon(QIcon("resources/icon_brown.png"))

        self.db.set_setting("theme_index", str(index))

    def clear_diary(self):
        reply = QMessageBox.question(
            self, "ВНИМАНИЕ!",
            "Вы уверены,что хотите удалить ВСЕ записи?\nЭто действие нельзя отменить!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_all_notes():
                self.load_notes()
                QMessageBox.information(
                    self, "Успех", "Дневник полностью очищен.")
            else:
                QMessageBox.critical(
                    self, "Ошибка", "Не удалось очистить дневник.")

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Выход', 'Вы уверены, что хотите закрыть Umbra?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
