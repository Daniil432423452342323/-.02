try:
    price = float(input("Введите цену товара (руб.): "))
    percent = float(input("Введите скидку (%): "))
    
    # Расчет цены со скидкой
    final_price = price * (1 - percent / 100)
    
    print(f"Цена со скидкой: {final_price:.2f} руб.")
except ValueError:
    print("Ошибка: Пожалуйста, вводите только числа.")
