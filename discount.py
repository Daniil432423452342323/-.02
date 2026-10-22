"""Модуль расчёта скидки для залежавшихся задач."""
from datetime import datetime, timedelta
import sqlite3
from config import DB_PATH

def get_previous_month_range(date):
    """
    Возвращает (начало, конец) предыдущего календарного месяца.
    Пример: 15.10.2026 -> ("2026-09-01", "2026-09-30")
    """
    first_day = date.replace(day=1)
    last_day_prev = first_day - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    return (
        first_day_prev.strftime("%Y-%m-%d"),
        last_day_prev.strftime("%Y-%m-%d")
    )

def has_orders_in_previous_month(task_id, date):
    """Есть ли назначения (заказы) по этой задаче в предыдущем месяце?"""
    start, end = get_previous_month_range(date)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Ищем назначения в таблице Заказ по товар_id
    cur.execute(
        "SELECT COUNT(*) FROM Заказ "
        "WHERE товар_id = ? AND дата BETWEEN ? AND ?",
        (task_id, start, end)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count > 0

def calculate_price_with_discount(task_id, price, date):
    """Рассчитывает условную стоимость со скидкой 25%, если назначений не было."""
    if has_orders_in_previous_month(task_id, date):
        return price  # Назначения были -> скидки нет
    return price * 0.75  # Назначений не было -> скидка 25%
