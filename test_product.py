"""Проверка класса Task."""
from models import Task

# Создаём одну тестовую задачу вручную
t = Task(
    task_id=1,
    category="Учёба",
    name="Сдать ДЭ",
    desc="Подготовиться к демоэкзамену",
    date="2026-10-15",
    status="Не начата",
    priority="Высокий"
)

print(t.info())
print(f"Требует выполнения? (is_available): {t.is_available()}")
