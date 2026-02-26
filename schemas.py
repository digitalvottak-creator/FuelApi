from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PlanTypeEnum(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"
    ULTRA = "ultra"


# ===== ПОЛЬЗОВАТЕЛЬ =====
class UserBase(BaseModel):
    email: EmailStr
    username: str
    company_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    username: Optional[str] = None


# ===== ПЛАН =====
class PlanResponse(BaseModel):
    id: int
    name: str
    plan_type: PlanTypeEnum
    monthly_requests: int
    price_uah: float
    price_usd: float
    description: str
    features: str
    
    class Config:
        from_attributes = True


class PlanListResponse(BaseModel):
    plans: List[PlanResponse]


# ===== ПОДПИСКА =====
class SubscriptionResponse(BaseModel):
    id: int
    plan: PlanResponse
    status: str
    requests_used: int
    started_at: datetime
    expires_at: datetime
    auto_renew: bool
    
    class Config:
        from_attributes = True


class SubscriptionDetailResponse(SubscriptionResponse):
    requests_remaining: int
    progress_percent: float
    days_remaining: int
    is_active: bool


# ===== API KEY =====
class APIKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class APIKeyResponse(BaseModel):
    id: int
    key: str
    name: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class APIKeyListResponse(BaseModel):
    keys: List[APIKeyResponse]


# ===== ТЦ ТОПЛИВА =====
class FuelPriceData(BaseModel):
    station: str
    price: float
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FuelPriceResponse(BaseModel):
    city: str
    fuel_type: str
    min_price: float
    avg_price: float
    max_price: float
    data: List[FuelPriceData]
    updated: datetime
    
    class Config:
        from_attributes = True


class FuelPriceHistoryPoint(BaseModel):
    date: datetime
    avg_price: float
    min_price: float
    max_price: float


class FuelPriceHistoryResponse(BaseModel):
    city: str
    fuel_type: str
    history: List[FuelPriceHistoryPoint]


# ===== ОПЛАТА =====
class PaymentCreateRequest(BaseModel):
    plan_id: int
    description: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    amount_uah: float
    status: str
    liqpay_order_id: str
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class LiqPayCheckoutResponse(BaseModel):
    order_id: str
    checkout_url: str
    
    
class LiqPayWebhookData(BaseModel):
    data: str  # Base64 encoded JSON
    signature: str


# ===== ОСНОВНОЙ API ЗАПРОС/ОТВЕТ =====
class APIErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: int


class APISuccessResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ===== АДМИН/СТАТИСТИКА =====
class APIUsageStatsResponse(BaseModel):
    total_requests_used: int
    total_requests_available: int
    progress_percent: float
    days_remaining: int
    today_requests: int


class AccountStatsResponse(BaseModel):
    user: UserResponse
    subscription: SubscriptionDetailResponse
    api_usage: APIUsageStatsResponse
    api_keys: List[APIKeyResponse]
