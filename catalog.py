"""Каталог товаров с полной обработкой полей, краш-тестами и индикаторами."""
import tkinter as tk
import styles  # Импортируем весь модуль стилей, чтобы избежать ошибок кэша
from app_resources import get_product_image  # Исправленный импорт нашего модуля ресурсов

def create_product_card(parent, product):
    """Создаёт карточку товара по макету КИМ."""
    # Безопасное извлечение количества (работает и с кортежем из БД, и с одиночным числом)
    if isinstance(product, (list, tuple)):
        qty = product[6] if len(product) > 6 and product[6] is not None else 0
    else:
        qty = product if product is not None else 0
    
    # Синхронное определение фона (Пара 10, 12, 13)
    bg_color = _get_card_color(qty)
    
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)
    
    # Модульное добавление компонентов карточки (Рефакторинг)
    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)
    return card

def _get_card_color(qty):
    """Возвращает красный цвет при дефиците (<=3), иначе белый."""
    return styles.COLOR_HIGHLIGHT if qty <= 3 else styles.COLOR_MAIN_BG

def _add_image(card, product, bg_color):
    """Добавляет изображение или безопасную заглушку."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)
    
    # Безопасное получение пути к изображению
    image_path = None
    if isinstance(product, (list, tuple)):
        image_path = product[7] if len(product) > 7 else None
        
    photo = get_product_image(image_path, size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color, width=10, height=5).pack()

def _add_text_info(card, product, bg_color, qty):
    """Отображает все текстовые поля из БД с защитой от пустых значений."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # Дефолтные значения на случай краш-теста (если передан не кортеж данных)
    name, category, production, composition, price = "[Без названия]", "[Без категории]", "[Без производства]", "[Не указан]", 0
    
    # Если на вход пришел полноценный кортеж из БД — разбираем его поля по макету КИМ
    if isinstance(product, (list, tuple)):
        name = product[1] if len(product) > 1 and product[1] else "[Без названия]"
        category = product[2] if len(product) > 2 and product[2] else "[Без категории]"
        production = product[3] if len(product) > 3 and product[3] else "[Без производства]"
        composition = product[4] if len(product) > 4 and product[4] else "[Не указан]"
        price = product[5] if len(product) > 5 and product[5] is not None else 0
    
    # Строка 1: Производство | Наименование по макету
    _add_label(text_frame, f"{production} | {name}", bg_color, bold=True, size=styles.FONT_SIZE_HEADER)
    
    # Строка 2: Категория
    _add_label(text_frame, f"Категория: {category}", bg_color)
    
    # Строка 3: Количество с текстовым индикатором (Пара 13)
    indicator_text = _indicator(qty)
    _add_label(text_frame, f"Количество: {indicator_text} ({qty})", bg_color)
    
    # Строка 4: Состав
    _add_label(text_frame, f"Состав: {composition}", bg_color)
    
    # Строка 5: Цена (выровнена по правому краю макета)
    _add_label(text_frame, f"{price} руб.", bg_color, bold=True, size=styles.FONT_SIZE_HEADER, align="e")

def _add_label(parent, text, bg_color, bold=False, size=None, align="w"):
    """Универсальная функция добавления текстовой метки."""
    if size is None:
        size = styles.FONT_SIZE_NORMAL
    tk.Label(parent, text=text, font=styles.font(size, bold=bold), bg=bg_color, anchor=align).pack(fill="x")

def _indicator(qty):
    """Индикатор остатка «много/мало» по строгому порогу КИМ (Пара 13)."""
    return "много" if qty > 5 else "мало"
