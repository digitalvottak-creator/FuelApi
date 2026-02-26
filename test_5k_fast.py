import asyncio
import aiohttp
import time

API_KEY = "NPs8Yt-ZElgc69A_x36pIrkhSbzWr9ihkIJtAeOeNR0"
BASE_URL = "http://localhost:8000"

async def get_stats(session):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with session.get(f"{BASE_URL}/account/stats", headers=headers) as resp:
        return await resp.json()

async def make_request(session, semaphore):
    """Отправить один запрос с семафором для контроля параллелизма"""
    async with semaphore:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        try:
            async with session.get(
                f"{BASE_URL}/fuel?city=odessa&fuel_type=A95",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60, connect=10)
            ) as resp:
                if resp.status == 200:
                    await resp.read()
                    return True
                else:
                    return False
        except asyncio.TimeoutError:
            print(f"❌ Timeout")
            return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False

async def main():
    print("=== НАЧАЛЬНАЯ СТАТИСТИКА ===")
    
    # Более мягкие настройки коннектора
    connector = aiohttp.TCPConnector(
        limit=100,  # Меньше соединений
        limit_per_host=100,
        ttl_dns_cache=300,
        enable_cleanup_closed=True
    )
    
    timeout = aiohttp.ClientTimeout(total=60)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        stats = await get_stats(session)
        print(f"Используется: {stats['api_usage']['total_requests_used']} запросов")
        print(f"Доступно: {stats['api_usage']['total_requests_available']} запросов\n")
        
        TOTAL = 5000
        MAX_CONCURRENT = 50  # Уменьшил с 500 до 50
        
        print(f"=== ОТПРАВЛЯЮ {TOTAL} ЗАПРОСОВ ({MAX_CONCURRENT} одновременно) ===\n")
        
        # Семафор для контроля количества одновременных запросов
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        
        start_time = time.time()
        
        # Создаём задачи со временем
        tasks = [make_request(session, semaphore) for _ in range(TOTAL)]
        
        # Отправляем с прогрессом
        results = []
        for i, task in enumerate(asyncio.as_completed(tasks), 1):
            try:
                result = await task
                results.append(result)
                
                if i % 500 == 0:
                    elapsed = time.time() - start_time
                    success = sum(results)
                    rps = i / elapsed
                    print(f"✓ Обработано {i}/{TOTAL} запросов ({rps:.2f} req/s) - успешно: {success}")
            except Exception as e:
                print(f"Error: {e}")
                results.append(False)
        
        success_count = sum(1 for r in results if r is True)
        error_count = TOTAL - success_count
        
        elapsed = time.time() - start_time
        
        print(f"\n✓ Успешно: {success_count} запросов")
        print(f"❌ Ошибок: {error_count} запросов")
        print(f"⏱️  Время: {elapsed:.2f} секунд")
        print(f"📊 Скорость: {success_count / elapsed:.2f} запросов/сек\n")
        
        # Небольшая задержка перед финальной статистикой
        await asyncio.sleep(1)
        
        print("=== ФИНАЛЬНАЯ СТАТИСТИКА ===")
        stats = await get_stats(session)
        print(f"Используется: {stats['api_usage']['total_requests_used']} запросов")
        print(f"Доступно: {stats['api_usage']['total_requests_available']} запросов")
        print(f"Осталось: {stats['api_usage']['total_requests_available'] - stats['api_usage']['total_requests_used']} запросов")
        print(f"Процент использования: {stats['api_usage']['progress_percent']:.1f}%")

# Запуск
if __name__ == "__main__":
    asyncio.run(main())