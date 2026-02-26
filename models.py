from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    company_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class PlanType(str, enum.Enum):
    STARTER = "starter"        # 5k запросов
    PROFESSIONAL = "professional"  # 20k запросов
    BUSINESS = "business"      # 50k запросов
    ENTERPRISE = "enterprise"  # 100k запросов
    ULTRA = "ultra"           # 1000k запросов


class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    plan_type = Column(Enum(PlanType))
    monthly_requests = Column(Integer)
    price_uah = Column(Float)  # Цена в гривнях
    price_usd = Column(Float)
    description = Column(Text)
    features = Column(Text)  # JSON строка с особенностями
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    
    status = Column(String(50), default="active")  # active, expired, cancelled
    requests_used = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    auto_renew = Column(Boolean, default=True)
    
    # Связи
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")


class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String(64), unique=True, index=True)
    name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    # Связи
    user = relationship("User", back_populates="api_keys")


class FuelPrice(Base):
    __tablename__ = "fuel_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    station = Column(String(100))  # OKKO, WOG, SOCAR
    fuel_type = Column(String(50))  # A95, A98, ДТ, Газ
    price = Column(Float)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    collected_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    class Config:
        indexes = [("city", "fuel_type", "collected_at")]


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    
    amount_uah = Column(Float)
    status = Column(String(50))  # success, pending, failed, refunded
    liqpay_order_id = Column(String(100), unique=True)
    liqpay_signature = Column(String(255))
    
    payment_method = Column(String(50))  # liqpay_card, liqpay_wallet
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Связи
    user = relationship("User", back_populates="payments")


class APILog(Base):
    __tablename__ = "api_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    
    endpoint = Column(String(255))
    method = Column(String(10))  # GET, POST
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    
    city = Column(String(100), nullable=True)
    fuel_type = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
