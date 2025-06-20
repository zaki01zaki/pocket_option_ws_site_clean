import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json

class TradeDirection(Enum):
    """اتجاهات التداول"""
    CALL = "call"  # شراء/صعود
    PUT = "put"    # بيع/هبوط
    NEUTRAL = "neutral"  # محايد

class TradeDuration(Enum):
    """مدد الصفقات المتاحة"""
    ONE_MINUTE = "1m"
    TWO_MINUTES = "2m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    TEN_MINUTES = "10m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"

@dataclass
class TradeSignal:
    """إشارة التداول مع المدة والاتجاه"""
    pair: str
    direction: TradeDirection
    duration: TradeDuration
    confidence: float
    entry_price: float
    expected_exit_price: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    timestamp: datetime
    expiry_time: datetime
    signal_strength: float
    risk_level: str
    success_probability: float

@dataclass
class LiveAnalysis:
    """التحليل المباشر"""
    pair: str
    current_price: float
    price_change: float
    price_change_percent: float
    trend_direction: str
    trend_strength: float
    volatility: float
    volume: float
    support_level: float
    resistance_level: float
    next_key_level: float
    market_sentiment: str
    session_strength: float
    timestamp: datetime

class TradeDurationAnalyzer:
    """محلل مدة الصفقات والاتجاه"""
    
    def __init__(self, pair_name: str = "EURUSD"):
        self.pair_name = pair_name
        self.price_history = []
        self.volatility_history = []
        self.trend_history = []
        
        # إعدادات المدة حسب التقلبات
        self.duration_settings = {
            TradeDuration.ONE_MINUTE: {
                "min_volatility": 0.0001,
                "max_volatility": 0.0005,
                "min_trend_strength": 60,
                "success_rate_modifier": 0.8
            },
            TradeDuration.TWO_MINUTES: {
                "min_volatility": 0.0002,
                "max_volatility": 0.0008,
                "min_trend_strength": 55,
                "success_rate_modifier": 0.85
            },
            TradeDuration.THREE_MINUTES: {
                "min_volatility": 0.0003,
                "max_volatility": 0.0010,
                "min_trend_strength": 50,
                "success_rate_modifier": 0.9
            },
            TradeDuration.FIVE_MINUTES: {
                "min_volatility": 0.0004,
                "max_volatility": 0.0015,
                "min_trend_strength": 45,
                "success_rate_modifier": 0.95
            },
            TradeDuration.TEN_MINUTES: {
                "min_volatility": 0.0006,
                "max_volatility": 0.0020,
                "min_trend_strength": 40,
                "success_rate_modifier": 1.0
            },
            TradeDuration.FIFTEEN_MINUTES: {
                "min_volatility": 0.0008,
                "max_volatility": 0.0025,
                "min_trend_strength": 35,
                "success_rate_modifier": 1.05
            },
            TradeDuration.THIRTY_MINUTES: {
                "min_volatility": 0.0010,
                "max_volatility": 0.0035,
                "min_trend_strength": 30,
                "success_rate_modifier": 1.1
            },
            TradeDuration.ONE_HOUR: {
                "min_volatility": 0.0015,
                "max_volatility": 0.0050,
                "min_trend_strength": 25,
                "success_rate_modifier": 1.15
            }
        }
    
    def add_price_data(self, price: float, volume: float = 1000, timestamp: datetime = None):
        """إضافة بيانات سعرية جديدة"""
        if timestamp is None:
            timestamp = datetime.now()
        
        price_data = {
            'price': price,
            'volume': volume,
            'timestamp': timestamp
        }
        
        self.price_history.append(price_data)
        
        # الاحتفاظ بآخر 200 نقطة فقط
        if len(self.price_history) > 200:
            self.price_history = self.price_history[-200:]
    
    def calculate_volatility(self, periods: int = 20) -> float:
        """حساب التقلبات"""
        if len(self.price_history) < periods:
            return 0.001  # قيمة افتراضية
        
        prices = [p['price'] for p in self.price_history[-periods:]]
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns)
        
        return volatility
    
    def calculate_trend_strength(self, periods: int = 20) -> Tuple[str, float]:
        """حساب قوة واتجاه الترند"""
        if len(self.price_history) < periods:
            return "neutral", 50.0
        
        prices = [p['price'] for p in self.price_history[-periods:]]
        
        # حساب المتوسط المتحرك قصير وطويل المدى
        short_ma = np.mean(prices[-5:])
        long_ma = np.mean(prices[-periods:])
        
        # تحديد الاتجاه
        if short_ma > long_ma:
            direction = "bullish"
            strength = min(100, ((short_ma - long_ma) / long_ma) * 10000)
        elif short_ma < long_ma:
            direction = "bearish"
            strength = min(100, ((long_ma - short_ma) / long_ma) * 10000)
        else:
            direction = "neutral"
            strength = 50.0
        
        return direction, strength
    
    def calculate_support_resistance(self) -> Tuple[float, float]:
        """حساب مستويات الدعم والمقاومة"""
        if len(self.price_history) < 20:
            current_price = self.price_history[-1]['price'] if self.price_history else 1.0
            return current_price * 0.999, current_price * 1.001
        
        prices = [p['price'] for p in self.price_history[-50:]]
        
        # البحث عن القمم والقيعان
        highs = []
        lows = []
        
        for i in range(2, len(prices) - 2):
            # قمة محلية
            if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                highs.append(prices[i])
            # قاع محلي
            if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                lows.append(prices[i])
        
        # أقرب مستويات دعم ومقاومة
        current_price = prices[-1]
        
        resistance = min([h for h in highs if h > current_price], default=current_price * 1.001)
        support = max([l for l in lows if l < current_price], default=current_price * 0.999)
        
        return support, resistance
    
    def determine_optimal_duration(self, volatility: float, trend_strength: float) -> List[TradeDuration]:
        """تحديد المدد المثلى للتداول"""
        suitable_durations = []
        
        for duration, settings in self.duration_settings.items():
            # فحص التقلبات
            if settings["min_volatility"] <= volatility <= settings["max_volatility"]:
                # فحص قوة الترند
                if trend_strength >= settings["min_trend_strength"]:
                    suitable_durations.append(duration)
        
        # ترتيب حسب الأفضلية
        if not suitable_durations:
            # إذا لم تكن هناك مدة مناسبة، اختر الأقرب
            suitable_durations = [TradeDuration.FIVE_MINUTES]
        
        return suitable_durations
    
    def calculate_success_probability(self, direction: TradeDirection, duration: TradeDuration, 
                                    trend_strength: float, volatility: float) -> float:
        """حساب احتمالية النجاح"""
        base_probability = 50.0
        
        # تعديل حسب قوة الترند
        if direction == TradeDirection.CALL and trend_strength > 0:
            base_probability += min(30, trend_strength * 0.3)
        elif direction == TradeDirection.PUT and trend_strength > 0:
            base_probability += min(30, trend_strength * 0.3)
        
        # تعديل حسب المدة
        duration_modifier = self.duration_settings[duration]["success_rate_modifier"]
        base_probability *= duration_modifier
        
        # تعديل حسب التقلبات
        optimal_volatility = 0.0008  # تقلبات مثلى
        volatility_factor = 1.0 - abs(volatility - optimal_volatility) / optimal_volatility
        base_probability *= max(0.7, volatility_factor)
        
        return min(95.0, max(20.0, base_probability))
    
    def calculate_price_targets(self, current_price: float, direction: TradeDirection, 
                              duration: TradeDuration, volatility: float) -> Tuple[float, float, float]:
        """حساب أهداف السعر"""
        duration_minutes = {
            TradeDuration.ONE_MINUTE: 1,
            TradeDuration.TWO_MINUTES: 2,
            TradeDuration.THREE_MINUTES: 3,
            TradeDuration.FIVE_MINUTES: 5,
            TradeDuration.TEN_MINUTES: 10,
            TradeDuration.FIFTEEN_MINUTES: 15,
            TradeDuration.THIRTY_MINUTES: 30,
            TradeDuration.ONE_HOUR: 60
        }
        
        minutes = duration_minutes[duration]
        expected_move = volatility * np.sqrt(minutes / 60) * current_price
        
        if direction == TradeDirection.CALL:
            expected_exit = current_price + expected_move
            take_profit = current_price + (expected_move * 1.5)
            stop_loss = current_price - (expected_move * 0.5)
        elif direction == TradeDirection.PUT:
            expected_exit = current_price - expected_move
            take_profit = current_price - (expected_move * 1.5)
            stop_loss = current_price + (expected_move * 0.5)
        else:
            expected_exit = current_price
            take_profit = current_price
            stop_loss = current_price
        
        return expected_exit, take_profit, stop_loss
    
    def generate_trade_signal(self) -> Optional[TradeSignal]:
        """توليد إشارة تداول مع المدة والاتجاه"""
        if len(self.price_history) < 20:
            return None
        
        current_price = self.price_history[-1]['price']
        current_time = datetime.now()
        
        # حساب المؤشرات
        volatility = self.calculate_volatility()
        trend_direction, trend_strength = self.calculate_trend_strength()
        support, resistance = self.calculate_support_resistance()
        
        # تحديد الاتجاه
        if trend_direction == "bullish" and trend_strength > 40:
            direction = TradeDirection.CALL
        elif trend_direction == "bearish" and trend_strength > 40:
            direction = TradeDirection.PUT
        else:
            direction = TradeDirection.NEUTRAL
        
        if direction == TradeDirection.NEUTRAL:
            return None
        
        # تحديد المدة المثلى
        suitable_durations = self.determine_optimal_duration(volatility, trend_strength)
        optimal_duration = suitable_durations[0]
        
        # حساب احتمالية النجاح
        success_probability = self.calculate_success_probability(
            direction, optimal_duration, trend_strength, volatility
        )
        
        # حساب أهداف السعر
        expected_exit, take_profit, stop_loss = self.calculate_price_targets(
            current_price, direction, optimal_duration, volatility
        )
        
        # حساب وقت انتهاء الصفقة
        duration_minutes = {
            TradeDuration.ONE_MINUTE: 1,
            TradeDuration.TWO_MINUTES: 2,
            TradeDuration.THREE_MINUTES: 3,
            TradeDuration.FIVE_MINUTES: 5,
            TradeDuration.TEN_MINUTES: 10,
            TradeDuration.FIFTEEN_MINUTES: 15,
            TradeDuration.THIRTY_MINUTES: 30,
            TradeDuration.ONE_HOUR: 60
        }
        
        expiry_time = current_time + timedelta(minutes=duration_minutes[optimal_duration])
        
        # تحديد مستوى المخاطر
        if volatility < 0.0005:
            risk_level = "منخفض"
        elif volatility < 0.0015:
            risk_level = "متوسط"
        else:
            risk_level = "عالي"
        
        # إنشاء الإشارة
        signal = TradeSignal(
            pair=self.pair_name,
            direction=direction,
            duration=optimal_duration,
            confidence=success_probability,
            entry_price=current_price,
            expected_exit_price=expected_exit,
            stop_loss=stop_loss,
            take_profit=take_profit,
            timestamp=current_time,
            expiry_time=expiry_time,
            signal_strength=trend_strength,
            risk_level=risk_level,
            success_probability=success_probability
        )
        
        return signal

