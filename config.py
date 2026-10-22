"""Настройки проекта."""
import os

# Автоматическое определение пути к папке проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Железобетонный путь к базе данных 27-го варианта
DB_PATH = os.path.join(BASE_DIR, "databases", "db_variant_27.db")
