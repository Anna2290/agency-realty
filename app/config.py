"""Конфигурация приложения."""

from pathlib import Path

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Путь к файлу базы данных SQLite
DB_PATH = BASE_DIR / "agency_realty.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Настройки экспорта
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

# Настройки UI
APP_TITLE = "ИС «Агентство недвижимости»"
WINDOW_SIZE = "1200x700"
FONT_MAIN = ("Arial", 11)
FONT_HEADER = ("Arial", 14, "bold")
