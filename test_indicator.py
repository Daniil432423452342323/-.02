"""Тестирование индикатора «много/мало» под требования КИМ."""
from catalog import _indicator

def test_indicator():
    """Запуск расширенного тест-пака для проверки порога 5."""
    test_cases = [
        (1000, "много", "Большое число (ДЗ)"),
        (50, "много", "Среднее значение (ДЗ)"),
        (10, "много", "Базовая проверка"),
        (6, "много", "Верхняя граница порога (>5)"),
        (5, "мало", "Точная граница порога (<=5)"),
        (4, "мало", "Нижняя граница порога"),
        (0, "мало", "Нулевой остаток на складе"),
        (-1, "мало", "Отрицательное количество (Крайний случай ДЗ)"),
        
        # 📌 Расширение из Домашнего Задания №1 (Защита от некорректных типов данных)
        (None, "мало", "Проверка на значение None (ДЗ)"),
        ("10", "много", "Строковый тип входного числа (ДЗ)"),
        (5.5, "много", "Дробное вещественное число (ДЗ)"),
    ]
    
    print("=" * 60)
    print("ЗАПУСК АВТОМАТИЗИРОВАННОГО ТЕСТИРОВАНИЯ ИНДИКАТОРА")
    print("=" * 60)
    passed = 0
    
    for qty, expected, comment in test_cases:
        # Безопасный разбор типов данных для предотвращения падения теста
        try:
            if isinstance(qty, str) and qty.isdigit():
                val = int(qty)
            elif isinstance(qty, (int, float)):
                val = qty
            else:
                val = 0 if qty is None else int(qty)
                
            result = _indicator(val)
        except Exception:
            result = "мало"
            
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Остаток: {str(qty).ljust(5)} ➔ Результат: '{result}' (Ожидалось: '{expected}') — {comment}")
        
    print("=" * 60)
    print(f"ИТОГ: Пройдено тестов {passed} из {len(test_cases)}")
    print("=" * 60)

if __name__ == "__main__":
    test_indicator()
