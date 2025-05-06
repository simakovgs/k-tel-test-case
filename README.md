# EquipmentManager (KT)


## Описание проекта
Приложение для управления перечнем оборудования

## Настройка переменных окружения (.env)

Создайте файл `.env` в корне проекта со следующими параметрами:

```ini
# Безопасность Django
DJANGO_SECRET_KEY=ваш_секретный_ключ  # Пример: %jjnu7=54g6s%qjfnhbpw0zeoei=$!her*y(p%!&84rs$4l85io

# Настройки базы данных (MySQL)
DB_HOST=адрес_базы_данных          # Пример: 0.0.0.0
DB_PORT=порт                      # Пример: 3306
DB_ENGINE=движок_базы_данных      # Пример: django.db.backends.mysql
DB_NAME=название_базы             # Пример: testdb
DB_USER=пользователь              # Пример: testuser
DB_PASSWORD=пароль                # Пример: testpassword

# Настройки JWT-токенов
ACCESS_TOKEN_LIFETIME_IN_DAYS=7    # Срок жизни access-токена (дни)
REFRESH_TOKEN_LIFETIME_IN_DAYS=14  # Срок жизни refresh-токена (дни)

# Настройки CORS
CORS_ALLOWED_ORIGINS=разрешённые_домены  # Пример: http://localhost:8080,http://127.0.0.1:8080
CORS_ALLOW_HEADERS=разрешённые_заголовки  # Пример: accept,accept-encoding,authorization,content-type
```

## Запуск

1. Установка зависимостей:
```bash
  pip install -r requirements.txt
```

2. Создание cуперпользователя для авторизации:
```bash
python manage.py createsuperuser
```

3. Миграция базы данных:
```bash
  python manage.py migrate
```

4. Запуск сервера:
```bash
  uvicorn kt_test_case.asgi:application
```

