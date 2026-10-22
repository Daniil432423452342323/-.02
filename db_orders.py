"""Загрузка назначений (заказов) из БД с использованием класса Order."""
import sqlite3
from config import DB_PATH
from models import Task, Order

def get_real_table_name():
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

def get_all_orders():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Загружаем заказы
    cur.execute("SELECT id, дата, клиент, товар_id, количество FROM Заказ ORDER BY id")
    order_rows = cur.fetchall()
    
    orders = []
    for row in order_rows:
        order_id, date, client, task_id, quantity = row
        
        # Для каждого заказа подгружаем саму задачу, чтобы создать объект Task
        cur.execute(f"SELECT * FROM [{TABLE}] WHERE id = ?", (task_id,))
        t_row = cur.fetchone()
        
        if t_row:
            task_obj = Task(t_row[0], t_row[1], t_row[2], t_row[3], t_row[4], t_row[5], t_row[6])
            # Создаем объект Order, куда передаем объект Task
            order = Order(order_id, date, client, task_obj, quantity)
            orders.append(order)
            
    conn.close()
    return orders

if __name__ == "__main__":
    print("\nСПИСОК НАЗНАЧЕННЫХ ЗАДАЧ (ИЗ БД):")
    print("=" * 70)
    for o in get_all_orders():
        print(o.info())
    print("=" * 70)
