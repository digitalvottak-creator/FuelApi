import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FuelPriceParser:
    """Базовый класс для парсеров"""
    
    FUEL_TYPES = {
        "A95": "A95",
        "A98": "A98",
        "ДТ": "ДТ",
        "Газ": "Газ"
    }
    
    async def fetch(self, url: str, timeout: int = 10) -> Optional[str]:
        """Получить HTML страницы"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                async with session.get(url, headers=headers, timeout=timeout) as resp:
                    if resp.status == 200:
                        return await resp.text()
        except Exception as e:
            logger.error(f"Ошибка при fetch {url}: {e}")
        return None


class OKKOParser(FuelPriceParser):
    """Парсер для OKKO"""
    
    BASE_URL = "https://www.okko.ua"
    
    async def get_prices(self, city: str) -> List[Dict]:
        """
        Получить цены OKKO для города
        
        ПРИМЕЧАНИЕ: В реальном приложении нужно использовать:
        1. Selenium/Puppeteer для JS-рендеринга
        2. Мобильный API если есть
        3. Прямые контакты с OKKO
        """
        try:
            html = await self.fetch(f"{self.BASE_URL}/ua/")
            if not html:
                return []
            
            # Это упрощённый парсер - в реальности нужно более сложная логика
            prices = await self._parse_okko_data(city)
            return prices
        except Exception as e:
            logger.error(f"OKKO parser error: {e}")
            return []
    
    async def _parse_okko_data(self, city: str) -> List[Dict]:
        """Парсинг данных OKKO"""
        # Mock данные для демонстрации
        okko_data = {
            "odessa": [
                {
                    "station": "OKKO",
                    "address": "ул. Деришевская, 39",
                    "prices": {"A95": 45.50, "A98": 47.20, "ДТ": 42.80, "Газ": 14.50},
                    "latitude": 46.4826,
                    "longitude": 30.7338
                },
                {
                    "station": "OKKO",
                    "address": "ул. Ланжеронская, 100",
                    "prices": {"A95": 45.60, "A98": 47.30, "ДТ": 42.90, "Газ": 14.60},
                    "latitude": 46.4853,
                    "longitude": 30.7457
                }
            ],
            "kyiv": [
                {
                    "station": "OKKO",
                    "address": "ул. Княжа, 8",
                    "prices": {"A95": 46.20, "A98": 47.90, "ДТ": 43.50, "Газ": 15.00},
                    "latitude": 50.4009,
                    "longitude": 30.5238
                }
            ]
        }
        
        city_lower = city.lower()
        result = []
        
        if city_lower in okko_data:
            for station_data in okko_data[city_lower]:
                for fuel_type, price in station_data["prices"].items():
                    result.append({
                        "station": "OKKO",
                        "city": city,
                        "fuel_type": fuel_type,
                        "price": price,
                        "address": station_data["address"],
                        "latitude": station_data["latitude"],
                        "longitude": station_data["longitude"],
                        "collected_at": datetime.utcnow()
                    })
        
        return result


class WOGParser(FuelPriceParser):
    """Парсер для WOG"""
    
    BASE_URL = "https://www.wog.ua"
    
    async def get_prices(self, city: str) -> List[Dict]:
        """Получить цены WOG для города"""
        try:
            prices = await self._parse_wog_data(city)
            return prices
        except Exception as e:
            logger.error(f"WOG parser error: {e}")
            return []
    
    async def _parse_wog_data(self, city: str) -> List[Dict]:
        """Парсинг данных WOG"""
        wog_data = {
            "odessa": [
                {
                    "station": "WOG",
                    "address": "ул. Канатна, 25",
                    "prices": {"A95": 46.00, "A98": 47.70, "ДТ": 43.20, "Газ": 14.70},
                    "latitude": 46.4750,
                    "longitude": 30.7300
                },
                {
                    "station": "WOG",
                    "address": "пр. Поточний, 45",
                    "prices": {"A95": 46.10, "A98": 47.80, "ДТ": 43.30, "Газ": 14.80},
                    "latitude": 46.4920,
                    "longitude": 30.7500
                }
            ],
            "kyiv": [
                {
                    "station": "WOG",
                    "address": "ул. Мінська, 17",
                    "prices": {"A95": 46.50, "A98": 48.20, "ДТ": 43.80, "Газ": 15.20},
                    "latitude": 50.4100,
                    "longitude": 30.5100
                }
            ]
        }
        
        city_lower = city.lower()
        result = []
        
        if city_lower in wog_data:
            for station_data in wog_data[city_lower]:
                for fuel_type, price in station_data["prices"].items():
                    result.append({
                        "station": "WOG",
                        "city": city,
                        "fuel_type": fuel_type,
                        "price": price,
                        "address": station_data["address"],
                        "latitude": station_data["latitude"],
                        "longitude": station_data["longitude"],
                        "collected_at": datetime.utcnow()
                    })
        
        return result


class SOCARParser(FuelPriceParser):
    """Парсер для SOCAR"""
    
    BASE_URL = "https://socar.ua"
    
    async def get_prices(self, city: str) -> List[Dict]:
        """Получить цены SOCAR для города"""
        try:
            prices = await self._parse_socar_data(city)
            return prices
        except Exception as e:
            logger.error(f"SOCAR parser error: {e}")
            return []
    
    async def _parse_socar_data(self, city: str) -> List[Dict]:
        """Парсинг данных SOCAR"""
        socar_data = {
            "odessa": [
                {
                    "station": "SOCAR",
                    "address": "ул. Французька, 15",
                    "prices": {"A95": 45.80, "A98": 47.50, "ДТ": 43.00, "Газ": 14.40},
                    "latitude": 46.4880,
                    "longitude": 30.7400
                }
            ],
            "kyiv": [
                {
                    "station": "SOCAR",
                    "address": "пр. Павла Тичини, 2",
                    "prices": {"A95": 46.30, "A98": 48.00, "ДТ": 43.60, "Газ": 15.10},
                    "latitude": 50.4050,
                    "longitude": 30.5050
                }
            ]
        }
        
        city_lower = city.lower()
        result = []
        
        if city_lower in socar_data:
            for station_data in socar_data[city_lower]:
                for fuel_type, price in station_data["prices"].items():
                    result.append({
                        "station": "SOCAR",
                        "city": city,
                        "fuel_type": fuel_type,
                        "price": price,
                        "address": station_data["address"],
                        "latitude": station_data["latitude"],
                        "longitude": station_data["longitude"],
                        "collected_at": datetime.utcnow()
                    })
        
        return result


class FuelPriceAggregator:
    """Агрегатор цен всех АЗС"""
    
    def __init__(self):
        self.okko = OKKOParser()
        self.wog = WOGParser()
        self.socar = SOCARParser()
    
    async def get_all_prices(self, city: str) -> List[Dict]:
        """Получить цены от всех АЗС для города"""
        tasks = [
            self.okko.get_prices(city),
            self.wog.get_prices(city),
            self.socar.get_prices(city)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_prices = []
        for result in results:
            if isinstance(result, list):
                all_prices.extend(result)
        
        return all_prices
    
    @staticmethod
    def aggregate_by_fuel_type(prices: List[Dict]) -> Dict:
        """Агрегировать цены по типам топлива"""
        aggregated = {}
        
        for price_data in prices:
            fuel_type = price_data["fuel_type"]
            
            if fuel_type not in aggregated:
                aggregated[fuel_type] = {
                    "stations": [],
                    "prices": []
                }
            
            aggregated[fuel_type]["stations"].append({
                "station": price_data["station"],
                "price": price_data["price"],
                "address": price_data.get("address"),
                "latitude": price_data.get("latitude"),
                "longitude": price_data.get("longitude")
            })
            aggregated[fuel_type]["prices"].append(price_data["price"])
        
        # Добавить статистику
        for fuel_type in aggregated:
            prices_list = aggregated[fuel_type]["prices"]
            aggregated[fuel_type]["min_price"] = min(prices_list)
            aggregated[fuel_type]["avg_price"] = round(sum(prices_list) / len(prices_list), 2)
            aggregated[fuel_type]["max_price"] = max(prices_list)
        
        return aggregated
