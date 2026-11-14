import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QTextEdit, QComboBox, QHBoxLayout, QMessageBox,
    QListWidget, QLineEdit, QDateEdit, QTableWidget, QTableWidgetItem, QFileDialog, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate, QSettings
from PyQt6.QtGui import QIcon, QPalette, QBrush, QPixmap, QShortcut, QKeySequence
from database import DatabaseManager

TRANSLATIONS = {
    "ru": {
        "menu_title": "Добро пожаловать в Umbra 🌒",
        "btn_diary": "📖 Мой дневник",
        "btn_goals": "🎯 Мои цели",
        "btn_settings": "⚙️ Настройки",
        "back": "← Назад в меню",
        "save": "💾 Сохранить",
        "export": "📤 Экспорт дневника в TXT",
        "about": "ℹ️ О программе",
        "set_data": "Сохранение данных:",
        "set_view": "Внешний вид и язык:",
        "set_lang": "Язык интерфейса:",
        "set_theme": "Тема оформления:",
        "goal_ph": "Введите название цели...",
        "goal_col1": "Цель",
        "goal_col2": "Дедлайн",
        "note_title_ph": "Название записи...",
        "note_text_ph": "Напиши свои мысли здесь...",
        "msg_success": "Успех",
        "msg_saved": "Запись сохранена!",
        "msg_err_empty": "Заполни название и текст!",
        "msg_close_title": "Выход",
        "msg_close_text": "Вы уверены, что хотите закрыть Umbra?",
        "btn_cancel": "← Отмена",
        "btn_del_note": "🗑️ Удалить запись",
        "btn_new_note": "➕ Создать новую запись",
        "btn_add_goal": "➕ Добавить цель",
        "btn_del_goal": "🗑️ Удалить выбранную цель"
    },
    "en": {
        "menu_title": "Welcome to Umbra 🌒",
        "btn_diary": "📖 My Diary",
        "btn_goals": "🎯 My Goals",
        "btn_settings": "⚙️ Settings",
        "back": "← Back to Menu",
        "save": "💾 Save",
        "export": "📤 Export Diary to TXT",
        "about": "ℹ️ About",
        "set_data": "Data saving:",
        "set_view": "Appearance & Language:",
        "set_lang": "Interface language:",
        "set_theme": "Theme:",
        "goal_ph": "Enter goal name...",
        "goal_col1": "Goal",
        "goal_col2": "Deadline",
        "note_title_ph": "Note title...",
        "note_text_ph": "Write your thoughts here...",
        "msg_success": "Success",
        "msg_saved": "Note saved!",
        "msg_err_empty": "Fill in the title and text!",
        "msg_close_title": "Exit",
        "msg_close_text": "Are you sure you want to close Umbra?",
        "btn_cancel": "← Cancel",
        "btn_del_note": "🗑️ Delete note",
        "btn_new_note": "➕ Create new note",
        "btn_add_goal": "➕ Add goal",
        "btn_del_goal": "🗑️ Delete selected goal"
    },
    "es": {
        "menu_title": "Bienvenido a Umbra 🌒",
        "btn_diary": "📖 Mi Diario",
        "btn_goals": "🎯 Mis Metas",
        "btn_settings": "⚙️ Ajustes",
        "back": "← Volver al Menú",
        "save": "💾 Guardar",
        "export": "📤 Exportar Diario a TXT",
        "about": "ℹ️ Acerca de",
        "set_data": "Guardado de datos:",
        "set_view": "Apariencia e Idioma:",
        "set_lang": "Idioma de la interfaz:",
        "set_theme": "Tema:",
        "goal_ph": "Ingrese el nombre de la meta...",
        "goal_col1": "Meta",
        "goal_col2": "Fecha límite",
        "note_title_ph": "Título de la nota...",
        "note_text_ph": "Escribe tus pensamientos aquí...",
        "msg_success": "Éxito",
        "msg_saved": "¡Nota guardada!",
        "msg_err_empty": "¡Rellena el título y el texto!",
        "msg_close_title": "Salir",
        "msg_close_text": "¿Estás seguro de que quieres cerrar Umbra?",
        "btn_cancel": "← Cancelar",
        "btn_del_note": "🗑️ Eliminar nota",
        "btn_new_note": "➕ Crear nueva nota",
        "btn_add_goal": "➕ Añadir meta",
        "btn_del_goal": "🗑️ Eliminar meta seleccionada"
    }
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Umbra")
        self.resize(800, 600)
        self.db = DatabaseManager()
        self.current_lang = "ru"

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


# Главное меню

    def setup_menu_screen(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.label_title = QLabel("Добро пожаловать в Umbra 🌒")
        self.label_title.setStyleSheet(
            "font-size: 28px; font-weight: bold; margin-bottom: 30px;")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.btn_diary = QPushButton("📖 Мой дневник")
        self.btn_goals = QPushButton("🎯 Мои цели")
        self.btn_settings = QPushButton("⚙️ Настройки")

        for btn in [self.btn_diary, self.btn_goals, self.btn_settings]:
            btn.setFixedSize(250, 50)

        layout.addWidget(
            self.btn_diary, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(
            self.btn_goals, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_settings,
                         alignment=Qt.AlignmentFlag.AlignCenter)

        self.menu_screen.setLayout(layout)

        self.btn_diary.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_goals.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.btn_settings.clicked.connect(
            lambda: self.stack.setCurrentIndex(4))

    def setup_diary_list_screen(self):
        layout = QVBoxLayout()

        self.btn_back_diary = QPushButton("← Назад в меню")
        self.btn_back_diary.setFixedWidth(200)
        self.btn_back_diary.clicked.connect(
            lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.btn_back_diary)

        self.btn_new_note = QPushButton("📑Создать новую запись")
        self.btn_new_note.setFixedHeight(40)
        self.btn_new_note.clicked.connect(
            lambda: self.stack.setCurrentIndex(2))
        layout.addWidget(self.btn_new_note)

        self.notes_list = QListWidget()

        self.notes_list.itemClicked.connect(self.read_note)
        layout.addWidget(self.notes_list)

        self.diary_list_screen.setLayout(layout)


# Дневник


    def setup_diary_edit_screen(self):
        layout = QVBoxLayout()

        self.btn_cancel = QPushButton("← Отмена")
        self.btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(self.btn_cancel)

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

        self.btn_save_note = QPushButton("💾 Сохранить запись")
        self.btn_save_note.setFixedHeight(40)
        self.btn_save_note.clicked.connect(self.save_note)
        layout.addWidget(self.btn_save_note)

        self.btn_delete_note = QPushButton("🗑️Удалить запись")
        layout.addWidget(self.btn_delete_note)

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

        self.btn_back_goals = QPushButton("← Назад в меню")
        self.btn_back_goals.setFixedWidth(200)
        self.btn_back_goals.clicked.connect(
            lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.btn_back_goals)

        self.goal_input = QLineEdit()
        self.goal_input.setPlaceholderText("Введите название цели...")
        layout.addWidget(self.goal_input)

        goal_controls = QHBoxLayout()

        self.goal_date = QDateEdit()
        self.goal_date.setCalendarPopup(True)
        self.goal_date.setDate(QDate.currentDate())
        goal_controls.addWidget(self.goal_date)

        self.btn_add_goal = QPushButton("🖋 Добавить цель")
        goal_controls.addWidget(self.btn_add_goal)

        layout.addLayout(goal_controls)

        self.goals_table = QTableWidget()
        self.goals_table.setColumnCount(3)
        self.goals_table.setHorizontalHeaderLabels(["ID", "Цель", "Дедлайн"])
        self.goals_table.setColumnHidden(0, True)
        layout.addWidget(self.goals_table)

        self.btn_delete_goal = QPushButton("❗Удалить выбранную цель")
        layout.addWidget(self.btn_delete_goal)

        self.goals_screen.setLayout(layout)

# Настройки
    def setup_settings_screen(self):
        layout = QVBoxLayout()

        self.btn_back_setting = QPushButton("← Назад в меню")
        self.btn_back_setting.setFixedWidth(200)
        self.btn_back_setting.clicked.connect(
            lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.btn_back_setting)

        self.label_set_data = QLabel("Сохранение данных:")
        layout.addWidget(self.label_set_data)

        self.btn_export = QPushButton("📨Экспорт дневника в TXT")
        layout.addWidget(self.btn_export)

        self.label_set_view = QLabel("Внешний вид и язык:")
        layout.addWidget(self.label_set_view)

        self.label_set_lang = QLabel("Язык интерфейса:")
        layout.addWidget(self.label_set_lang)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "English", "Español"])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.lang_combo)

        self.label_set_theme = QLabel("Тема оформления:")
        layout.addWidget(self.label_set_theme)

        self.theme_combo = QComboBox()
        self, self.theme_combo.addItems(
            ["Темная тема", "Светлая тема", "Красная тема", "Синяя тема", "Розовая тема", "Коричневая тема"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)

        layout.addSpacing(20)
        self.btn_about = QPushButton("🚨О программе")
        self.btn_about.clicked.connect(self.show_about)
        layout.addWidget(self.btn_about)

        layout.addStretch()
        self.settings_screen.setLayout(layout)

    def show_support_phrase(self, mood):
        import random
        lang = self.current_lang

        phrases = SUPPORT_PHRASES[lang].get(mood, ["Дневник всегда рядом."])
        selected_phrase = random.choice(phrases)
        QMessageBox.information(self, "Поддержка", selected_phrase)

    def save_note(self):
        title = self.title_input.text().strip()
        text = self.text_edit.toPlainText().strip()
        mood = self.mood_combo.currentText()
        t = TRANSLATIONS[self.current_lang]

        if not title or not text:
            QMessageBox.warning(self, "Ошибка", t["msg_err_empty"])
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
        QMessageBox.information(self, t["msg_success"], t["msg_saved"])
        self.show_support_phrase(mood)

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

    def change_theme(self, index):
        print(f"Меняем язык на индекс: {index}")
        if index == 0:
            self.setWindowIcon(QIcon("resources/icon_dark.png"))
            menu_img, smoke_img, text_color = "bg_menu.png", "bg_smoke.png", "white"
        elif index == 1:
            self.setWindowIcon(QIcon("resources/icon_light.png"))
            menu_img, smoke_img, text_color = "bg_light_menu.png", "bg_light_smoke.png", "black"
        elif index == 2:
            self.setWindowIcon(QIcon("resources/icon_red.png"))
            menu_img, smoke_img, text_color = "bg_red_menu.png", "bg_red_smoke.png", "white"
        elif index == 3:
            self.setWindowIcon(QIcon("resources/icon_blue.png"))
            menu_img, smoke_img, text_color = "bg_blue_menu.png", "bg_blue_smoke.png", "white"
        elif index == 4:
            self.setWindowIcon(QIcon("resources/icon_pink.png"))
            menu_img, smoke_img, text_color = "bg_pink_menu.png", "bg_pink_smoke.png", "black"
        else:
            self.setWindowIcon(QIcon("resources/icon_brown.png"))
            menu_img, smoke_img, text_color = "bg_brown_menu.png", "bg_brown_smoke.png", "white"

        self.menu_screen.setStyleSheet(f"""
            QWidget {{
                background-image: url(resources/{menu_img});
            }}
        """)

        screens = [self.diary_list_screen, self.diary_edit_screen,
                   self.goals_screen, self.settings_screen]
        for screen in screens:
            screen.setStyleSheet(f"""
                QWidget {{
                    background-image: url(resources/{smoke_img});
                }}
            """)

        global_styles = f"""
            QLabel {{
                color: {text_color};
                background-color: transparent;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
            }}
            QPushButton {{
                background-color: rgba(20, 20, 20, 180);
                color: white;
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 12px; /* Сильное скругление кнопок */
                padding: 12px 20px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(60, 60, 60, 220); /* Светлеет при наведении */
                border: 1px solid rgba(255, 255, 255, 150);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 220); /* Темнеет при нажатии */
            }}
            QLineEdit, QTextEdit, QComboBox, QListWidget, QTableWidget {{
                background-color: rgba(20, 20, 20, 150);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 8px; /* Скругление полей ввода */
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }}

            QComboBox QAbstractItemView {{
                background-color: #1a1a1a; /* Темный фон списка */
                color: white;              /* Белый текст пунктов */
                border: 1px solid rgba(255, 255, 255, 50);
                selection-background-color: #8b0000; /* Красная подсветка при наведении */
                selection-color: white;
            }}

            QMessageBox {{
                background-color: #2b2b2b; /* Темный фон для окошка */
            }}
            QMessageBox QLabel {{
                color: white; /* Белый текст вопроса */
            }}
            QMessageBox QPushButton {{
                background-color: #444444;
                color: white;
                border-radius: 6px;
                padding: 6px 15px;
            }}
        """

        self.setStyleSheet(global_styles)

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

    def change_language(self, index):
        if index == 0:
            lang = "ru"
        elif index == 1:
            lang = "en"
        else:
            lang = "es"

        self.current_lang = lang
        t = TRANSLATIONS[lang]

# Главное меню
        self.label_title.setText(t["menu_title"])
        self.btn_diary.setText(t["btn_diary"])
        self.btn_goals.setText(t["btn_goals"])
        self.btn_settings.setText(t["btn_settings"])

# Кнопки назад
        self.btn_back_diary.setText(t["back"])
        self.btn_back_goals.setText(t["back"])
        self.btn_back_setting.setText(t["back"])

# Кнопки дейсвий
        self.btn_save_note.setText(t["save"])
        self.btn_export.setText(t["export"])

        self.btn_cancel.setText(t["btn_cancel"])
        self.btn_delete_note.setText(t["btn_del_note"])
        self.btn_new_note.setText(t["btn_new_note"])
        self.btn_add_goal.setText(t["btn_add_goal"])
        self.btn_delete_goal.setText(t["btn_del_goal"])

# Настройки
        self.label_set_data.setText(t["set_data"])
        self.label_set_view.setText(t["set_view"])
        self.label_set_lang.setText(t["set_lang"])
        self.label_set_theme.setText(t["set_theme"])

# Цели
        self.goal_input.setPlaceholderText(t["goal_ph"])
        self.goals_table.setHorizontalHeaderLabels(
            ["ID", t["goal_col1"], t["goal_col2"]]
        )

# Дневник
        self.title_input.setPlaceholderText(t["note_title_ph"])
        self.text_edit.setPlaceholderText(t["note_text_ph"])

# Настроения
        self.mood_combo.clear()
        if lang == "ru":
            self.mood_combo.addItems(
                ["Радость", "Грусть", "Вдохновение", "Злость"])
        elif lang == "en":
            self.mood_combo.addItems(
                ["Joy", "Sadness", "Inspiration", "Anger"])
        else:
            self.mood_combo.addItems(
                ["Alegría", "Tristeza", "Inspiración", "Ira"])

        self.btn_about.setText(t["about"])

# Темы
        self.theme_combo.clear()
        if lang == "ru":
            self.theme_combo.addItems(
                ["Темная тема", "Светлая тема", "Красная тема", "Синяя тема", "Розовая тема", "Коричневая тема"])
        elif lang == "en":
            self.theme_combo.addItems(
                ["Dark theme", "Light theme", "Red theme", "Blue theme", "Pink theme", "Brown theme"])
        else:
            self.theme_combo.addItems(
                ["Tema oscuro", "Tema claro", "Tema rojo", "Tema azul", "Tema rosa", "Tema marrón"])

        print("ПЕРЕВОД ЗАВЕРШЕН УСПЕШНО!")

    def closeEvent(self, event):
        t = TRANSLATIONS[self.current_lang]
        reply = QMessageBox.question(
            self, t["msg_close_title"], t["msg_close_text"],
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
