# Fuel Price API - Полная Документация

## Базовая информация

- **Base URL:** `http://localhost:8000` (разработка) или `https://api.fuelapi.com` (продакшен)
- **Version:** 1.0.0
- **Auth:** Bearer Token (API Key)

## 🔐 Аутентификация

Все запросы (кроме `/auth/register`, `/auth/login`, `/plans`) требуют заголовка:

```
Authorization: Bearer YOUR_API_KEY
```

API ключ можна получить после:
1. Регистрации через `/auth/register`
2. Входа через `/auth/login`
3. Создания нового ключа через `/api-keys`

---

## 📚 Эндпоинты

### 1. АУТЕНТИФИКАЦИЯ

#### POST /auth/register
Регистрация нового пользователя

**Request:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "myusername",
    "password": "SecurePass123",
    "company_name": "My Company"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "myusername",
    "company_name": "My Company",
    "is_active": true,
    "created_at": "2024-02-25T12:00:00"
  }
}
```

**Errors:**
- `400 Bad Request`: Email или username уже существуют
- `422 Unprocessable Entity`: Ошибка валидации данных

---

#### POST /auth/login
Вход в существующий аккаунт

**Request:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "myusername",
    "company_name": "My Company",
    "is_active": true,
    "created_at": "2024-02-25T12:00:00"
  }
}
```

**Errors:**
- `401 Unauthorized`: Неверные учетные данные

---

### 2. ОСНОВНОЙ API

#### GET /fuel
Получить цены на топливо для города

**Query Parameters:**
| Параметр | Тип | Обязательно | Описание |
|----------|-----|------------|---------|
| city | string | Да | Название города (odessa, kyiv, kharkiv) |
| fuel_type | string | Нет | Тип топлива (A95, A98, ДТ, Газ) |

**Request:**
```bash
curl -X GET "http://localhost:8000/fuel?city=odessa&fuel_type=A95" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**
```json
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
          "address": "ул. Деришевская, 39",
          "latitude": 46.4826,
          "longitude": 30.7338
        },
        {
          "station": "WOG",
          "price": 46.00,
          "address": "ул. Канатна, 25",
          "latitude": 46.4750,
          "longitude": 30.7300
        },
        {
          "station": "SOCAR",
          "price": 45.80,
          "address": "ул. Французька, 15",
          "latitude": 46.4880,
          "longitude": 30.7400
        }
      ]
    }
  },
  "updated": "2024-02-25T14:30:00"
}
```

**Errors:**
- `401 Unauthorized`: Неверный API ключ
- `403 Forbidden`: Нет активной подписки или истекла подписка
- `404 Not Found`: Город или тип топлива не найден
- `429 Too Many Requests`: Превышен лимит запросов по плану

---

#### GET /plans
Получить список всех доступных планов подписки

**Request:**
```bash
curl -X GET http://localhost:8000/plans
```

**Response (200 OK):**
```json
{
  "plans": [
    {
      "id": 1,
      "name": "Starter",
      "plan_type": "starter",
      "monthly_requests": 5000,
      "price_uah": 99.0,
      "price_usd": 2.7,
      "description": "Для разработчиков",
      "features": "[\"5000 запросов/месяц\", \"Основной API\", \"Email поддержка\"]"
    },
    {
      "id": 2,
      "name": "Professional",
      "plan_type": "professional",
      "monthly_requests": 20000,
      "price_uah": 299.0,
      "price_usd": 8.0,
      "description": "Для малого бизнеса",
      "features": "[\"20000 запросов/месяц\", \"API v1+v2\", \"Priority поддержка\", \"Вебхуки\"]"
    }
    // ... остальные планы
  ]
}
```

---

### 3. API КЛЮЧИ

#### POST /api-keys
Создать новый API ключ

**Request:**
```bash
curl -X POST http://localhost:8000/api-keys \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Mobile App"
  }'
```

**Response (200 OK):**
```json
{
  "id": 2,
  "key": "sk_1a2b3c4d5e6f7g8h9i0j",
  "name": "My Mobile App",
  "is_active": true,
  "created_at": "2024-02-25T14:30:00",
  "last_used_at": null
}
```

---

#### GET /api-keys
Получить список всех API ключей пользователя

**Request:**
```bash
curl -X GET http://localhost:8000/api-keys \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**
```json
{
  "keys": [
    {
      "id": 1,
      "key": "sk_original_key_here",
      "name": "Default Key",
      "is_active": true,
      "created_at": "2024-02-25T12:00:00",
      "last_used_at": "2024-02-25T14:20:00"
    },
    {
      "id": 2,
      "key": "sk_1a2b3c4d5e6f7g8h9i0j",
      "name": "My Mobile App",
      "is_active": true,
      "created_at": "2024-02-25T14:30:00",
      "last_used_at": null
    }
  ]
}
```

