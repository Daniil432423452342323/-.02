import tkinter as tk
from tkinter import ttk, messagebox
import db_tasks  # Импортируем наш модуль работы с БД

# Инициализируем БД при старте приложения
db_tasks.init_tasks_db()

class TaskManagerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Управление задачами — УП.02")
        self.root.geometry("750x650")
        self.root.configure(bg="#F5F5F5")
        
        self.build_ui()
        self.load_tasks()

    def build_ui(self):
        # Шапка приложения (в стиле твоего проекта)
        header = tk.Frame(self.root, bg="#D2F6E7")
        header.pack(fill="x")
        
        tk.Label(header, text="АВТОМАТИЗАЦИЯ УПРАВЛЕНИЯ ЗАДАЧАМИ", 
                 font=("Calibri", 14, "bold"), bg="#D2F6E7", fg="#333").pack(pady=15)
        
        # Область вывода с прокруткой (Canvas + Scrollbar)
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def create_task_card(self, parent, task):
        """Создает карточку задачи по строгому макету."""
        task_id, title, desc, cat, priority, deadline, status = task
        
        # Подсветка: если приоритет "Высокий" и задача не выполнена — красим в светло-красный
        if priority == "Высокий" and status != "Выполнена":
            bg_color = "#ff8080"
        elif status == "Выполнена":
            bg_color = "#E0E0E0"  # Серый цвет для завершенных
        else:
            bg_color = "white"

        # Контейнер карточки
        card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
        card.pack(fill="x", padx=10, pady=5)
        
        # Верхняя строка: Категория | Название -------- Дедлайн
        top_text = f"[{cat}] | {title}"
        tk.Label(card, text=top_text, font=("Calibri", 12, "bold"), bg=bg_color, anchor="w").pack(fill="x", padx=10, pady=2)
        
        tk.Label(card, text=f"Срок до: {deadline}", font=("Calibri", 10, "italic"), bg=bg_color, anchor="e").pack(fill="x", padx=10)
        
        # Описание задачи
        tk.Label(card, text=f"Описание: {desc}", font=("Calibri", 11), bg=bg_color, anchor="w", justify="left", wraplength=550).pack(fill="x", padx=10, pady=5)
        
        # Нижняя строка: Статус и Кнопка смены статуса
        bottom_frame = tk.Frame(card, bg=bg_color)
        bottom_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(bottom_frame, text=f"Статус: {status}", font=("Calibri", 11, "bold"), bg=bg_color).pack(side="left")
        
        # Кнопка отображается только для невыполненных задач
        if status != "Выполнена":
            btn_done = tk.Button(bottom_frame, text="Завершить", bg="#70B2AF", fg="white", 
                                 command=lambda: self.complete_task(task_id))
            btn_done.pack(side="right")

    def load_tasks(self):
        """Загружает актуальные данные из SQLite."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
            
        tasks = db_tasks.get_all_tasks()
        for t in tasks:
            self.create_task_card(self.catalog_frame, t)

    def complete_task(self, task_id):
        """Меняет статус в БД и обновляет интерфейс."""
        db_tasks.update_task_status(task_id, "Выполнена")
        messagebox.showinfo("Успех", f"Задача №{task_id} переведена в статус 'Выполнена'!")
        self.load_tasks()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    TaskManagerWindow().run()
