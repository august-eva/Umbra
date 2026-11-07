```markdown
# 🌒 Umbra (Эстетичный дневник)

**Выберите язык / Choose language / Elige el idioma:**
[🇷🇺 Русский](#-русский) | [🇬🇧 English](#-english) | [🇪🇸 Español](#-español)

---

## 🇷🇺 Русский

**Описание проекта:**
Umbra — это десктопное приложение для ведения личного дневника и трекинга целей в эстетике Dark Academia. Приложение создает безопасную и уютную цифровую среду, помогая пользователю не только записывать мысли, но и анализировать свое настроение, получать поддержку и визуально наслаждаться процессом.

**Стек технологий:** Python, PyQt6, SQLite3, PyInstaller.

### ✨ Особенности проекта:
*   **Мультиязычный интерфейс:** Описание проекта доступно на русском, английском и испанском языках.
*   **Эстетичный дизайн:** Поддержка 4 цветовых тем (Темная, Светлая, Синяя, Розовая) с возможностью смены фоновых изображений и иконок окна.
*   **Умный дневник:** При сохранении записи приложение анализирует выбранное настроение и генерирует случайную фразу поддержки (модуль `random`).
*   **Трекинг целей:** Удобная таблица для отслеживания дедлайнов и статусов выполнения задач.
*   **База данных SQLite:** Надежное локальное хранение всех записей (без необходимости подключения к интернету). Все запросы реализованы через класс `DatabaseManager` (принципы ООП).
*   **Экспорт данных:** Возможность выгрузить все записи дневника в текстовый файл (.txt) в один клик.

### 🚀 Планы на будущее:
*   Автоматическое сохранение даты и времени записи (с использованием модуля `datetime`).
*   Сохранение выбранной темы оформления в базу данных (чтобы при перезапуске настройки не сбрасывались).
*   Графики статистики настроения за месяц.
*   Синхронизация с облачными сервисами.

### 📂 Структура проекта:
```text
Umbra/
├── main.py              # Точка входа в приложение
├── ui_main.py           # Графический интерфейс (окна, кнопки)
├── database.py          # Логика работы с базой данных SQLite
├── requirements.txt     # Список зависимостей проекта
├── resources/           # Папка с картинками и иконками для тем
└── README.md            # Документация проекта
```

⚙️ Установка и запуск:

Перед первым запуском программы вам необходимо настроить окружение.

1. Откройте терминал в папке с проектом.
2. Создайте виртуальное окружение: python -m venv .venv
3. Активируйте его: .venv\Scripts\activate
4. Установите нужные библиотеки: pip install -r requirements.txt
5. Запустите приложение: python main.py

---

🇬🇧 English

Project Description:
Umbra is a desktop application for keeping a personal diary and setting goals, designed in a Dark Academia aesthetic. The app creates a safe and cozy digital environment, helping the user not only to write down thoughts, but also to analyze their mood, receive support, and visually enjoy the process.

Tech Stack: Python, PyQt6, SQLite3, PyInstaller.

✨ Key Features:

· Multilingual Interface: Project description is available in Russian, English, and Spanish.
· Aesthetic Design: Support for 4 color themes (Dark, Light, Blue, Pink) with the ability to change background images and window icons.
· Smart Diary: When saving a note, the app analyzes the selected mood and generates a random support phrase (using the random module).
· Goal Tracking: A convenient table to track deadlines and task completion statuses.
· SQLite Database: Reliable local storage for all notes (no internet connection required). All queries are implemented through the DatabaseManager class (OOP principles).
· Data Export: Ability to export all diary notes to a text file (.txt) in one click.

🚀 Future Roadmap:

· Automatic saving of date and time for each note (using datetime).
· Saving the selected theme to the database (so settings are not reset on restart).
· Mood statistics charts for the month.
· Cloud synchronization.

📂 Project Structure:

```text
Umbra/
├── main.py              # Application entry point
├── ui_main.py           # Graphical interface (windows, buttons)
├── database.py          # SQLite database logic