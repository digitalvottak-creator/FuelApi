from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
import logging
import hashlib
import secrets

# Импорты моделей и схем
from models import Base, User, Plan, PlanType, Subscription, APIKey, FuelPrice, Payment, APILog
from schemas import (
    UserCreate, UserLogin, UserResponse, TokenResponse,
    PlanResponse, PlanListResponse,
    SubscriptionDetailResponse,
    APIKeyCreate, APIKeyResponse, APIKeyListResponse,
    AccountStatsResponse, APIUsageStatsResponse
)
from parsers import FuelPriceAggregator

# Настройки
load_dotenv()
logger = logging.getLogger(__name__)

# Конфигурация базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fuel_api.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

Base.metadata.create_all(bind=engine)


def get_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI приложение
app = FastAPI(
    title="Fuel Price API",
    description="API для отслеживания цен на топливо на АЗС (OKKO, WOG, SOCAR)",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Парсер
fuel_aggregator = FuelPriceAggregator()


# ===== УТИЛИТЫ =====

def hash_password(password: str) -> str:
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return hash_password(plain_password) == hashed_password


def create_api_key() -> str:
    """Генерация API ключа"""
    return secrets.token_urlsafe(32)


def get_api_key_from_header(authorization: Optional[str] = Header(None)) -> str:
    """Получить API ключ из заголовка"""
    if not authorization:
        raise HTTPException(status_code=401, detail="API key required")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    return parts[1]


# ===== АУТЕНТИФИКАЦИЯ =====

@app.post("/auth/register", response_model=TokenResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        company_name=user_data.company_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Создание подписки STARTER по умолчанию
    starter_plan = db.query(Plan).filter(Plan.plan_type == PlanType.STARTER).first()
    if not starter_plan:
        # Создать план если его нет
        starter_plan = Plan(
            name="Starter",
            plan_type=PlanType.STARTER,
            monthly_requests=5000,
            price_uah=99.0,
            price_usd=2.7,
            description="Для разработчиков",
            features='["5000 запросов/месяц", "Основной API"]'
        )
        db.add(starter_plan)
        db.commit()
        db.refresh(starter_plan)
    
    subscription = Subscription(
        user_id=new_user.id,
        plan_id=starter_plan.id,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(subscription)
    
    # Создать API ключ
    api_key_str = create_api_key()
    api_key = APIKey(
        user_id=new_user.id,
        key=api_key_str,
        name="Default Key"
    )
    db.add(api_key)
    db.commit()
    
    return TokenResponse(
        access_token=api_key_str,
        user=UserResponse.model_validate(new_user)
    )


@app.post("/auth/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Вход в аккаунт"""
    
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    api_key = db.query(APIKey).filter(APIKey.user_id == user.id).first()
    if not api_key:
        key_str = create_api_key()
        api_key = APIKey(user_id=user.id, key=key_str, name="Default Key")
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
    
    api_key.last_used_at = datetime.utcnow()
    db.commit()
    
    return TokenResponse(
        access_token=api_key.key,
        user=UserResponse.model_validate(user)
    )


# ===== ОСНОВНОЙ API =====

@app.get("/plans", response_model=PlanListResponse)
def get_plans(db: Session = Depends(get_db)):
    """Получить список всех доступных планов"""
    
    plans = db.query(Plan).all()
    
    if not plans:
        plans_data = [
            {
                "name": "Starter",
                "plan_type": PlanType.STARTER,
                "monthly_requests": 5000,
                "price_uah": 99.0,
                "price_usd": 2.7,
                "description": "Для разработчиков",
                "features": '["5000 запросов/месяц", "Основной API", "Email поддержка"]'
            },
            {
                "name": "Professional",
                "plan_type": PlanType.PROFESSIONAL,
                "monthly_requests": 20000,
                "price_uah": 299.0,
                "price_usd": 8.0,
                "description": "Для малого бизнеса",
                "features": '["20000 запросов/месяц", "API v1+v2", "Priority поддержка"]'
            },
            {
                "name": "Business",
                "plan_type": PlanType.BUSINESS,
                "monthly_requests": 50000,
                "price_uah": 699.0,
                "price_usd": 19.0,
                "description": "Для растущих компаний",
                "features": '["50000 запросов/месяц", "Advanced API", "24/7 поддержка"]'
            },
            {
                "name": "Enterprise",
                "plan_type": PlanType.ENTERPRISE,
                "monthly_requests": 100000,
                "price_uah": 1299.0,
                "price_usd": 35.0,
                "description": "Для крупных компаний",
                "features": '["100000 запросов/месяц", "Full API access", "Dedicated support"]'
            },
            {
                "name": "Ultra",
                "plan_type": PlanType.ULTRA,
                "monthly_requests": 1000000,
                "price_uah": 4999.0,
                "price_usd": 135.0,
                "description": "Для корпоратива",
                "features": '["1000000 запросов/месяц", "Всё включено"]'
            }
        ]
        
        for plan_data in plans_data:
            plan = Plan(**plan_data)
            db.add(plan)
        
        db.commit()
        plans = db.query(Plan).all()
    
    return PlanListResponse(plans=[PlanResponse.model_validate(p) for p in plans])


@app.get("/fuel")
async def get_fuel_prices(
    city: str,
    fuel_type: Optional[str] = None,
    api_key: str = Depends(get_api_key_from_header),
    db: Session = Depends(get_db)
):
    """Получить цены на топливо для города"""
    
    key_obj = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not key_obj:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    user = db.query(User).filter(User.id == key_obj.user_id).first()
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.status == "active"
    ).first()
    
    if not subscription or subscription.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="No active subscription")
    
    if subscription.requests_used >= subscription.plan.monthly_requests:
        raise HTTPException(status_code=429, detail="Request limit exceeded")
    
    prices = await fuel_aggregator.get_all_prices(city)
    
    if not prices:
        raise HTTPException(status_code=404, detail=f"No prices found for city: {city}")
    
    if fuel_type:
        prices = [p for p in prices if p["fuel_type"] == fuel_type]
        if not prices:
            raise HTTPException(status_code=404, detail=f"No prices found for fuel type: {fuel_type}")
    
    for price in prices:
        fuel_price = FuelPrice(**price)
        db.add(fuel_price)
    
    api_log = APILog(
        user_id=user.id,
        api_key_id=key_obj.id,
        endpoint="/fuel",
        method="GET",
        status_code=200,
        response_time_ms=100,
        city=city,
        fuel_type=fuel_type
    )
    db.add(api_log)
    
    subscription.requests_used += 1
    key_obj.last_used_at = datetime.utcnow()
    
    db.commit()
    
    aggregated = fuel_aggregator.aggregate_by_fuel_type(prices)
    
    response_data = {
        "city": city,
        "fuel_types": {}
    }
    
    for fuel_type_key, data in aggregated.items():
        response_data["fuel_types"][fuel_type_key] = {
            "min_price": data["min_price"],
            "avg_price": data["avg_price"],
            "max_price": data["max_price"],
            "data": data["stations"]
        }
    
    response_data["updated"] = datetime.utcnow().isoformat()
    
    return response_data


@app.post("/api-keys", response_model=APIKeyResponse)
def create_api_key_endpoint(
    key_data: APIKeyCreate,
    api_key: str = Depends(get_api_key_from_header),
    db: Session = Depends(get_db)
):
    """Создать новый API ключ"""
    
    key_obj = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not key_obj:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    new_key = APIKey(
        user_id=key_obj.user_id,
        key=create_api_key(),
        name=key_data.name
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    
    return APIKeyResponse.model_validate(new_key)


@app.get("/api-keys", response_model=APIKeyListResponse)
def list_api_keys(
    api_key: str = Depends(get_api_key_from_header),
    db: Session = Depends(get_db)
):
    """Получить список API ключей"""
    
    key_obj = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not key_obj:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    keys = db.query(APIKey).filter(APIKey.user_id == key_obj.user_id).all()
    
    return APIKeyListResponse(keys=[APIKeyResponse.model_validate(k) for k in keys])


@app.delete("/api-keys/{key_id}")
def delete_api_key(
    key_id: int,
    api_key: str = Depends(get_api_key_from_header),
    db: Session = Depends(get_db)
):
    """Удалить API ключ"""
    
    key_obj = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not key_obj:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    key_to_delete = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == key_obj.user_id
    ).first()
    
    if not key_to_delete:
        raise HTTPException(status_code=404, detail="API key not found")
    
    db.delete(key_to_delete)
    db.commit()
    
    return {"message": "API key deleted"}


@app.get("/account/stats", response_model=AccountStatsResponse)
def get_account_stats(
    api_key: str = Depends(get_api_key_from_header),
    db: Session = Depends(get_db)
):
    """Получить статистику аккаунта"""
    
    key_obj = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not key_obj:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    user = db.query(User).filter(User.id == key_obj.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.status == "active"
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    
    requests_remaining = subscription.plan.monthly_requests - subscription.requests_used
    progress = (subscription.requests_used / subscription.plan.monthly_requests) * 100
    days_remaining = (subscription.expires_at - datetime.utcnow()).days
    
    api_keys = db.query(APIKey).filter(APIKey.user_id == user.id).all()
    
    return AccountStatsResponse(
        user=UserResponse.model_validate(user),
        subscription=SubscriptionDetailResponse(
            id=subscription.id,
            plan=PlanResponse.model_validate(subscription.plan),
            status=subscription.status,
            requests_used=subscription.requests_used,
            started_at=subscription.started_at,
            expires_at=subscription.expires_at,
            auto_renew=subscription.auto_renew,
            requests_remaining=requests_remaining,
            progress_percent=progress,
            days_remaining=days_remaining,
            is_active=True
        ),
        api_usage=APIUsageStatsResponse(
            total_requests_used=subscription.requests_used,
            total_requests_available=subscription.plan.monthly_requests,
            progress_percent=progress,
            days_remaining=days_remaining,
            today_requests=0
        ),
        api_keys=[APIKeyResponse.model_validate(k) for k in api_keys]
    )


@app.get("/health")
def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)