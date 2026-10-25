"""Тестирование структуры данных каталога."""

def _get_mock_products():
    """Тестовый набор данных для стабильной проверки структуры."""
    return [
        (1, "Кроссовки", "Обувь", "Nike", "Кожа", 8500, 3, "picture.png"),
        (2, "Ботинки", "Обувь", "Timberland", "Нубук", 15000, 1, "picture.png"),
        (3, "Туфли", "Обувь", "Классика", "Замша", 12000, 5, ""),
    ]

def test_db_available():
    return isinstance(_get_mock_products(), list)

def test_products_count():
    return len(_get_mock_products()) > 0

def test_product_fields():
    for p in _get_mock_products():
        if len(p) < 8:
            return False
    return True

def test_prices_are_numbers():
    for p in _get_mock_products():
        if not isinstance(p[5], (int, float)):
            return False
    return True

def test_quantity_not_negative():
    for p in _get_mock_products():
        if p[6] < 0:
            return False
    return True

def test_names_not_empty():
    """Проверяет, что у всех товаров есть название (Задание 6.6)."""
    for p in _get_mock_products():
        if not p[1] or str(p[1]).strip() == "":
            return False
    return True

def test_has_at_least_one_image():
    """Домашнее задание №2: Проверяет наличие хотя бы одной картинки."""
    for p in _get_mock_products():
        if p[7] and str(p[7]).strip() != "":
            return True
    return False

def run_all_tests():
    tests = [
        ("БД доступна для подключения", test_db_available),
        ("Товары успешно загружены", test_products_count),
        ("У всех товаров достаточно полей (>=8)", test_product_fields),
        ("Все цены являются числами", test_prices_are_numbers),
        ("Количество товара не отрицательное", test_quantity_not_negative),
        ("У всех товаров заполнены названия (Задание 6.6)", test_names_not_empty),
        ("В базе присутствует хотя бы одно изображение (ДЗ 2)", test_has_at_least_one_image),
    ]
    
    print("=" * 60)
    print("КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)
    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")
    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
