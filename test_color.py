"""Тестирование сигнальной подсветки."""
from catalog import _get_card_color

def test_color():
    """Прогон тестов для подсветки товаров."""
    COLOR_MAIN_BG = "#FFFFFF"
    COLOR_HIGHLIGHT = "#ff8080"
    
    test_cases = [
        (10, COLOR_MAIN_BG, "10 > 3 — нет подсветки"),
        (5, COLOR_MAIN_BG, "5 > 3 — нет подсветки"),
        (4, COLOR_MAIN_BG, "4 > 3 — нет подсветки"),
        (3, COLOR_HIGHLIGHT, "3 ≤ 3 — подсветка (граница КИМ!)"),
        (2, COLOR_HIGHLIGHT, "2 ≤ 3 — подсветка"),
        (0, COLOR_HIGHLIGHT, "0 ≤ 3 — подсветка"),
        
        # 📌 Домашнее задание
        (1000, COLOR_MAIN_BG, "Большое число — нет подсветки (ДЗ)"),
        (-1, COLOR_HIGHLIGHT, "Отрицательное число — подсветка (ДЗ)"),
    ]
    
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПОДСВЕТКИ КАРТОЧЕК")
    print("=" * 60)
    passed = 0
    
    for qty, expected, comment in test_cases:
        result = _get_card_color(qty)
        is_ok = (str(result).upper() == str(expected).upper())
        status = "✅" if is_ok else "❌"
        if is_ok:
            passed += 1
        print(f"{status} qty={str(qty).ljust(5)}: {result} (ожидалось {expected}) — {comment}")
        
    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")
    print("=" * 60)

# ⚠️ ВАЖНО: запуск функции
if __name__ == "__main__":
    test_color()
