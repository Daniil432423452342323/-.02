"""Загрузка задач из БД с динамическим определением системного индекса таблицы."""
import sqlite3
from config import DB_PATH

def get_real_table_name():
    """Автоматически находит точное системное имя таблицы задач."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]
    conn.close()
    
    # Ищем таблицу, в имени которой содержится слово 'Товар'
    for t in tables:
        if 'Товар' in t:
            return t
    return None

# Переменная динамически хранит имя таблицы со всеми скрытыми байтами кодировки
TABLE = get_real_table_name()

def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Безопасное динамическое форматирование строки запроса
    query = f'SELECT * FROM "{TABLE}" ORDER BY id'
    cur.execute(query)
    products = cur.fetchall()
    conn.close()
    return products

def get_products_low_stock():
    """Вместо низкого остатка — задачи с ВЫСОКИМ приоритетом."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f'SELECT * FROM "{TABLE}" WHERE приоритет = "Высокий"'
    cur.execute(query)
    products = cur.fetchall()
    conn.close()
    return products

def get_categories():
    """Список всех категорий (Работа, Дом, Учёба)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f'SELECT DISTINCT категория FROM "{TABLE}" ORDER BY категория'
    cur.execute(query)
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories

def print_catalog(products):
    """Вывод списка задач с индикаторами."""
    print(f"\n{'=' * 70}")
    print(f"СПИСОК ЗАДАЧ АВТОМАТИЗАЦИИ ({len(products)} строк)")
    print("=" * 70)
    for p in products:
        # Четкая привязка к индексам вашей новой БД
        task_id = p[0]
        category = p[1]
        name = p[2]
        desc = p[3]
        date = p[4]
        status = p[5]
        priority = p[6]
        
        # Индикатор и подсветка по условию ДЭ
        highlight = "⚠️" if priority == "Высокий" else "  "
        indicator = "СРОЧНО" if priority == "Высокий" else "нормально"
        
        print(f"{highlight} {task_id}. {name} [{category}] — {status}")
        print(f"   Описание: {desc}")
        print(f"   Срок до: {date} | Приоритет: {priority} ({indicator})")
        print("-" * 70)

if __name__ == "__main__":
    if TABLE is None:
        print("❌ КРИТИЧЕСКАЯ ОШИБКА: Таблица со словом 'Товар' не найдена в файле базы данных!")
    else:
        print(f"🔍 Системное авто-определение сработало успешно!")
        print("\n1. Все задачи в системе:")
        print_catalog(get_all_products())
        
        print("\n2. Доступные категории контекста:")
        for cat in get_categories():
            print(f"   - {cat}")
            
        print("\n3. Задачи, требующие внимания (Высокий приоритет):")
        print_catalog(get_products_low_stock())
