"""Комплексный автоматизированный скрипт тестирования (Пара 14 и Пара 15)."""
from catalog import _get_card_color, _indicator

def run_comprehensive_tests():
    """Запуск расширенного тест-пака граничных и крайних случаев."""
    # Точные HEX-коды из требований КИМ
    COLOR_MAIN_BG = "#FFFFFF"       # основной белый фон
    COLOR_HIGHLIGHT = "#ff8080"     # светло-красная подсветка дефицита
    
    test_cases = [
        # (qty, expected_color, expected_indicator, comment)
        (1000, COLOR_MAIN_BG, "много", "ДЗ: Огромная партия товара"),
        (50, COLOR_MAIN_BG, "много", "ДЗ: Стандартная поставка"),
        (6, COLOR_MAIN_BG, "много", "Верхняя граница индикатора (qty > 5)"),
        (5, COLOR_MAIN_BG, "мало", "Точная граница индикатора (qty <= 5)"),
        (4, COLOR_MAIN_BG, "мало", "Значение между порогами 3 и 5"),
        (3, COLOR_HIGHLIGHT, "мало", "Точная граница подсветки (qty <= 3)"),
        (1, COLOR_HIGHLIGHT, "мало", "Критический остаток на складе"),
        (0, COLOR_HIGHLIGHT, "мало", "Товар полностью отсутствует (qty = 0)"),
        (-5, COLOR_HIGHLIGHT, "мало", "ДЗ: Отрицательное количество (Ошибки БД)"),
    ]
    
    print("=" * 80)
    print("        ЗАПУСК КОМПЛЕКСНОЙ ОТЛАДКИ И ТЕСТИРОВАНИЯ (ПАРА 14 И 15)")
    print("=" * 80)
    passed = 0
    
    for qty, exp_color, exp_ind, comment in test_cases:
        res_color = _get_card_color(qty)
        res_ind = _indicator(qty)
        
        # Переводим оба цвета в верхний регистр для точности сравнения
        color_ok = (str(res_color).upper() == str(exp_color).upper())
        ind_ok = (res_ind == exp_ind)
        
        if color_ok and ind_ok:
            status = "✅ УСПЕХ"
            passed += 1
        else:
            status = "❌ СБОЙ "
            
        print(f"{status} Ост: {str(qty).ljust(5)} | Цвет: {res_color} | Инд: {res_ind.ljust(5)} ➔ {comment}")
        
    print("=" * 80)
    print(f"ИТОГОВЫЙ РЕЗУЛЬТАТ: Пройдено успешно тестов {passed} из {len(test_cases)}")
    print("=" * 80)

if __name__ == "__main__":
    run_comprehensive_tests()
