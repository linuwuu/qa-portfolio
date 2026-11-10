# Restful-booker API tests

Автотесты для учебного REST API бронирований [Restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html).

Стек: Python, pytest, requests, pydantic

## Что реализовано

- API-клиент на классах (`Reservation`) с авторизацией по токену и `requests.Session`: CRUD бронирований.
- Тесты создания, получения, обновления (PUT / PATCH), удаления и авторизации.
- Позитивные и негативные сценарии: неверные типы данных, невалидные значения, пропущенные обязательные поля, несуществующие id, доступ без токена.
- Проверка ответов в три шага: статус-код, структура и типы (pydantic-модели), значения.
- Клиент передаётся в тесты через фикстуры pytest, негативные кейсы параметризованы.
- Тестовые брони удаляются автоматически после каждого теста.
- Известные баги сервера помечены `xfail` с описанием причины.


## Структура
```
├── api/
│ ├── client.py # клиент Restful-booker
│ └── schemas.py # pydantic-модели ответов
├── tests/
│ ├── config.py # адрес сервера и логин/пароль
│ ├── data.py # тестовые данные
│ ├── conftest.py # фикстуры
│ ├── test_auth.py
│ ├── test_create_booking.py
│ ├── test_get_booking.py
│ ├── test_update_booking.py
│ └── test_delete_booking.py
├── pytest.ini
├── requirements.txt
└── README.md
```