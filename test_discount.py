"""Тестирование алгоритма скидки под данные 27-го варианта."""
from datetime import datetime
from discount import calculate_price_with_discount

def run_tests():
    """Прогон тест-кейсов."""
    # Точка отсчета — октябрь 2026 (проверяем сентябрь)
    date = datetime(2026, 10, 15)
    
    test_cases = [
        # (id, базовая_цена, ожидаемая_цена, описание)
        (1, 1000, 1000, "Задача 1: Сделать отчёт — были назначения в сентябре (назн. №3)"),
        (2, 2000, 2000, "Задача 2: Сдать ДЭ — были назначения в сентябре (назн. №2)"),
        (3, 3000, 3000, "Задача 3: Купить продукты — были назначения в сентябре (назн. №1)"),
        (4, 4000, 3000, "Задача 4: Позвонить клиенту — нет назначений в сентябре → скидка 25%"),
        (5, 5000, 3750, "Задача 5: Прочитать книгу — нет назначений в сентябре → скидка 25%"),
    ]
    
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (ООП-МОДЕЛЬ)")
    print("=" * 70)
    passed = 0
    
    for task_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(task_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Задача №{task_id}: {price} руб. ➔ {result} руб. (Ожидалось: {expected})")
        print(f"   Пояснение: {comment}\n")
        
    print("=" * 70)
    print(f"Результат тестирования: Пройдено {passed} / {len(test_cases)}")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
