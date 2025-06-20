import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
import sqlite3
import os
from typing import Dict, List, Optional, Callable
import time

class AlternativeAPIManager:
    """
    مدير APIs البديلة للحصول على أسعار السوق من مصادر متعددة
    """
    
    def __init__(self):
        self.apis = {}
        self.db_path = 'alternative_apis_data.db'
        self.setup_database()
        self.setup_logging()
        self.setup_apis()
    
    def setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('alternative_apis.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """إعداد قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول البيانات من APIs البديلة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                price REAL NOT NULL,
                bid_price REAL,
                ask_price REAL,
                volume REAL,
                change_24h REAL,
                high_24h REAL,
                low_24h REAL,
                market_cap REAL,
                response_time REAL,
                is_valid BOOLEAN DEFAULT 1
            )
        ''')
        
        # جدول إحصائيات الأداء
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT NOT NULL,
                response_time REAL,
                success_rate REAL,
                error_count INTEGER DEFAULT 0,
                last_error TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def setup_apis(self):
        """إعداد APIs المختلفة"""
        
        # Alpha Vantage API
        self.apis['alphavantage'] = {
            'base_url': 'https://www.alphavantage.co/query',
            'api_key': 'demo',  # يجب استبدالها بمفتاح حقيقي
            'rate_limit': 5,  # 5 طلبات في الدقيقة
            'last_request': 0,
            'supported_assets': ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'],
            'priority': 1
        }
        
        # Fixer.io API
        self.apis['fixer'] = {
            'base_url': 'http://data.fixer.io/api/latest',
            'api_key': 'demo',  # يجب استبدالها بمفتاح حقيقي
            'rate_limit': 100,  # 100 طلب في الشهر للحساب المجاني
            'last_request': 0,
            'supported_assets': ['EUR', 'GBP', 'USD', 'JPY', 'AUD', 'CAD'],
            'priority': 2
        }
        
        # CoinGecko API (للعملات المشفرة)
        self.apis['coingecko'] = {
            'base_url': 'https://api.coingecko.com/api/v3',
            'api_key': None,  # مجاني بدون مفتاح
            'rate_limit': 50,  # 50 طلب في الدقيقة
            'last_request': 0,
            'supported_assets': ['bitcoin', 'ethereum', 'litecoin', 'ripple'],
            'priority': 3
        }
        
        # Yahoo Finance (غير رسمي)
        self.apis['yahoo'] = {
            'base_url': 'https://query1.finance.yahoo.com/v8/finance/chart',
            'api_key': None,
            'rate_limit': 2000,  # حد عالي
            'last_request': 0,
            'supported_assets': ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'BTC-USD', 'ETH-USD'],
            'priority': 4
        }
        
        # Binance API (للعملات المشفرة)
        self.apis['binance'] = {
            'base_url': 'https://api.binance.com/api/v3',
            'api_key': None,
            'rate_limit': 1200,  # 1200 طلب في الدقيقة
            'last_request': 0,
            'supported_assets': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT'],
            'priority': 5
        }
    
    async def check_rate_limit(self, source: str) -> bool:
        """فحص حدود معدل الطلبات"""
        api_config = self.apis.get(source)
        if not api_config:
            return False
        
        current_time = time.time()
        time_since_last = current_time - api_config['last_request']
        min_interval = 60 / api_config['rate_limit']  # الحد الأدنى بين الطلبات
        
        if time_since_last < min_interval:
            await asyncio.sleep(min_interval - time_since_last)
        
        api_config['last_request'] = time.time()
        return True
    
    async def fetch_alphavantage_data(self, symbol: str) -> Optional[Dict]:
        """جلب البيانات من Alpha Vantage"""
        try:
            await self.check_rate_limit('alphavantage')
            
            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': symbol[:3],
                'to_currency': symbol[3:],
                'apikey': self.apis['alphavantage']['api_key']
            }
            
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(self.apis['alphavantage']['base_url'], params=params) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'Realtime Currency Exchange Rate' in data:
                            rate_data = data['Realtime Currency Exchange Rate']
                            return {
                                'source': 'alphavantage',
                                'asset_name': symbol,
                                'price': float(rate_data['5. Exchange Rate']),
                                'bid_price': float(rate_data.get('8. Bid Price', 0)),
                                'ask_price': float(rate_data.get('9. Ask Price', 0)),
                                'response_time': response_time,
                                'timestamp': datetime.now()
                            }
        
        except Exception as e:
            self.logger.error(f"خطأ في جلب بيانات Alpha Vantage: {e}")
            await self.log_api_error('alphavantage', str(e))
        
        return None
    
    async def fetch_fixer_data(self, base_currency: str = 'USD') -> Optional[Dict]:
        """جلب البيانات من Fixer.io"""
        try:
            await self.check_rate_limit('fixer')
            
            params = {
                'access_key': self.apis['fixer']['api_key'],
                'base': base_currency,
                'symbols': 'EUR,GBP,JPY,AUD,CAD'
            }
            
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(self.apis['fixer']['base_url'], params=params) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('success'):
                            rates = data['rates']
                            results = []
                            
                            for currency, rate in rates.items():
                                results.append({
                                    'source': 'fixer',
                                    'asset_name': f'{base_currency}{currency}',
                                    'price': float(rate),
                                    'response_time': response_time,
                                    'timestamp': datetime.now()
                                })
                            
                            return results
        
        except Exception as e:
            self.logger.error(f"خطأ في جلب بيانات Fixer: {e}")
            await self.log_api_error('fixer', str(e))
        
        return None
    
    async def fetch_coingecko_data(self, coin_ids: List[str]) -> Optional[List[Dict]]:
        """جلب البيانات من CoinGecko"""
        try:
            await self.check_rate_limit('coingecko')
            
            ids_str = ','.join(coin_ids)
            url = f"{self.apis['coingecko']['base_url']}/simple/price"
            params = {
                'ids': ids_str,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true'
            }
            
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(url, params=params) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        
                        for coin_id, coin_data in data.items():
                            results.append({
                                'source': 'coingecko',
                                'asset_name': f'{coin_id.upper()}USD',
                                'price': float(coin_data['usd']),
                                'change_24h': coin_data.get('usd_24h_change', 0),
                                'volume': coin_data.get('usd_24h_vol', 0),
                                'market_cap': coin_data.get('usd_market_cap', 0),
                                'response_time': response_time,
                                'timestamp': datetime.now()
                            })
                        
                        return results
        
        except Exception as e:
            self.logger.error(f"خطأ في جلب بيانات CoinGecko: {e}")
            await self.log_api_error('coingecko', str(e))
        
        return None
    
    async def fetch_yahoo_data(self, symbol: str) -> Optional[Dict]:
        """جلب البيانات من Yahoo Finance"""
        try:
            await self.check_rate_limit('yahoo')
            
            url = f"{self.apis['yahoo']['base_url']}/{symbol}"
            params = {
                'interval': '1m',
                'range': '1d'
            }
            
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(url, params=params) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'chart' in data and data['chart']['result']:
                            result = data['chart']['result'][0]
                            meta = result['meta']
                            
                            return {
                                'source': 'yahoo',
                                'asset_name': symbol,
                                'price': float(meta['regularMarketPrice']),
                                'high_24h': float(meta.get('dayHigh', 0)),
                                'low_24h': float(meta.get('dayLow', 0)),
                                'volume': float(meta.get('regularMarketVolume', 0)),
                                'response_time': response_time,
                                'timestamp': datetime.now()
                            }
        
        except Exception as e:
            self.logger.error(f"خطأ في جلب بيانات Yahoo: {e}")
            await self.log_api_error('yahoo', str(e))
        
        return None
    
    async def fetch_binance_data(self, symbol: str) -> Optional[Dict]:
        """جلب البيانات من Binance"""
        try:
            await self.check_rate_limit('binance')
            
            url = f"{self.apis['binance']['base_url']}/ticker/24hr"
            params = {'symbol': symbol}
            
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(url, params=params) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        return {
                            'source': 'binance',
                            'asset_name': symbol,
                            'price': float(data['lastPrice']),
                            'bid_price': float(data['bidPrice']),
                            'ask_price': float(data['askPrice']),
                            'high_24h': float(data['highPrice']),
                            'low_24h': float(data['lowPrice']),
                            'volume': float(data['volume']),
                            'change_24h': float(data['priceChangePercent']),
                            'response_time': response_time,
                            'timestamp': datetime.now()
                        }
        
        except Exception as e:
            self.logger.error(f"خطأ في جلب بيانات Binance: {e}")
            await self.log_api_error('binance', str(e))
        
        return None
    
    async def fetch_all_data(self, assets: List[str]) -> List[Dict]:
        """جلب البيانات من جميع المصادر المتاحة"""
        tasks = []
        
        for asset in assets:
            # تحديد المصادر المناسبة لكل أصل
            if asset in ['EURUSD', 'GBPUSD', 'USDJPY']:
                tasks.append(self.fetch_alphavantage_data(asset))
                tasks.append(self.fetch_yahoo_data(f'{asset}=X'))
            
            elif asset.endswith('USDT'):
                tasks.append(self.fetch_binance_data(asset))
            
            elif asset.lower() in ['bitcoin', 'ethereum', 'litecoin']:
                tasks.append(self.fetch_coingecko_data([asset.lower()]))
        
        # إضافة بيانات Fixer للعملات الرئيسية
        tasks.append(self.fetch_fixer_data())
        
        # تنفيذ جميع المهام بشكل متزامن
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # تجميع النتائج الصحيحة
        all_data = []
        for result in results:
            if isinstance(result, list):
                all_data.extend(result)
            elif isinstance(result, dict):
                all_data.append(result)
            elif isinstance(result, Exception):
                self.logger.error(f"خطأ في جلب البيانات: {result}")
        
        # حفظ البيانات في قاعدة البيانات
        for data in all_data:
            if data:
                await self.save_api_data(data)
        
        return all_data
    
    async def save_api_data(self, data: Dict):
        """حفظ البيانات في قاعدة البيانات"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO api_prices 
                (source, asset_name, price, bid_price, ask_price, volume, 
                 change_24h, high_24h, low_24h, market_cap, response_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('source'),
                data.get('asset_name'),
                data.get('price'),
                data.get('bid_price'),
                data.get('ask_price'),
                data.get('volume'),
                data.get('change_24h'),
                data.get('high_24h'),
                data.get('low_24h'),
                data.get('market_cap'),
                data.get('response_time')
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"تم حفظ بيانات {data.get('asset_name')} من {data.get('source')}")
        
        except Exception as e:
            self.logger.error(f"خطأ في حفظ بيانات API: {e}")
    
    async def log_api_error(self, source: str, error: str):
        """تسجيل أخطاء API"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO api_performance (source, response_time, success_rate, error_count, last_error)
                VALUES (?, ?, ?, ?, ?)
            ''', (source, 0, 0, 1, error))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل خطأ API: {e}")
    
    def get_best_price(self, asset_name: str, max_age_minutes: int = 5) -> Optional[Dict]:
        """الحصول على أفضل سعر من المصادر المختلفة"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # البحث عن أحدث الأسعار
            cursor.execute('''
                SELECT source, price, bid_price, ask_price, timestamp, response_time
                FROM api_prices
                WHERE asset_name = ? 
                AND datetime(timestamp) > datetime('now', '-{} minutes')
                ORDER BY timestamp DESC
            '''.format(max_age_minutes), (asset_name,))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return None
            
            # اختيار أفضل سعر بناءً على الأولوية والجودة
            best_price = None
            best_priority = float('inf')
            
            for result in results:
                source = result[0]
                api_priority = self.apis.get(source, {}).get('priority', 999)
                
                if api_priority < best_priority:
                    best_priority = api_priority
                    best_price = {
                        'source': source,
                        'price': result[1],
                        'bid_price': result[2],
                        'ask_price': result[3],
                        'timestamp': result[4],
                        'response_time': result[5]
                    }
            
            return best_price
        
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على أفضل سعر: {e}")
            return None
    
    def get_price_comparison(self, asset_name: str, max_age_minutes: int = 5) -> List[Dict]:
        """مقارنة الأسعار من مصادر مختلفة"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT source, price, timestamp, response_time
                FROM api_prices
                WHERE asset_name = ? 
                AND datetime(timestamp) > datetime('now', '-{} minutes')
                ORDER BY timestamp DESC
            '''.format(max_age_minutes), (asset_name,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'source': result[0],
                    'price': result[1],
                    'timestamp': result[2],
                    'response_time': result[3]
                }
                for result in results
            ]
        
        except Exception as e:
            self.logger.error(f"خطأ في مقارنة الأسعار: {e}")
            return []

# مثال على الاستخدام
async def main():
    api_manager = AlternativeAPIManager()
    
    # جلب البيانات لأصول مختلفة
    assets = ['EURUSD', 'GBPUSD', 'BTCUSDT', 'bitcoin']
    data = await api_manager.fetch_all_data(assets)
    
    print(f"تم جلب {len(data)} عنصر بيانات")
    
    # الحصول على أفضل سعر لـ EUR/USD
    best_price = api_manager.get_best_price('EURUSD')
    if best_price:
        print(f"أفضل سعر لـ EUR/USD: {best_price['price']} من {best_price['source']}")
    
    # مقارنة الأسعار
    comparison = api_manager.get_price_comparison('EURUSD')
    print(f"مقارنة أسعار EUR/USD من {len(comparison)} مصدر")

if __name__ == "__main__":
    asyncio.run(main())

