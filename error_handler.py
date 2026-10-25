"""Модуль централизованной обработки исключений и валидации данных."""
from tkinter import messagebox

def safe_call(func, *args, **kwargs):
    """
    Безопасно вызывает переданную функцию, перехватывая любые исключения.
    
    :return: Результат функции или None в случае падения
    """
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Ошибка файла", f"Критический ресурс не найден:\n{e}")
    except ConnectionError as e:
        messagebox.showerror("Ошибка сети", f"Сбой подключения к серверу или базе данных:\n{e}")
    except ValueError as e:
        messagebox.showwarning("Предупреждение данных", f"Некорректный формат параметров:\n{e}")
    except Exception as e:
        messagebox.showerror("Критический сбой", f"Непредвиденная системная ошибка:\n{e}")
    return None

def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, является ли переданная строка положительным целым числом.
    
    :return: Кортеж (True, число) или (False, сообщение об ошибке)
    """
    try:
        number = int(value)
        if number <= 0:
            return (False, f"Поле '{field_name}' должно содержать число больше нуля.")
        return (True, number)
    except ValueError:
        return (False, f"Поле '{field_name}' должно быть корректным целым числом.")
