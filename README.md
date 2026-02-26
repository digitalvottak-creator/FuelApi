# Fuel Price API

Повнофункціональна API для отстеження цін на паливо (OKKO, WOG, SOCAR) з веб-дашбордом та системою оплати LiqPay.

## 🚀 Особливості

- ✅ Парсинг цен с трьох АЗС (OKKO, WOG, SOCAR)
- ✅ REST API для отримання цен по città
- ✅ Веб-дашборд для користувачів
- ✅ Система підписок з 5 планами (5K, 20K, 50K, 100K, 1M запросів)
- ✅ Інтеграція LiqPay для оплаты
- ✅ API ключи та管理
- ✅ Обмеження запросів по плану
- ✅ Логування всіх запросів
- ✅ Docker готів до продакшену

## 📋 Технологічний стек

**Backend:**
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis (кэширование)
- APScheduler (парсинг)

**Frontend:**
- Next.js 14
- React 18
- Tailwind CSS
- Axios

**DevOps:**
- Docker
- Docker Compose

## 🛠️ Встановлення

### 1. Клонування репозиторія

```bash
git clone <your-repo>
cd fuel-api-project
```

### 2. Налаштування переменных окружения

```bash
cp .env.example .env
```

Редагуйте `.env`:
```env
LIQPAY_PUBLIC_KEY=your_public_key
LIQPAY_PRIVATE_KEY=your_private_key
DATABASE_URL=postgresql://fuel_user:fuel_password@db:5432/fuel_api
```

### 3. Запуск з Docker Compose

```bash
docker-compose up -d
```

Приложение будет доступно по адресам:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Локальна розробка (без Docker)

**Backend:**
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📚 API Документація

### Аутентифікація

#### Реєстрація
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password",
  "company_name": "Your Company"
}

Response:
{
  "access_token": "your_api_key",
  "token_type": "bearer",
  "user": { ... }
}
```

#### Вхід
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

Response:
{
  "access_token": "your_api_key",
  "token_type": "bearer",
  "user": { ... }
}
```

### API Запросы

#### Отримання цен на паливо
```bash
GET /fuel?city=odessa&fuel_type=A95
Authorization: Bearer YOUR_API_KEY

Response:
{
  "city": "odessa",
  "fuel_types": {
    "A95": {
      "min_price": 45.50,
      "avg_price": 45.75,
      "max_price": 46.00,
      "data": [
        {
          "station": "OKKO",
          "price": 45.50,
          "address": "ул. Деришевская, 39"
        },
        ...
      ]
    }
  },
  "updated": "2024-02-25T12:00:00"
}
```

#### Отримання планів
```bash
GET /plans

Response:
{
  "plans": [
    {
      "id": 1,
      "name": "Starter",
      "plan_type": "starter",
      "monthly_requests": 5000,
      "price_uah": 99.0,
      "price_usd": 2.7,
      "description": "Для разработчиков"
    },
    ...
  ]
}
```

#### Отримання статистики аккаунту
```bash
GET /account/stats
Authorization: Bearer YOUR_API_KEY

Response:
{
  "user": { ... },
  "subscription": { ... },
  "api_usage": {
    "total_requests_used": 1250,
    "total_requests_available": 5000,
    "progress_percent": 25.0,
    "days_remaining": 20
  },
  "api_keys": [ ... ]
}
```

#### Створення API ключа
```bash
POST /api-keys
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "My App Key"
}

Response:
{
  "id": 2,
  "key": "new_api_key_here",
  "name": "My App Key",
  "is_active": true,
  "created_at": "2024-02-25T12:00:00"
}
```

#### Отримання всіх API ключей
```bash
GET /api-keys
Authorization: Bearer YOUR_API_KEY

Response:
{
  "keys": [ ... ]
}
```

#### Видалення API ключа
```bash
DELETE /api-keys/{key_id}
Authorization: Bearer YOUR_API_KEY
```

## 💳 Інтеграція LiqPay

### Отримання облікових даних

1. Перейти на https://www.liqpay.com/uk/
2. Зареєструватися як мерчант
3. Отримати **Public Key** та **Private Key**
4. Додати ключи в `.env`:

```env
LIQPAY_PUBLIC_KEY=pk_1234567890
LIQPAY_PRIVATE_KEY=sk_0987654321
```

### Процес оплаты

1. Користувач вибирає план
2. Натискає "Оплатити"
3. Редіректиться на LiqPay форму оплатки
4. Після успішної оплати LP отправляет webhook
5. Система активує підписку користувача

## 📊 Система планів

| План | Запросив | Ціна (₴) | Особливості |
|------|----------|----------|------------|
| Starter | 5,000 | ₴99 | Основний API |
| Professional | 20,000 | ₴299 | +Вебхуки |
| Business | 50,000 | ₴699 | +Аналітика |
| Enterprise | 100,000 | ₴1,299 | +24/7 Поддержка |
| Ultra | 1,000,000 | ₴4,999 | Все включено |

## 🔧 Управління

### Парсинг цен

Парсинг запускається автоматично кожну годину через APScheduler.

Для ручного запуску парсера (в коді):
```python
from parsers import FuelPriceAggregator

aggregator = FuelPriceAggregator()
prices = await aggregator.get_all_prices('odessa')
```

### Логирование

Все API запросы логируются в таблицю `api_logs`:
- Кто запрашивал (user_id)
- Какой эндпоинт
- Сколько запросов сегодня
- Время ответа

### База данних

Для миграций используется SQLAlchemy. Схемы в `models.py`.

Создание новых таблиц:
```python
from models import Base, engine
Base.metadata.create_all(bind=engine)
```

## 🐛 Частые проблемы

### 1. Connection refused на PostgreSQL

```bash
# Проверить что контейнер запущен
docker ps | grep fuel_api_db

# Перезагрузить
docker-compose restart db
```

### 2. LIQPAY keys not configured

Убедитесь что в `.env` установлены ключи LiqPay:
```bash
echo $LIQPAY_PUBLIC_KEY
echo $LIQPAY_PRIVATE_KEY
```

### 3. API Key invalid

Убедитесь что используете правильный формат:
```bash
Authorization: Bearer YOUR_KEY_HERE
```

## 🚀 Развертывание

### Heroku

```bash
# 1. Создать приложения
heroku create fuel-api-backend
heroku create fuel-api-frontend

# 2. Установить переменные
heroku config:set LIQPAY_PUBLIC_KEY=... --app fuel-api-backend
heroku config:set LIQPAY_PRIVATE_KEY=... --app fuel-api-backend

# 3. Добавить PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev --app fuel-api-backend

# 4. Deploy
git push heroku main
```

### Railway / Render

1. Conectи к GitHub
2. Импортируйте `docker-compose.yml`
3. Установите environment variables
4. Deploy!

## 📞 Поддержка

- Email: support@fuelapi.com
- Документация: https://docs.fuelapi.com
- GitHub Issues: https://github.com/your-repo/issues

## 📄 Лицензия

MIT License - смотрите файл LICENSE

## 🎯 Roadmap

- [ ] WebSocket для real-time цен
- [ ] Мобильное приложение (iOS/Android)
- [ ] Нотификации при скачках цен
- [ ] Интеграция с Telegram Bot
- [ ] Экспорт в CSV/PDF
- [ ] Расширение на другие страны

---

**Создано с ❤️ для украинских водителів**
