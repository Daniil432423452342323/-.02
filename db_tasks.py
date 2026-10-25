import sqlite3

DB_PATH = "databases/db_variant_1.db"  # Укажи свою активную БД

def init_tasks_db():
    """Создает таблицу задач, если её еще нет."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            priority TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'Новая'
        )
    """)
    # Добавим несколько тестовых записей, если таблица пустая
    cursor.execute("SELECT COUNT(*) FROM app_tasks")
    if cursor.fetchone()[0] == 0:
        test_tasks = [
            ("Проверить ДЗ", "Убедиться, что файлы загружены на GitHub", "Учеба", "Высокий", "2026-10-26", "Новая"),
            ("Дописать catalog.py", "Исправить индексы под свой вариант", "Учеба", "Средний", "2026-10-27", "В процессе"),
            ("Загрузить практику", "Сделать коммит и push в репозиторий", "Учеба", "Высокий", "2026-10-25", "Новая")
        ]
        cursor.executemany("""
            INSERT INTO app_tasks (title, description, category, priority, deadline, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, test_tasks)
    conn.commit()
    conn.close()

def get_all_tasks():
    """Возвращает список всех задач."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, category, priority, deadline, status FROM app_tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, new_status):
    """Обновляет статус задачи по её ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE app_tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_tasks_db()
    print("База данных задач успешно инициализирована!")
