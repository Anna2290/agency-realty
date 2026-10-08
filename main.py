"""Точка входа в приложение ИС «Агентство недвижимости»."""

from app.database.connection import init_db
from app.database.seed import seed_database
from app.ui.main_window import MainWindow


def main() -> None:
    """Инициализирует БД и запускает главное окно приложения."""
    init_db()
    seed_database()
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
