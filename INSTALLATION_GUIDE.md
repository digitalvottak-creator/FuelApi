# Fuel Price API - Инструкция по запуску

## 🎯 Что создано

✅ Полнофункциональное приложение с:
- Backend (Python FastAPI) с парсерами OKKO, WOG, SOCAR
- Frontend (Next.js React) с дашбордом
- PostgreSQL БД с моделями
- Система подписок с 5 планами
- LiqPay интеграция для оплаты
- Docker готово для продакшена

## 📦 Структура проекта

```
fuel-api-project/
├── main.py                     # FastAPI приложение
├── models.py                   # БД модели
├── schemas.py                  # Pydantic схемы
├── parsers.py                  # Парсеры АЗС
├── liqpay_service.py           # LiqPay интеграция
├── requirements.txt            # Python зависимости
├── docker-compose.yml          # Docker для всего
├── .env.example                # Пример конфига
├── README.md                   # Основная документация
├── API_DOCS.md                 # API документация
├── PROJECT_INDEX.md            # Индекс проекта
├── frontend/                   # Next.js приложение
│   ├── app/
│   │   ├── page.tsx            # Главная страница
│   │   ├── layout.tsx          # Layout
│   │   ├── dashboard/page.tsx  # Личный кабинет
│   │   ├── auth/
│   │   │   ├── login/page.tsx  # Страница входа
│   │   │   └── register/page.tsx # Регистрация
│   │   └── components/
│   │       ├── Navbar.tsx      # Навбар
│   │       └── Footer.tsx      # Футер
│   ├── package.json
│   ├── next.config.js
│   └── tailwind.config.js
└── docs/
    └── INSTALLATION_GUIDE.md    # Этот файл
```

## 🚀 СПОСОБ 1: Быстрый старт с Docker (рекомендуется)

### Требования
- Docker
- Docker Compose
- Git (опционально)

### Шаги

#### 1. Подготовка
```bash
# Перейти в директорию проекта
cd fuel-api-project

# Скопировать .env
cp .env.example .env
```

#### 2. Редактировать .env
```bash
# Откройте .env в редакторе и заполните:
LIQPAY_PUBLIC_KEY=pk_1234567890
LIQPAY_PRIVATE_KEY=sk_0987654321
# Остальное можно оставить по умолчанию
```

#### 3. Запустить Docker Compose
```bash
docker-compose up -d
```

#### 4. Инициализация БД
```bash
# База создается автоматически, но можно проверить
docker-compose exec api python -c "from models import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### 5. Проверка
```bash
# Frontend доступен на: http://localhost:3000
# Backend доступен на: http://localhost:8000
# API docs доступны на: http://localhost:8000/docs
```

---

## 🚀 СПОСОБ 2: Локальная разработка

### Требования
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (или SQLite для разработки)
- Redis (опционально)

### Backend

#### 1. Установка Python окружения
```bash
# Перейти в директорию проекта
cd fuel-api-project

# Создать виртуальное окружение
python -m venv venv

# Активировать (на Windows: venv\Scripts\activate)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

#### 2. Настройка .env
```bash
cp .env.example .env

# Отредактировать .env
# Для разработки можно использовать SQLite по умолчанию
```

#### 3. Инициализация БД
```bash
python -c "from models import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### 4. Запуск сервера
```bash
uvicorn main:app --reload
# Сервер запустится на http://localhost:8000
```

#### 5. Тестирование API
```bash
# Откройте http://localhost:8000/docs
# Там вы увидите интерактивную документацию Swagger
```

### Frontend

#### 1. Установка зависимостей
```bash
cd frontend
npm install
```

#### 2. Конфигурация
```bash
# Создать .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

#### 3. Запуск dev сервера
```bash
npm run dev
# Frontend будет на http://localhost:3000
```

---

## 🔐 LiqPay Настройка (Обязательно!)

### Шаг 1: Регистрация в LiqPay
1. Перейти на https://www.liqpay.com/uk/
2. Нажать "Регистрация"
3. Заполнить форму мерчанта
4. Подтвердить email

### Шаг 2: Получить ключи
1. Войти в личный кабинет LiqPay
2. Перейти в "Настройки" → "API"
3. Скопировать:
   - **Public Key** (начинается с `pk_`)
   - **Private Key** (начинается с `sk_`)

### Шаг 3: Добавить в .env
```env
LIQPAY_PUBLIC_KEY=pk_xxxxxxxxxxxxxxxx
LIQPAY_PRIVATE_KEY=sk_xxxxxxxxxxxxxxxxxxxx
```

### Шаг 4: Тестирование (Sandbox)
LiqPay предоставляет тестовые карты:
- **Карта:** 4111 1111 1111 1111
- **Месяц/Год:** 12/25
- **CVC:** 123

---

## 📝 Первый запуск приложения

### 1. Регистрация пользователя
1. Откройте http://localhost:3000
2. Нажмите "Регистрация"
3. Заполните форму:
   - Email: user@example.com
   - Username: myuser
   - Password: SecurePass123
   - Company: My Company (опционально)

