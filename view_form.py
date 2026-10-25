"""Модуль графической формы детального просмотра объектов (товаров и задач)."""
import tkinter as tk
from tkinter import ttk, messagebox
from app_resources import get_product_image

class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        
        self.window = tk.Toplevel(parent)
        self.window.configure(bg="#FFFFFF")
        self.window.grab_set()  # Делаем окно модальным
        
        # Определяем, что перед нами: задача (7 полей) или товар
        self.is_task = len(product) == 7 and isinstance(product[1], str)
        
        if self.is_task:
            self.window.title(f"Просмотр задачи — {product[1]}")
            self.window.geometry("600x450")
        else:
            self.window.title(f"Просмотр товара — {product[1] if len(product) > 1 else 'Товар'}")
            self.window.geometry("750x600")
            
        self.build_ui()
    
    def build_ui(self):
        # Верхняя шапка
        header = tk.Frame(self.window, bg="#D2F6E7", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_text = "ДЕТАЛЬНАЯ КАРТОЧКА ЗАДАЧИ" if self.is_task else "ДЕТАЛЬНАЯ КАРТОЧКА ТОВАРА"
        tk.Label(header, text=title_text, font=("Calibri", 16, "bold"), bg="#D2F6E7").pack(pady=15)
        
        # Центральная область
        main = tk.Frame(self.window, bg="#FFFFFF")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        if self.is_task:
            # === РЕНДЕРИНГ ДЛЯ ЗАДАЧИ ===
            info_frame = tk.Frame(main, bg="#FFFFFF")
            info_frame.pack(fill="both", expand=True, padx=10)
            
            self._add_field(info_frame, "Название задачи", self.product[1])
            self._add_field(info_frame, "Категория", self.product[3])
            self._add_field(info_frame, "Приоритет", self.product[4])
            self._add_field(info_frame, "Срок выполнения", self.product[5])
            self._add_field(info_frame, "Текущий статус", self.product[6])
            self._add_field(info_frame, "Описание", self.product[2])
        else:
            # === РЕНДЕРИНГ ДЛЯ ТОВАРА (КИМ) ===
            img_frame = tk.Frame(main, bg="#FFFFFF")
            img_frame.pack(side="left", anchor="n", padx=10)
            
            image_path = self.product[7] if len(self.product) > 7 else None
            photo = get_product_image(image_path, size=(220, 220))
            if photo:
                img_label = tk.Label(img_frame, image=photo, bg="#FFFFFF")
                img_label.image = photo
                img_label.pack()
                
            info_frame = tk.Frame(main, bg="#FFFFFF")
            info_frame.pack(side="left", fill="both", expand=True, padx=20)
            
            self._add_field(info_frame, "Наименование", self.product[1])
            self._add_field(info_frame, "Производство", self.product[3])
            self._add_field(info_frame, "Категория", self.product[2])
            self._add_field(info_frame, "Состав материала", self.product[4])
            self._add_field(info_frame, "Цена со скидкой", f"{self.product[5]} руб.")
            self._add_field(info_frame, "Размерный ряд", self.product[8] if len(self.product) > 8 else "Не указан")

        # Панель кнопок (снизу)
        btn_frame = tk.Frame(self.window, bg="#FFFFFF")
        btn_frame.pack(fill="x", side="bottom", pady=20, padx=20)
        
        if not self.is_task:
            btn_order = tk.Button(btn_frame, text="Добавить в заказ", bg="#70B2AF", fg="white",
                                  font=("Calibri", 12, "bold"), relief="flat", padx=15, command=self.add_to_order)
            btn_order.pack(side="left")
        
        btn_back = tk.Button(btn_frame, text="Закрыть окно", bg="#E0E0E0", fg="black",
                             font=("Calibri", 12), relief="flat", padx=15, command=self.window.destroy)
        btn_back.pack(side="right")

    def _add_field(self, parent, label, value):
        row = tk.Frame(parent, bg="#FFFFFF")
        row.pack(fill="x", pady=5)
        tk.Label(row, text=f"{label}:".ljust(18), font=("Calibri", 11, "bold"), bg="#FFFFFF", anchor="w", width=15).pack(side="left")
        tk.Label(row, text=str(value), font=("Calibri", 11), bg="#FFFFFF", anchor="w", justify="left", wraplength=400).pack(side="left", fill="x", expand=True)

    def add_to_order(self):
        if not self.on_add_to_order:
            messagebox.showinfo("Информация", "Функция формирования заказов находится в разработке.")
            return
        try:
            self.on_add_to_order(self.product)
            messagebox.showinfo("Успех", "Товар успешно добавлен в корзину!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обработать операцию:\n{e}")
