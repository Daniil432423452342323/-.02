"""Модели данных для проекта автоматизации управления задачами."""
from datetime import datetime

class Task:
    """Класс, описывающий задачу в системе."""
    
    def __init__(self, task_id, category, name, desc, date, status, priority):
        self.id = task_id
        self.category = category
        self.name = name
        self.desc = desc
        self.date = date
        self.status = status
        self.priority = priority

    def is_urgent(self):
        """Индикатор срочности."""
        return "СРОЧНО" if self.priority == "Высокий" else "нормально"

    def is_available(self):
        """Домашнее задание 1: возвращает True, если задача ещё не выполнена."""
        return self.status != "Выполнена"

    def price_with_discount_auto(self, base_price, date_calc=None):
        """Цена со скидкой по алгоритму ДЭ (Задание 8)."""
        from discount import calculate_price_with_discount
        if date_calc is None:
            date_calc = datetime.now()
        return calculate_price_with_discount(self.id, base_price, date_calc)

    def discounted_price(self):
        """Цена со скидкой 25% (итоговое значение после разрешения конфликта)."""
        return 1000 * 0.75

    def info(self):
        """Строка с информацией о задаче."""
        return (
            f"Задача №{self.id}: {self.name} [{self.category}] — {self.status} "
            f"(Приоритет: {self.priority} -> {self.is_urgent()})"
        )


class Order:
    """Домашнее задание 2: Класс Заказ (назначение задачи)."""
    
    def __init__(self, order_id, date, client, task_obj, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product = task_obj  # Объект класса Task
        self.quantity = quantity

    def info(self):
        return f"Назначение №{self.id} от {self.date}: {self.client} выполняет задачу '{self.product.name}'"
