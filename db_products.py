"""Загрузка задач из БД в объекты класса Task."""
import sqlite3
from config import DB_PATH
from models import Task

def get_real_table_name():
    """Автоматически находит настоящее имя таблицы задач."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]
    conn.close()
    for t in tables:
        if 'Товар' in t:
            return t
    return "Товар "

TABLE = get_real_table_name()

def get_all_products():
    """Возвращает список объектов Task из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM [{TABLE}] ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    
    tasks = []
    for row in rows:
        # Превращаем сырую строку БД в объект класса Task
        task = Task(
            task_id=row[0],
            category=row[1],
            name=row[2],
            desc=row[3],
            date=row[4],
            status=row[5],
            priority=row[6]
        )
        tasks.append(task)
    return tasks

def get_products_low_stock():
    """Задачи с ВЫСОКИМ приоритетом."""
    all_tasks = get_all_products()
    return [t for t in all_tasks if t.priority == "Высокий"]

def print_catalog_with_highlight(tasks_list):
    """Выводит задачи с подсветкой высокого приоритета."""
    print(f"\n{'=' * 70}")
    print(f"ПАНЕЛЬ ЗАДАЧ ООП ({len(tasks_list)} объектов)")
    print("=" * 70)
    for t in tasks_list:
        highlight = "⚠️" if t.priority == "Высокий" else "  "
        print(f"{highlight} {t.info()}")
    print("=" * 70)

if __name__ == "__main__":
    print("1. Все задачи (загружены как объекты класса Task):")
    print_catalog_with_highlight(get_all_products())
    
    print("\n2. Задачи, требующие немедленного внимания (Высокий приоритет):")
    print_catalog_with_highlight(get_products_low_stock())