---

#### DELETE /api-keys/{key_id}
Удалить API ключ

**Request:**
```bash
curl -X DELETE http://localhost:8000/api-keys/2 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**
```json
{
  "message": "API key deleted"
}
```

---

### 4. СТАТИСТИКА АККАУНТА

#### GET /account/stats
Получить полную статистику аккаунта

**Request:**
```bash
curl -X GET http://localhost:8000/account/stats \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "myusername",
    "company_name": "My Company",
    "is_active": true,
    "created_at": "2024-02-25T12:00:00"
  },
  "subscription": {
    "id": 1,
    "plan": {
      "id": 1,
      "name": "Starter",
      "plan_type": "starter",
      "monthly_requests": 5000,
      "price_uah": 99.0,
      "price_usd": 2.7,
      "description": "Для разработчиков",
      "features": "[...]"
    },
    "status": "active",
    "requests_used": 1250,
    "started_at": "2024-02-25T12:00:00",
    "expires_at": "2024-03-25T12:00:00",
    "auto_renew": true,
    "requests_remaining": 3750,
    "progress_percent": 25.0,
    "days_remaining": 28,
    "is_active": true
  },
  "api_usage": {
    "total_requests_used": 1250,
    "total_requests_available": 5000,
    "progress_percent": 25.0,
    "days_remaining": 28,
    "today_requests": 45
  },
  "api_keys": [
    {
      "id": 1,
      "key": "sk_original_key_here",
      "name": "Default Key",
      "is_active": true,
      "created_at": "2024-02-25T12:00:00",
      "last_used_at": "2024-02-25T14:20:00"
    }
  ]
}
```

---

### 5. HEALTH CHECK

#### GET /health
Проверить статус API

**Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "timestamp": "2024-02-25T14:30:00"
}
```

---

## 🔄 Rate Limiting

API использует следующие лимиты на основе плана подписки:

| План | Запросов/месяц | Запросов/час |
|------|----------------|--------------|
| Starter | 5,000 | ~7 |
| Professional | 20,000 | ~28 |
| Business | 50,000 | ~70 |
| Enterprise | 100,000 | ~140 |
| Ultra | 1,000,000 | ~1,400 |

При превышении лимита получите ответ:
```json
{
  "detail": "Request limit exceeded"
}
```

---

## 💾 Версионирование API

Текущая версия: `1.0.0`

Версионирование осуществляется через URL:
- `http://localhost:8000/v1/...` (текущая версия)
- `http://localhost:8000/v2/...` (в будущем)

---

## 🛡️ Безопасность

1. **HTTPS:** Используйте только HTTPS для продакшена
2. **API Key Rotation:** Периодически обновляйте API ключи
3. **Rate Limiting:** Соблюдайте лимиты запросов
4. **IP Whitelist:** Можно установить на уровне брандмауэра
5. **Логирование:** Все запросы логируются в целях безопасности

---

## 📝 Примеры использования

### Python
```python
import requests

api_key = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {api_key}"}

# Получить цены
response = requests.get(
    "http://localhost:8000/fuel",
    params={"city": "odessa", "fuel_type": "A95"},
    headers=headers
)

print(response.json())
```

### JavaScript / Node.js
```javascript
const apiKey = "YOUR_API_KEY";

fetch("http://localhost:8000/fuel?city=odessa&fuel_type=A95", {
  headers: {
    "Authorization": `Bearer ${apiKey}`
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X GET "http://localhost:8000/fuel?city=odessa&fuel_type=A95" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 🐛 Коды ошибок

| Код | Описание |
|-----|---------|
| 200 | OK - Успешный запрос |
| 400 | Bad Request - Ошибка в параметрах |
| 401 | Unauthorized - Неверный API ключ |
| 403 | Forbidden - Нет подписки или она истекла |
| 404 | Not Found - Ресурс не найден |
| 429 | Too Many Requests - Превышен лимит |
| 500 | Internal Server Error - Ошибка сервера |

---

## 📞 Контакты и поддержка

- Email: support@fuelapi.com
- Telegram: @fuelapi_support
- GitHub Issues: https://github.com/your-repo/issues
