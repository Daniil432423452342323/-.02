catalog = [
    {"name": "Кроссовки", "price": 8500, "qty": 3},
    {"name": "Ботинки", "price": 15000, "qty": 1},
    {"name": "Туфли", "price": 12000, "qty": 5},
    {"name": "Сандалии", "price": 4500, "qty": 8},
    {"name": "Кеды", "price": 6000, "qty": 2}
]

# Сортировка: сначала те, у кого qty > 5 (много)
sorted_catalog = sorted(catalog, key=lambda x: x["qty"] > 5, reverse=True)

print("Каталог с индикатором остатка:")
for i, item in enumerate(sorted_catalog, 1):
    indicator = "много" if item["qty"] > 5 else "мало"
    print(f"{i}. {item['name'].ljust(10)} — {item['qty']} шт. → {indicator}")
