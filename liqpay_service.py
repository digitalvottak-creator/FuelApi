import base64
import json
import hashlib
import hmac
import requests
from typing import Dict, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class LiqPayService:
    """Сервис для работы с LiqPay"""
    
    # LiqPay API endpoints
    API_URL = "https://www.liqpay.com/api/3/checkout"
    WEBHOOK_URL = "https://www.liqpay.com/api/3/action"
    
    def __init__(self):
        self.public_key = os.getenv("LIQPAY_PUBLIC_KEY")
        self.private_key = os.getenv("LIQPAY_PRIVATE_KEY")
        
        if not self.public_key or not self.private_key:
            logger.error("LiqPay keys not configured!")
    
    def _create_signature(self, data: str) -> str:
        """Создать подпись для LiqPay запроса"""
        signature_str = self.private_key + data + self.private_key
        signature = base64.b64encode(
            hashlib.sha1(signature_str.encode()).digest()
        ).decode()
        return signature
    
    def _encode_data(self, data: Dict) -> str:
        """Кодировать данные в base64"""
        json_str = json.dumps(data)
        return base64.b64encode(json_str.encode()).decode()
    
    def _decode_data(self, data: str) -> Dict:
        """Декодировать данные из base64"""
        json_str = base64.b64decode(data).decode()
        return json.loads(json_str)
    
    def create_payment(
        self,
        order_id: str,
        amount: float,
        description: str,
        return_url: str = None,
        server_url: str = None
    ) -> Dict:
        """
        Создать платёж в LiqPay
        
        Args:
            order_id: Уникальный ID заказа
            amount: Сумма в гривнях
            description: Описание платежа
            return_url: URL для возврата после платежа
            server_url: URL для server-to-server callback
        """
        
        if not self.public_key or not self.private_key:
            return {
                "success": False,
                "error": "LiqPay not configured"
            }
        
        # Подготовка данных для LiqPay
        data = {
            "public_key": self.public_key,
            "version": "3",
            "action": "pay",
            "amount": int(amount * 100),  # LiqPay требует сумму в копейках
            "currency": "UAH",
            "description": description,
            "order_id": order_id,
            "result_url": return_url or os.getenv("FRONTEND_URL", "http://localhost:3000") + "/payment/success",
            "server_url": server_url or os.getenv("API_URL", "http://localhost:8000") + "/payments/webhook",
            "language": "uk"
        }
        
        # Кодирование данных
        encoded_data = self._encode_data(data)
        signature = self._create_signature(encoded_data)
        
        return {
            "success": True,
            "data": encoded_data,
            "signature": signature,
            "checkout_url": self.API_URL,
            "order_id": order_id
        }
    
    def verify_signature(self, data: str, signature: str) -> bool:
        """Проверить подпись от LiqPay webhook"""
        expected_signature = self._create_signature(data)
        
        # Сравнение подписей
        return hmac.compare_digest(signature, expected_signature)
    
    def process_webhook(self, data: str, signature: str) -> Optional[Dict]:
        """
        Обработать webhook от LiqPay
        
        Returns:
            Декодированные данные платежа или None если подпись неверная
        """
        
        if not self.verify_signature(data, signature):
            logger.error("Invalid LiqPay signature")
            return None
        
        try:
            return self._decode_data(data)
        except Exception as e:
            logger.error(f"Error decoding LiqPay data: {e}")
            return None
    
    def get_payment_status(self, order_id: str) -> Dict:
        """
        Получить статус платежа (требует API запроса)
        
        ПРИМЕЧАНИЕ: Эта функция требует дополнительной аутентификации
        """
        
        data = {
            "public_key": self.public_key,
            "version": "3",
            "action": "status",
            "order_id": order_id
        }
        
        encoded_data = self._encode_data(data)
        signature = self._create_signature(encoded_data)
        
        try:
            response = requests.post(
                self.WEBHOOK_URL,
                data={
                    "data": encoded_data,
                    "signature": signature
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"LiqPay status error: {response.status_code}")
                return {"status": "error"}
        except Exception as e:
            logger.error(f"LiqPay status request error: {e}")
            return {"status": "error"}


# Статусы платежей LiqPay
PAYMENT_STATUSES = {
    "success": "success",        # Успешный платёж
    "failure": "failure",        # Неудачный платёж
    "wait_secure": "wait_secure",  # Ожидание подтверждения
    "processing": "processing",  # Обработка
    "sandbox": "sandbox"         # Песочница
}


class PaymentProcessor:
    """Обработчик платежей"""
    
    def __init__(self):
        self.liqpay = LiqPayService()
    
    def create_subscription_payment(
        self,
        user_id: int,
        plan_id: int,
        plan_name: str,
        amount: float
    ) -> Dict:
        """Создать платёж для подписки"""
        
        order_id = f"user_{user_id}_plan_{plan_id}_{int(datetime.utcnow().timestamp())}"
        
        payment_data = self.liqpay.create_payment(
            order_id=order_id,
            amount=amount,
            description=f"Подписка {plan_name} - Fuel API"
        )
        
        return {
            **payment_data,
            "user_id": user_id,
            "plan_id": plan_id
        }
    
    def handle_payment_callback(self, webhook_data: Dict) -> Dict:
        """Обработать callback от LiqPay"""
        
        status = webhook_data.get("status")
        order_id = webhook_data.get("order_id")
        amount = webhook_data.get("amount")  # в копейках
        
        return {
            "order_id": order_id,
            "status": status,
            "amount_uah": amount / 100 if amount else 0,
            "success": status == "success"
        }
