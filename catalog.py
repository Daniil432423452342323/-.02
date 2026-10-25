"""Каталог товаров и задач с полной обработкой полей, краш-тестами, индикаторами и формой просмотра."""
import tkinter as tk
from app_resources import get_product_image  # Импорт нашего рабочего модуля ресурсов

def create_product_card(parent, product, refresh=None):
    """Создаёт карточку по макету КИМ с поддержкой callback-обновления."""
    # Извлекаем шестое поле (индекс 6). Это либо статус задачи (строка), либо количество товара (число)
    if isinstance(product, (list, tuple)):
        qty_or_status = product[6] if len(product) > 6 and product[6] is not None else 0
    else:
        qty_or_status = product if product is not None else 0
    
    # Синхронное определение фона карточки
    bg_color = _get_card_color(qty_or_status)
    
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)
    
    # Модульное добавление компонентов карточки (Рефакторинг)
    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty_or_status)

    # === ИНТЕГРАЦИЯ КЛИКА И REFRESH-СВЯЗИ (Пара 19, 20, 23) ===
    def _open_view(event):
        from view_form import ViewForm
        # Передаем ссылку на функцию обновления экрана дальше в окно просмотра
        ViewForm(parent, product, on_add_to_order=refresh)

    # Привязываем клик мыши к самой карточке и всем её дочерним элементам
    card.bind("<Button-1>", _open_view)
    for child in card.winfo_children():
        child.bind("<Button-1>", _open_view)
    # ==========================================================

    return card

def _get_card_color(qty_or_status):
    """Возвращает точный сигнальный цвет КИМ при дефиците, новой задаче или белом фоне."""
    # Если на вход пришла строка статуса задачи (проект Даниила)
    if isinstance(qty_or_status, str):
        if qty_or_status == "Новая":
            return "#ff8080"  # Красный фон для новых/срочных задач
        elif qty_or_status == "Выполнена":
            return "#E0E0E0"  # Серый фон для завершенных задач
        return "#FFFFFF"      # Белый фон для задач в процессе
        
    # Если на вход пришло число количества товара (Оригинальный КИМ Обуви)
    try:
        val = int(qty_or_status)
        return "#ff8080" if val <= 3 else "#FFFFFF"
    except (ValueError, TypeError):
        return "#FFFFFF"

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

def _add_text_info(card, product, bg_color, qty_or_status):
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
    
    # Если это проект ЗАДАЧ, переопределяем вывод текстов строк под интерфейс Даниила
    if len(product) == 7 and isinstance(qty_or_status, str):
        _add_label(text_frame, f"[{category}] | {name}", bg_color, bold=True, size=14)
        _add_label(text_frame, f"Срок контроля: {production}", bg_color)
        _add_label(text_frame, f"Описание: {composition}", bg_color)
        _add_label(text_frame, f"Статус: {qty_or_status}", bg_color, bold=True)
        return

    # Стандартный вывод для оригинального КИМ Обуви
    _add_label(text_frame, f"{production} | {name}", bg_color, bold=True, size=14)
    _add_label(text_frame, f"Категория: {category}", bg_color)
    indicator_text = _indicator(qty_or_status)
    _add_label(text_frame, f"Количество: {indicator_text} ({qty_or_status})", bg_color)
    _add_label(text_frame, f"Состав: {composition}", bg_color)
    _add_label(text_frame, f"{price} руб.", bg_color, bold=True, size=14, align="e")

def _add_label(parent, text, bg_color, bold=False, size=12, align="w"):
    """Универсальная функция добавления текстовой метки с фиксированным шрифтом Calibri."""
    tk.Label(parent, text=text, font=("Calibri", size, "bold" if bold else "normal"), bg=bg_color, anchor=align).pack(fill="x")

def _indicator(qty):
    """Индикатор остатка «много/мало» по строгому порогу КИМ (Пара 13)."""
    try:
        val = int(qty)
        return "много" if val > 5 else "мало"
    except (ValueError, TypeError):
        return "мало"
