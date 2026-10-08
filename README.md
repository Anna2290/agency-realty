 # ИС «Агентство недвижимости»

Информационная система для подбора и учёта объектов недвижимости
(продажа/аренда), с фильтрацией под запросы клиентов и автоматическим
формированием коммерческих предложений.

## Технологии
# ИС «Агентство недвижимости»

Информационная система для подбора и учёта объектов недвижимости.

## Технологии
- Python 3.11
- Tkinter (GUI)
- SQLAlchemy 2.0 (ORM)
- SQLite (СУБД)
- reportlab (PDF)

## Установка
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Запуск
python main.py

## Логин
- admin / admin

## Структура
- `app/database/` — модели, подключение, seed
- `app/logic/` — бизнес-логика (сервисы)
- `app/ui/` — интерфейс (Tkinter)
- `app/utils/` — утилиты
- `tests/` — тесты- Python 3.11
- Tkinter (GUI)
- SQLAlchemy (ORM)
- SQLite (СУБД)
- reportlab (экспорт КП в PDF)

## Установка
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Запуск
python main.py

## Логин по умолчанию
- admin / admin
