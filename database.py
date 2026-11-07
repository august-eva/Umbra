import sqlite3
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self, db_name="umbra.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        print(f"Подключение к базе данных '{db_name}' установлено.")

    def create_tables(self):
        create_notes_query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            mood TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        create_goals_query = """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            deadline TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        create_goals_index_query = """
        CREATE INDEX IF NOT EXISTS idx_goals_deadline ON goals(deadline);
        """

        try:
            self.cursor.execute(create_notes_query)
            self.cursor.execute(create_goals_query)
            self.cursor.execute(create_goals_index_query)

            self.connection.commit()
            print("Таблицы 'notes' и 'goals' успешно созданы или уже существуют.")

        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Произошла ошибка при создании таблиц: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто.")


# Тест
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_tables()

    try:
        db_manager.cursor.execute(
            "INSERT INTO notes (text, mood) VALUES (?, ?)",
            ("Изучить документацию sqlite3", "продуктивное")
        )

        future_date = (datetime.now() + timedelta(days=365)
                       ).strftime('%Y-%m-%d')
        db_manager.cursor.execute(
            "INSERT INTO goals (text, deadline) VALUES (?, ?)",
            ("Написать книгу", future_date)
        )

        db_manager.connection.commit()

        print("\nТекущие заметки:")
        for row in db_manager.cursor.execute("SELECT id, text, mood, created_at FROM notes"):
            print(row)

        print("\nТекущие цели:")
        for row in db_manager.cursor.execute("SELECT id, text, deadline FROM goals"):
            print(row)
    finally:
        db_manager.close()
