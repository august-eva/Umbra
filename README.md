# 🌒 Umbra (Эстетичный дневник / Aesthetic Diary)

**🌐 Выберите язык описания / Choose description language / Elige el idioma:**
[🇷🇺 Русский](#русский) | [🇬🇧 English](#english) | [🇪🇸 Español](#español)

---

## 🇷🇺 Русский

> **Umbra** — это десктопное приложение для ведения личного дневника и трекинга целей в эстетике *Dark Academia*. 
> Программа создает безопасную, уютную и визуально приятную среду для рефлексии, анализа настроения и планирования будущего.

### 🛠️ Стек технологий
* **Язык:** Python
* **Интерфейс:** PyQt6 (QSS стилизация)
* **База данных:** SQLite3
* **Сборка:** PyInstaller

### ✨ Главные фичи
* **Множество тем:** Смена оформления (Темная, Светлая, Красная, Розовая и др.) с изменением фоновых картинок и иконки самого окна.
* **Умный дневник:** При сохранении записи приложение анализирует выбранное настроение и выдает случайную фразу поддержки (модуль `random`).
* **Трекинг целей:** Таблица для отслеживания дедлайнов и статусов задач.
* **Экспорт данных:** Возможность выгрузить все свои записи в обычный текстовый файл `.txt` в один клик.
* **ООП:** Вся работа с базой данных инкапсулирована в классе `DatabaseManager`.

### ⚙️ Как запустить проект (Инструкция для терминала)

Перед первым запуском программы обязательно нужно настроить виртуальное окружение, чтобы не засорять систему лишними библиотеками.

1. Откройте проект в VS Code.
2. Откройте новый терминал (в VS Code: `Terminal` -> `New Terminal`).
3. Создайте виртуальное окружение (в папке проекта):
   ```bash
   python -m venv .venv
```

4. Активируйте окружение (для Windows):
   ```bash
   .venv\Scripts\activate
   ```
   (Для Mac/Linux команда будет: source .venv/bin/activate)
5. Установите все нужные библиотеки (PyQt6):
   ```bash
   pip install -r requirements.txt
   ```
   (или напрямую: pip install PyQt6)
6. Запустите приложение:
   ```bash
   python main.py
   ```

---

🇬🇧 English

Umbra is a desktop application for keeping a personal diary and goal tracking with a Dark Academia aesthetic. 
The app creates a safe, cozy, and visually pleasing environment for reflection, mood analysis, and future planning.

🛠️ Tech Stack

· Language: Python
· UI: PyQt6 (QSS styling)
· Database: SQLite3
· Build: PyInstaller

✨ Key Features

· Multiple Themes: Change UI (Dark, Light, Red, Pink, etc.) with dynamic background images and window icons.
· Smart Diary: When saving a note, the app analyzes the selected mood and generates a random support phrase (using the random module).
· Goal Tracking: A table to track deadlines and task statuses.
· Data Export: Export all your notes to a plain .txt file in one click.
· OOP: All database logic is encapsulated in the DatabaseManager class.

⚙️ How to Run (Terminal Instructions)

Before running the app for the first time, you must set up a virtual environment.

1. Open the project in VS Code.
2. Open a new terminal (Terminal -> New Terminal).
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the environment (Windows):
   ```bash
   .venv\Scripts\activate
   ```
   (For Mac/Linux: source .venv/bin/activate)
5. Install dependencies (PyQt6):
   ```bash
   pip install -r requirements.txt
   ```
6. Run the app:
   ```bash
   python main.py
   ```

---

🇪🇸 Español

Umbra es una aplicación de escritorio para llevar un diario personal y establecer metas con una estética Dark Academia. 
La aplicación crea un entorno seguro, acogedor y visualmente agradable para la reflexión, el análisis del estado de ánimo y la planificación del futuro.

🛠️ Tecnologías

· Lenguaje: Python
· Interfaz: PyQt6 (estilos QSS)
· Base de datos: SQLite3
· Compilación: PyInstaller

✨ Características principales

· Múltiples temas: Cambio de diseño (Oscuro, Claro, Rojo, Rosa, etc.) con imágenes de fondo dinámicas e iconos de ventana.
· Diario inteligente: Al guardar una nota, la aplicación analiza el estado de ánimo y genera una frase de apoyo aleatoria (módulo random).
· Seguimiento de metas: Una tabla para rastrear fechas límite y estados de las tareas.
· Exportación de datos: Exporta todas tus notas a un archivo .txt con un solo clic.
· POO: Toda la lógica de la base de datos está encapsulada en la clase DatabaseManager.

⚙️ Cómo ejecutar (Instrucciones de terminal)

Antes de ejecutar la aplicación por primera vez, debe configurar un entorno virtual.

1. Abra el proyecto en VS Code.
2. Abra una nueva terminal (Terminal -> New Terminal).
3. Cree un entorno virtual:
   ```bash
   python -m venv .venv
   ```
4. Active el entorno (Windows):
   ```bash
   .venv\Scripts\activate
   ```
   (Para Mac/Linux: source .venv/bin/activate)
5. Instale las dependencias (PyQt6):
   ```bash
   pip install -r requirements.txt
   ```
6. Ejecute la aplicación:
   ```bash
   python main.py
   ```

---

Автор / Author: Ева Август (Eva August)