class LiveMarketAnalyzer:
    """محلل السوق المباشر"""
    
    def __init__(self, pair_name: str = "EURUSD"):
        self.pair_name = pair_name
        self.price_history = []
        self.last_analysis = None
    
    def add_price_data(self, price: float, volume: float = 1000, timestamp: datetime = None):
        """إضافة بيانات سعرية جديدة"""
        if timestamp is None:
            timestamp = datetime.now()
        
        price_data = {
            'price': price,
            'volume': volume,
            'timestamp': timestamp
        }
        
        self.price_history.append(price_data)
        
        # الاحتفاظ بآخر 100 نقطة فقط
        if len(self.price_history) > 100:
            self.price_history = self.price_history[-100:]
    
    def calculate_price_change(self) -> Tuple[float, float]:
        """حساب تغيير السعر"""
        if len(self.price_history) < 2:
            return 0.0, 0.0
        
        current_price = self.price_history[-1]['price']
        previous_price = self.price_history[-2]['price']
        
        price_change = current_price - previous_price
        price_change_percent = (price_change / previous_price) * 100
        
        return price_change, price_change_percent
    
    def calculate_market_sentiment(self) -> str:
        """حساب معنويات السوق"""
        if len(self.price_history) < 10:
            return "محايد"
        
        recent_prices = [p['price'] for p in self.price_history[-10:]]
        price_changes = np.diff(recent_prices)
        
        positive_changes = sum(1 for change in price_changes if change > 0)
        negative_changes = sum(1 for change in price_changes if change < 0)
        
        if positive_changes > negative_changes * 1.5:
            return "إيجابي"
        elif negative_changes > positive_changes * 1.5:
            return "سلبي"
        else:
            return "محايد"
    
    def calculate_session_strength(self) -> float:
        """حساب قوة الجلسة"""
        current_hour = datetime.now().hour
        
        # جلسة آسيا (23-8)
        if 23 <= current_hour or current_hour <= 8:
            if "JPY" in self.pair_name:
                return 0.9
            else:
                return 0.4
        
        # جلسة لندن (8-17)
        elif 8 <= current_hour <= 17:
            if any(currency in self.pair_name for currency in ["EUR", "GBP", "CHF"]):
                return 0.9
            else:
                return 0.7
        
        # جلسة نيويورك (13-22)
        elif 13 <= current_hour <= 22:
            if "USD" in self.pair_name:
                return 0.9
            else:
                return 0.6
        
        return 0.3
    
    def generate_live_analysis(self) -> LiveAnalysis:
        """توليد التحليل المباشر"""
        if not self.price_history:
            # إنشاء بيانات افتراضية
            base_prices = {"EURUSD": 1.0850, "GBPUSD": 1.2650, "USDJPY": 149.50}
            current_price = base_prices.get(self.pair_name, 1.0850)
            
            return LiveAnalysis(
                pair=self.pair_name,
                current_price=current_price,
                price_change=0.0,
                price_change_percent=0.0,
                trend_direction="محايد",
                trend_strength=50.0,
                volatility=0.0008,
                volume=1000.0,
                support_level=current_price * 0.999,
                resistance_level=current_price * 1.001,
                next_key_level=current_price * 1.001,
                market_sentiment="محايد",
                session_strength=self.calculate_session_strength(),
                timestamp=datetime.now()
            )
        
        current_price = self.price_history[-1]['price']
        current_volume = self.price_history[-1]['volume']
        
        # حساب التغييرات
        price_change, price_change_percent = self.calculate_price_change()
        
        # حساب التقلبات
        if len(self.price_history) >= 20:
            prices = [p['price'] for p in self.price_history[-20:]]
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns)
        else:
            volatility = 0.0008
        
        # حساب الاتجاه
        if len(self.price_history) >= 10:
            recent_prices = [p['price'] for p in self.price_history[-10:]]
            if recent_prices[-1] > recent_prices[0]:
                trend_direction = "صاعد"
                trend_strength = min(100, ((recent_prices[-1] - recent_prices[0]) / recent_prices[0]) * 1000)
            elif recent_prices[-1] < recent_prices[0]:
                trend_direction = "هابط"
                trend_strength = min(100, ((recent_prices[0] - recent_prices[-1]) / recent_prices[0]) * 1000)
            else:
                trend_direction = "محايد"
                trend_strength = 50.0
        else:
            trend_direction = "محايد"
            trend_strength = 50.0
        
        # حساب الدعم والمقاومة
        support_level = current_price * 0.999
        resistance_level = current_price * 1.001
        
        if len(self.price_history) >= 20:
            prices = [p['price'] for p in self.price_history[-20:]]
            support_level = min(prices)
            resistance_level = max(prices)
        
        # تحديد المستوى الرئيسي التالي
        if price_change > 0:
            next_key_level = resistance_level
        else:
            next_key_level = support_level
        
        # معنويات السوق
        market_sentiment = self.calculate_market_sentiment()
        
        # قوة الجلسة
        session_strength = self.calculate_session_strength()
        
        analysis = LiveAnalysis(
            pair=self.pair_name,
            current_price=current_price,
            price_change=price_change,
            price_change_percent=price_change_percent,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            volatility=volatility,
            volume=current_volume,
            support_level=support_level,
            resistance_level=resistance_level,
            next_key_level=next_key_level,
            market_sentiment=market_sentiment,
            session_strength=session_strength,
            timestamp=datetime.now()
        )
        
        self.last_analysis = analysis
        return analysis

# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء محلل المدة والاتجاه
    duration_analyzer = TradeDurationAnalyzer("EURUSD")
    live_analyzer = LiveMarketAnalyzer("EURUSD")
    
    # محاكاة بيانات السوق
    base_price = 1.0850
    for i in range(50):
        # توليد تغيير سعر عشوائي
        price_change = np.random.normal(0, 0.0008)
        new_price = base_price + price_change
        volume = np.random.normal(1000, 200)
        
        # إضافة البيانات
        duration_analyzer.add_price_data(new_price, volume)
        live_analyzer.add_price_data(new_price, volume)
        
        base_price = new_price
    
    # توليد إشارة تداول
    trade_signal = duration_analyzer.generate_trade_signal()
    if trade_signal:
        print("=== إشارة التداول ===")
        print(f"الزوج: {trade_signal.pair}")
        print(f"الاتجاه: {trade_signal.direction.value}")
        print(f"المدة: {trade_signal.duration.value}")
        print(f"مستوى الثقة: {trade_signal.confidence:.1f}%")
        print(f"سعر الدخول: {trade_signal.entry_price:.5f}")
        print(f"السعر المتوقع: {trade_signal.expected_exit_price:.5f}")
        print(f"وقت انتهاء الصفقة: {trade_signal.expiry_time.strftime('%H:%M:%S')}")
        print(f"مستوى المخاطر: {trade_signal.risk_level}")
        print(f"احتمالية النجاح: {trade_signal.success_probability:.1f}%")
    
    # توليد التحليل المباشر
    live_analysis = live_analyzer.generate_live_analysis()
    print("\n=== التحليل المباشر ===")
    print(f"الزوج: {live_analysis.pair}")
    print(f"السعر الحالي: {live_analysis.current_price:.5f}")
    print(f"تغيير السعر: {live_analysis.price_change:+.5f} ({live_analysis.price_change_percent:+.2f}%)")
    print(f"اتجاه الترند: {live_analysis.trend_direction}")
    print(f"قوة الترند: {live_analysis.trend_strength:.1f}")
    print(f"مستوى الدعم: {live_analysis.support_level:.5f}")
    print(f"مستوى المقاومة: {live_analysis.resistance_level:.5f}")
    print(f"معنويات السوق: {live_analysis.market_sentiment}")
    print(f"قوة الجلسة: {live_analysis.session_strength:.1f}")

