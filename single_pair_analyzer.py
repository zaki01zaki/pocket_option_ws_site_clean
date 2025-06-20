import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import json
import sqlite3
from dataclasses import dataclass
from simplified_indicators import SimplifiedTechnicalIndicators
import logging

@dataclass
class PairAnalysisConfig:
    """
    إعدادات التحليل المخصصة لكل زوج
    """
    pair_name: str
    volatility_threshold: float
    trend_sensitivity: float
    signal_confidence_threshold: float
    max_signals_per_hour: int
    trading_sessions: List[str]
    economic_factors: List[str]
    correlation_pairs: List[str]

class SinglePairAnalyzer:
    """
    نظام التحليل المركز لزوج عملة واحد
    """
    
    def __init__(self, pair_name: str = "EURUSD"):
        self.pair_name = pair_name
        self.indicators = SimplifiedTechnicalIndicators(pair_name)
        self.config = self._get_pair_config(pair_name)
        self.historical_data = []
        self.analysis_history = []
        self.signal_history = []
        
        # إعداد قاعدة البيانات
        self._setup_database()
        
        # إعداد نظام التسجيل
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"PairAnalyzer_{pair_name}")
    
    def _get_pair_config(self, pair_name: str) -> PairAnalysisConfig:
        """
        الحصول على إعدادات التحليل المخصصة للزوج
        """
        configs = {
            "EURUSD": PairAnalysisConfig(
                pair_name="EURUSD",
                volatility_threshold=0.0008,
                trend_sensitivity=0.7,
                signal_confidence_threshold=75.0,
                max_signals_per_hour=3,
                trading_sessions=["London", "New_York"],
                economic_factors=["ECB_Rate", "Fed_Rate", "GDP_EU", "GDP_US"],
                correlation_pairs=["GBPUSD", "USDCHF", "USDJPY"]
            ),
            "GBPUSD": PairAnalysisConfig(
                pair_name="GBPUSD",
                volatility_threshold=0.0012,
                trend_sensitivity=0.8,
                signal_confidence_threshold=70.0,
                max_signals_per_hour=4,
                trading_sessions=["London", "New_York"],
                economic_factors=["BOE_Rate", "Fed_Rate", "GDP_UK", "GDP_US"],
                correlation_pairs=["EURUSD", "EURGBP", "GBPJPY"]
            ),
            "USDJPY": PairAnalysisConfig(
                pair_name="USDJPY",
                volatility_threshold=0.0006,
                trend_sensitivity=0.6,
                signal_confidence_threshold=80.0,
                max_signals_per_hour=2,
                trading_sessions=["Tokyo", "New_York"],
                economic_factors=["Fed_Rate", "BOJ_Rate", "GDP_US", "GDP_JP"],
                correlation_pairs=["EURJPY", "GBPJPY", "AUDJPY"]
            )
        }
        
        return configs.get(pair_name, configs["EURUSD"])
    
    def _setup_database(self):
        """
        إعداد قاعدة البيانات لحفظ البيانات والتحليلات
        """
        self.db_path = f"/home/ubuntu/pocket_option_trading_platform/backend/data/{self.pair_name}_analysis.db"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول البيانات التاريخية
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                close_price REAL,
                volume REAL,
                timeframe TEXT
            )
        ''')
        
        # جدول التحليلات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                indicators_data TEXT,
                trend_analysis TEXT,
                volatility_analysis TEXT,
                session_analysis TEXT,
                overall_score REAL
            )
        ''')
        
        # جدول الإشارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                signal_type TEXT,
                confidence_score REAL,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                timeframe TEXT,
                status TEXT,
                result REAL
            )
        ''')
        
        # جدول الأداء
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                total_signals INTEGER,
                successful_signals INTEGER,
                success_rate REAL,
                total_profit REAL,
                max_drawdown REAL,
                sharpe_ratio REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_price_data(self, timestamp: datetime, open_price: float, 
                      high_price: float, low_price: float, close_price: float,
                      volume: float = 1000, timeframe: str = "1m"):
        """
        إضافة بيانات سعرية جديدة
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO price_data (timestamp, open_price, high_price, low_price, close_price, volume, timeframe)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, open_price, high_price, low_price, close_price, volume, timeframe))
        
        conn.commit()
        conn.close()
        
        # تحديث البيانات التاريخية في الذاكرة
        self.historical_data.append({
            'timestamp': timestamp,
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume,
            'timeframe': timeframe
        })
        
        # الاحتفاظ بآخر 1000 نقطة فقط في الذاكرة
        if len(self.historical_data) > 1000:
            self.historical_data = self.historical_data[-1000:]
    
    def get_recent_data(self, periods: int = 100, timeframe: str = "1m") -> Dict:
        """
        الحصول على البيانات الحديثة
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, open_price, high_price, low_price, close_price, volume
            FROM price_data 
            WHERE timeframe = ?
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (timeframe, periods))
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            return self._generate_sample_data(periods)
        
        # تحويل البيانات إلى arrays
        data.reverse()  # ترتيب تصاعدي
        
        timestamps = [row[0] for row in data]
        opens = np.array([row[1] for row in data])
        highs = np.array([row[2] for row in data])
        lows = np.array([row[3] for row in data])
        closes = np.array([row[4] for row in data])
        volumes = np.array([row[5] for row in data])
        
        return {
            'timestamps': timestamps,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': volumes
        }
    
    def _generate_sample_data(self, periods: int = 100) -> Dict:
        """
        توليد بيانات عينة للاختبار
        """
        np.random.seed(42)
        
        # أسعار أساسية حسب الزوج
        base_prices = {
            "EURUSD": 1.0850,
            "GBPUSD": 1.2650,
            "USDJPY": 149.50
        }
        
        base_price = base_prices.get(self.pair_name, 1.0850)
        
        # توليد تغييرات الأسعار
        price_changes = np.random.normal(0, self.config.volatility_threshold, periods)
        closes = base_price + np.cumsum(price_changes)
        
        # توليد أسعار الفتح والإغلاق والأعلى والأدنى
        opens = np.roll(closes, 1)
        opens[0] = base_price
        
        highs = closes + np.random.uniform(0, self.config.volatility_threshold * 0.5, periods)
        lows = closes - np.random.uniform(0, self.config.volatility_threshold * 0.5, periods)
        
        # التأكد من أن الأعلى أعلى من الإغلاق والأدنى أقل
        highs = np.maximum(highs, closes)
        lows = np.minimum(lows, closes)
        
        volumes = np.random.normal(1000, 200, periods)
        
        # توليد timestamps
        now = datetime.now()
        timestamps = [now - timedelta(minutes=i) for i in range(periods, 0, -1)]
        
        return {
            'timestamps': timestamps,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': volumes
        }
    
    def analyze_trading_session(self, timestamp: datetime) -> Dict:
        """
        تحليل جلسة التداول الحالية
        """
        hour = timestamp.hour
        
        # تحديد الجلسة
        session = "Off_Hours"
        session_strength = 0.3
        
        if 8 <= hour <= 16:  # جلسة لندن
            session = "London"
            session_strength = 0.9 if self.pair_name in ["EURUSD", "GBPUSD"] else 0.7
        elif 13 <= hour <= 21:  # جلسة نيويورك
            session = "New_York"
            session_strength = 0.9 if "USD" in self.pair_name else 0.6
        elif 23 <= hour or hour <= 7:  # جلسة طوكيو
            session = "Tokyo"
            session_strength = 0.9 if "JPY" in self.pair_name else 0.5
        
        # تحليل تداخل الجلسات
        overlap_bonus = 0
        if 13 <= hour <= 16:  # تداخل لندن ونيويورك
            overlap_bonus = 0.2
        elif 23 <= hour or hour <= 1:  # تداخل طوكيو ولندن
            overlap_bonus = 0.1
        
        session_strength = min(1.0, session_strength + overlap_bonus)
        
        return {
            "session": session,
            "strength": session_strength,
            "overlap": overlap_bonus > 0,
            "recommended_trading": session_strength > 0.6
        }
    
    def analyze_volatility_patterns(self, data: Dict) -> Dict:
        """
        تحليل أنماط التقلبات
        """
        closes = data['close']
        highs = data['high']
        lows = data['low']
        
        # حساب التقلبات
        returns = np.diff(closes) / closes[:-1]
        volatility = np.std(returns) * np.sqrt(1440)  # تقلبات يومية
        
        # حساب Average True Range
        tr1 = highs[1:] - lows[1:]
        tr2 = np.abs(highs[1:] - closes[:-1])
        tr3 = np.abs(lows[1:] - closes[:-1])
        true_range = np.maximum(tr1, np.maximum(tr2, tr3))
        atr = np.mean(true_range[-14:])  # ATR لآخر 14 فترة
        
        # تصنيف مستوى التقلب
        volatility_level = "low"
        if volatility > self.config.volatility_threshold * 2:
            volatility_level = "very_high"
        elif volatility > self.config.volatility_threshold * 1.5:
            volatility_level = "high"
        elif volatility > self.config.volatility_threshold:
            volatility_level = "moderate"
        
        # تحليل اتجاه التقلبات
        recent_volatility = np.std(returns[-10:]) * np.sqrt(1440)
        volatility_trend = "increasing" if recent_volatility > volatility else "decreasing"
        
        return {
            "current_volatility": volatility,
            "atr": atr,
            "volatility_level": volatility_level,
            "volatility_trend": volatility_trend,
            "trading_recommendation": volatility_level in ["moderate", "high"]
        }
    
    def analyze_trend_strength(self, data: Dict) -> Dict:
        """
        تحليل قوة الاتجاه متعدد الإطارات الزمنية
        """
        closes = data['close']
        
        # تحليل الاتجاهات على فترات مختلفة
        trends = {}
        
        # اتجاه قصير المدى (10 فترات)
        short_sma = np.mean(closes[-10:])
        short_trend = "bullish" if closes[-1] > short_sma else "bearish"
        short_strength = abs(closes[-1] - short_sma) / short_sma * 100
        
        trends["short_term"] = {
            "direction": short_trend,
            "strength": min(100, short_strength * 1000)
        }
        
        # اتجاه متوسط المدى (20 فترة)
        medium_sma = np.mean(closes[-20:])
        medium_trend = "bullish" if closes[-1] > medium_sma else "bearish"
        medium_strength = abs(closes[-1] - medium_sma) / medium_sma * 100
        
        trends["medium_term"] = {
            "direction": medium_trend,
            "strength": min(100, medium_strength * 1000)
        }
        
        # اتجاه طويل المدى (50 فترة)
        if len(closes) >= 50:
            long_sma = np.mean(closes[-50:])
            long_trend = "bullish" if closes[-1] > long_sma else "bearish"
            long_strength = abs(closes[-1] - long_sma) / long_sma * 100
            
            trends["long_term"] = {
                "direction": long_trend,
                "strength": min(100, long_strength * 1000)
            }
        
        # تحديد الاتجاه العام
        directions = [trends[key]["direction"] for key in trends.keys()]
        bullish_count = directions.count("bullish")
        bearish_count = directions.count("bearish")
        
        if bullish_count > bearish_count:
            overall_trend = "bullish"
            trend_confidence = bullish_count / len(directions) * 100
        elif bearish_count > bullish_count:
            overall_trend = "bearish"
            trend_confidence = bearish_count / len(directions) * 100
        else:
            overall_trend = "neutral"
            trend_confidence = 50
        
        return {
            "trends": trends,
            "overall_trend": overall_trend,
            "trend_confidence": trend_confidence,
            "trend_alignment": bullish_count == len(directions) or bearish_count == len(directions)
        }
    
    def calculate_support_resistance(self, data: Dict) -> Dict:
        """
        حساب مستويات الدعم والمقاومة
        """
        highs = data['high']
        lows = data['low']
        closes = data['close']
        
        # البحث عن القمم والقيعان
        peaks = []
        troughs = []
        
        for i in range(2, len(highs) - 2):
            # البحث عن القمم
            if (highs[i] > highs[i-1] and highs[i] > highs[i-2] and 
                highs[i] > highs[i+1] and highs[i] > highs[i+2]):
                peaks.append(highs[i])
            
            # البحث عن القيعان
            if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and 
                lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                troughs.append(lows[i])
        
        # حساب مستويات المقاومة والدعم
        resistance_levels = sorted(peaks, reverse=True)[:3] if peaks else [max(highs)]
        support_levels = sorted(troughs)[:3] if troughs else [min(lows)]
        
        current_price = closes[-1]
        
        # تحديد أقرب مستويات
        nearest_resistance = min(resistance_levels, key=lambda x: abs(x - current_price) if x > current_price else float('inf'))
        nearest_support = min(support_levels, key=lambda x: abs(x - current_price) if x < current_price else float('inf'))
        
        return {
            "resistance_levels": resistance_levels,
            "support_levels": support_levels,
            "nearest_resistance": nearest_resistance,
            "nearest_support": nearest_support,
            "current_price": current_price,
            "distance_to_resistance": (nearest_resistance - current_price) / current_price * 100 if nearest_resistance > current_price else None,
            "distance_to_support": (current_price - nearest_support) / current_price * 100 if nearest_support < current_price else None
        }
    
    def comprehensive_analysis(self, periods: int = 100) -> Dict:
        """
        التحليل الشامل للزوج
        """
        # الحصول على البيانات
        data = self.get_recent_data(periods)
        
        if len(data['close']) < 20:
            return {"error": "بيانات غير كافية للتحليل"}
        
        # حساب المؤشرات الفنية
        indicators = self.indicators.get_all_indicators(
            data['high'], data['low'], data['close'], data['volume']
        )
        
        # تحليل الجلسة
        session_analysis = self.analyze_trading_session(datetime.now())
        
        # تحليل التقلبات
        volatility_analysis = self.analyze_volatility_patterns(data)
        
        # تحليل الاتجاه
        trend_analysis = self.analyze_trend_strength(data)
        
        # تحليل الدعم والمقاومة
        support_resistance = self.calculate_support_resistance(data)
        
        # حساب النقاط الإجمالية
        overall_score = self._calculate_overall_score(
            indicators, session_analysis, volatility_analysis, trend_analysis
        )
        
        # حفظ التحليل في قاعدة البيانات
        self._save_analysis_result({
            "indicators": indicators,
            "session": session_analysis,
            "volatility": volatility_analysis,
            "trend": trend_analysis,
            "support_resistance": support_resistance,
            "overall_score": overall_score
        })
        
        return {
            "pair_name": self.pair_name,
            "timestamp": datetime.now().isoformat(),
            "indicators": indicators,
            "session_analysis": session_analysis,
            "volatility_analysis": volatility_analysis,
            "trend_analysis": trend_analysis,
            "support_resistance": support_resistance,
            "overall_score": overall_score,
            "recommendation": self._generate_recommendation(overall_score, indicators, trend_analysis)
        }
    
    def _calculate_overall_score(self, indicators: Dict, session: Dict, 
                                volatility: Dict, trend: Dict) -> float:
        """
        حساب النقاط الإجمالية للتحليل
        """
        scores = []
        
        # نقاط المؤشرات الفنية
        for indicator_name, indicator_data in indicators.items():
            if "quality_score" in indicator_data:
                scores.append(indicator_data["quality_score"])
        
        # نقاط الجلسة
        session_score = session["strength"] * 100
        scores.append(session_score)
        
        # نقاط التقلبات
        volatility_score = 80 if volatility["trading_recommendation"] else 40
        scores.append(volatility_score)
        
        # نقاط الاتجاه
        trend_score = trend["trend_confidence"]
        scores.append(trend_score)
        
        return np.mean(scores) if scores else 50.0
    
    def _generate_recommendation(self, overall_score: float, indicators: Dict, trend: Dict) -> Dict:
        """
        توليد التوصية النهائية
        """
        # جمع إشارات الشراء والبيع
        buy_signals = 0
        sell_signals = 0
        total_strength = 0
        
        for indicator_name, indicator_data in indicators.items():
            if "signal_type" in indicator_data and "signal_strength" in indicator_data:
                if indicator_data["signal_type"] == "buy":
                    buy_signals += 1
                    total_strength += indicator_data["signal_strength"]
                elif indicator_data["signal_type"] == "sell":
                    sell_signals += 1
                    total_strength += indicator_data["signal_strength"]
        
        # تحديد التوصية
        if buy_signals > sell_signals and overall_score > self.config.signal_confidence_threshold:
            recommendation = "BUY"
            confidence = min(100, (buy_signals / (buy_signals + sell_signals)) * overall_score)
        elif sell_signals > buy_signals and overall_score > self.config.signal_confidence_threshold:
            recommendation = "SELL"
            confidence = min(100, (sell_signals / (buy_signals + sell_signals)) * overall_score)
        else:
            recommendation = "HOLD"
            confidence = 50
        
        return {
            "action": recommendation,
            "confidence": confidence,
            "buy_signals": buy_signals,
            "sell_signals": sell_signals,
            "overall_score": overall_score,
            "trend_alignment": trend["overall_trend"] if recommendation.lower() == trend["overall_trend"] else False
        }
    
    def _save_analysis_result(self, analysis_data: Dict):
        """
        حفظ نتيجة التحليل في قاعدة البيانات
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_results (timestamp, indicators_data, trend_analysis, volatility_analysis, session_analysis, overall_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            json.dumps(analysis_data["indicators"]),
            json.dumps(analysis_data["trend"]),
            json.dumps(analysis_data["volatility"]),
            json.dumps(analysis_data["session"]),
            analysis_data["overall_score"]
        ))
        
        conn.commit()
        conn.close()
    
    def get_performance_metrics(self, days: int = 30) -> Dict:
        """
        الحصول على مقاييس الأداء
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # الحصول على الإشارات الأخيرة
        cursor.execute('''
            SELECT signal_type, confidence_score, result, timestamp
            FROM signals 
            WHERE timestamp > datetime('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days))
        
        signals = cursor.fetchall()
        conn.close()
        
        if not signals:
            return {
                "total_signals": 0,
                "success_rate": 0,
                "average_confidence": 0,
                "total_profit": 0
            }
        
        total_signals = len(signals)
        successful_signals = len([s for s in signals if s[2] and s[2] > 0])
        success_rate = (successful_signals / total_signals) * 100 if total_signals > 0 else 0
        average_confidence = np.mean([s[1] for s in signals])
        total_profit = sum([s[2] for s in signals if s[2]])
        
        return {
            "total_signals": total_signals,
            "successful_signals": successful_signals,
            "success_rate": success_rate,
            "average_confidence": average_confidence,
            "total_profit": total_profit,
            "signals_per_day": total_signals / days
        }

# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء محلل للزوج EURUSD
    analyzer = SinglePairAnalyzer("EURUSD")
    
    # إضافة بيانات عينة
    base_price = 1.0850
    for i in range(100):
        timestamp = datetime.now() - timedelta(minutes=100-i)
        price_change = np.random.normal(0, 0.0008)
        price = base_price + price_change
        
        analyzer.add_price_data(
            timestamp=timestamp,
            open_price=price - np.random.uniform(-0.0002, 0.0002),
            high_price=price + np.random.uniform(0, 0.0005),
            low_price=price - np.random.uniform(0, 0.0005),
            close_price=price,
            volume=np.random.normal(1000, 200)
        )
        
        base_price = price
    
    # إجراء التحليل الشامل
    analysis_result = analyzer.comprehensive_analysis()
    
    # طباعة النتائج
    print(f"تحليل شامل للزوج: {analysis_result['pair_name']}")
    print(f"النقاط الإجمالية: {analysis_result['overall_score']:.2f}")
    print(f"التوصية: {analysis_result['recommendation']['action']}")
    print(f"مستوى الثقة: {analysis_result['recommendation']['confidence']:.2f}%")
    print(f"الاتجاه العام: {analysis_result['trend_analysis']['overall_trend']}")
    print(f"قوة الجلسة: {analysis_result['session_analysis']['strength']:.2f}")
    
    # الحصول على مقاييس الأداء
    performance = analyzer.get_performance_metrics()
    print(f"\nمقاييس الأداء:")
    print(f"إجمالي الإشارات: {performance['total_signals']}")
    print(f"معدل النجاح: {performance['success_rate']:.2f}%")

