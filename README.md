# Bristol Mobile Barcode

**Bristol Mobile Barcode** — это асинхронный парсер для поиска товров по баркоду из интернет-магазина "Бристоль". Данные сохраняются в базу данных PostgreSQL.

## Функциональность

- Перебор возможных баркодов производителя
- Сбор данных товара по баркоду
- Сохранение данных в PostgreSQL
- Логирование и обработка ошибок
- Тестирование с pytest

---

## Установка и запуск

### 1. Клонируйте репозиторий

```sh
git clone https://github.com/Alab0/magnit_scraper.git
cd magnit_scraper
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта и добавьте туда настройки базы данных:

```ini
DB_HOST=host
DB_NAME=name
DB_USER=user
DB_PASSWORD=passwd
DB_PORT=port
API=api
```

---

## Структура проекта

```
bristol_mobile_barcode/
│── bristol_mobile_barcode/  
│   │── __init__.py
│   │── main.py        # Основной файл запуска парсера
│   │── fetcher.py     # Запрос к API Бристоля
│   │── database.py    # Работа с БД PostgreSQL
│   │── config.py      # Настройки проекта
│   │── utils.py       # Вспомогательные функции
│   │── models.py      # Описание моделей данных
│── tests/             # Тесты pytest
│── logs/              # Логи работы
│── failed_records/    # Данные, которые не записались в БД
│── database/          
│   │── schema.sql     # SQL-скрипт для создания таблиц
│── .gitignore
│── .env               # Файл с настройками
│── requirements.txt   # Список зависимостей
│── pytest.ini         # Настройки pytest
│── README.md
```

---

## Запуск тестов

```sh
pytest tests/
```

---

## Технологии

- **Python** (asyncio, aiohttp)
- **PostgreSQL** (asyncpg)
- **pytest** (тестирование)
- **aioresponses** (мокирование HTTP-запросов)
- **unittest.mock** (мокирование объектов в тестах)