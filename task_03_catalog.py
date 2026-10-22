catalog = [
    {"name": "Кроссовки", "price": 8500, "qty": 3},
    {"name": "Ботинки", "price": 15000, "qty": 1},
    {"name": "Туфли", "price": 12000, "qty": 5},
    {"name": "Сандалии", "price": 4500, "qty": 8},
    {"name": "Кеды", "price": 6000, "qty": 2}
]

print("Каталог товаров:")
total_sum = 0

for i, item in enumerate(catalog, 1):
    item_total = item["price"] * item["qty"]
    total_sum += item_total
    print(f"{i}. {item['name'].ljust(10)} — {item['price']} × {item['qty']} = {item_total} руб.")

print("-" * 30)
print(f"Итоговая стоимость: {total_sum} руб.")