### 2. Вход
1. Вернитесь на главную или перейдите на /auth/login
2. Введите учетные данные

### 3. Перейти на Dashboard
1. После входа вы будете редиректены на /dashboard
2. Там вы увидите:
   - Информацию о подписке
   - API ключи
   - Статистику использования

### 4. Получить цены
```bash
# В curl или Postman:
curl -X GET "http://localhost:8000/fuel?city=odessa&fuel_type=A95" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 🧪 Тестирование API

### С Swagger UI (рекомендуется)
1. Откройте http://localhost:8000/docs
2. Найдите нужный эндпоинт
3. Нажмите "Try it out"
4. Заполните параметры
5. Нажмите "Execute"

### С cURL
```bash
# 1. Регистрация
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPass123"
  }'

# 2. Получить цены
curl -X GET "http://localhost:8000/fuel?city=odessa" \
  -H "Authorization: Bearer YOUR_API_KEY"

# 3. Получить планы
curl http://localhost:8000/plans
```

### С Postman
1. Скачать [Postman](https://www.postman.com/downloads/)
2. Импортировать коллекцию:
   - Файл → Import
   - Вставить API_DOCS.md
3. Установить переменные окружения
4. Тестировать запросы

---

## 🐳 Docker команды

```bash
# Просмотр логов
docker-compose logs -f api
docker-compose logs -f frontend

# Остановка
docker-compose down

# Перезагрузка
docker-compose restart

# Удаление всего
docker-compose down -v

# Входа в контейнер
docker-compose exec api bash
docker-compose exec frontend sh
```

---

## 🔧 Решение проблем

### 1. Connection refused на PostgreSQL
```bash
# Проверить контейнеры
docker ps

# Перезагрузить
docker-compose restart db
```

### 2. Port 3000 занят
```bash
# Найти процесс
lsof -i :3000

# Или использовать другой порт
docker-compose up -d -p 3001:3000
```

### 3. LiqPay keys not configured
```bash
# Убедитесь что в .env установлены ключи
cat .env | grep LIQPAY

# Перезагрузить контейнер
docker-compose restart api
```

### 4. CORS ошибка
```bash
# Проверить что frontend_url правильный
# Пересчитать контейнеры
docker-compose down
docker-compose up -d
```

### 5. База данных не создается
```bash
# Вручную инициализировать
docker-compose exec api python
>>> from models import Base, engine
>>> Base.metadata.create_all(bind=engine)
>>> exit()
```

---

## 📊 Проверка работоспособности

### Health Check
```bash
curl http://localhost:8000/health
# Ответ: {"status": "ok", "timestamp": "..."}
```

### Получить планы
```bash
curl http://localhost:8000/plans
# Ответ: {"plans": [...]}
```

### Регистрация
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"Test123456"}'
```

---

## 🚀 Развертывание на продакшене

### Heroku
```bash
# Установить Heroku CLI
# Создать приложение
heroku create fuel-api-backend

# Установить переменные
heroku config:set LIQPAY_PUBLIC_KEY=...
heroku config:set LIQPAY_PRIVATE_KEY=...

# Развернуть
git push heroku main
```

### Railway.app
1. Подключить GitHub репозиторий
2. Импортировать docker-compose.yml
3. Установить environment variables
4. Deploy

### DigitalOcean App Platform
1. Создать новое приложение
2. Выбрать GitHub репозиторий
3. Выбрать docker-compose.yml
4. Установить переменные
5. Deploy

### AWS EC2
```bash
# SSH в EC2
ssh -i key.pem ec2-user@your-instance

# Установить Docker
sudo apt update && sudo apt install docker.io docker-compose

# Клонировать проект
git clone ...

# Запустить
docker-compose up -d
```

---

## 📚 Дополнительные команды

### Очистить БД
```bash
docker-compose down -v  # Удалить volumes
docker-compose up -d    # Пересоздать
```

### Скачать логи
```bash
docker-compose logs > logs.txt
```

### Обновить зависимости
```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend && npm update
```

---

## 💡 Рекомендации

1. **Разработка:** Используйте локальный setup для лучшей производительности
2. **Testing:** Используйте SQLite для БД в разработке
3. **Production:** Всегда используйте PostgreSQL
4. **Security:** Измените SECRET_KEY в .env
5. **LiqPay:** Используйте sandbox до готовности к prodакшену

---

## ✅ Checklist перед запуском

- [ ] Docker установлен
- [ ] .env заполнен
- [ ] LiqPay ключи добавлены
- [ ] Порты 3000, 8000, 5432 свободны
- [ ] PostgreSQL готов (если локально)
- [ ] Redis готов (если используется)

---

## 📞 Помощь

- Документация: README.md, API_DOCS.md
- Структура проекта: PROJECT_INDEX.md
- GitHub Issues: [your-repo]/issues
- Email: support@fuelapi.com

---

**Версія:** 1.0.0  
**Статус:** Готово ✅  
**Последнее обновление:** 25.02.2024
