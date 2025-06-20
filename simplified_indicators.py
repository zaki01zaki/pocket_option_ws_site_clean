import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import ta
from scipy import signal
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class SimplifiedTechnicalIndicators:
    """
    مجموعة المؤشرات الفنية المحسنة الـ12 مع تقنيات تقليل التذبذب - نسخة مبسطة
    """
    
    def __init__(self, pair_name: str = "EURUSD"):
        self.pair_name = pair_name
        
        # معاملات التحسين الخاصة بكل زوج
        self.pair_configs = {
            "EURUSD": {
                "rsi_period": 14,
                "rsi_smooth": 3,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "bb_period": 20,
                "bb_std": 2.0,
                "volatility_threshold": 0.001
            },
            "GBPUSD": {
                "rsi_period": 16,
                "rsi_smooth": 4,
                "macd_fast": 10,
                "macd_slow": 24,
                "macd_signal": 8,
                "bb_period": 18,
                "bb_std": 2.2,
                "volatility_threshold": 0.0012
            },
            "USDJPY": {
                "rsi_period": 12,
                "rsi_smooth": 2,
                "macd_fast": 14,
                "macd_slow": 28,
                "macd_signal": 10,
                "bb_period": 22,
                "bb_std": 1.8,
                "volatility_threshold": 0.0008
            }
        }
        
        self.config = self.pair_configs.get(pair_name, self.pair_configs["EURUSD"])
    
    def simple_smooth(self, data: np.ndarray, window: int = 3) -> np.ndarray:
        """
        تمهيد بسيط باستخدام المتوسط المتحرك
        """
        if len(data) < window:
            return data
        
        smoothed = np.zeros_like(data)
        for i in range(len(data)):
            start_idx = max(0, i - window + 1)
            smoothed[i] = np.mean(data[start_idx:i+1])
        
        return smoothed
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        حساب RSI مبسط
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """
        حساب MACD مبسط
        """
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram
        }
    
    def calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: float = 2) -> Dict:
        """
        حساب نطاقات بولينجر مبسطة
        """
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return {
            "upper": upper_band,
            "middle": sma,
            "lower": lower_band
        }
    
    def calculate_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, k_period: int = 14, d_period: int = 3) -> Dict:
        """
        حساب مؤشر Stochastic مبسط
        """
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return {
            "k": k_percent,
            "d": d_percent
        }
    
    def enhanced_rsi(self, prices: np.ndarray, high: np.ndarray, 
                    low: np.ndarray, volume: np.ndarray = None) -> Dict:
        """
        مؤشر RSI محسن مع تقليل التذبذب
        """
        period = self.config["rsi_period"]
        smooth_period = self.config["rsi_smooth"]
        
        # تحويل إلى pandas Series
        prices_series = pd.Series(prices)
        
        # حساب RSI
        rsi_values = self.calculate_rsi(prices_series, period)
        
        # تطبيق التمهيد
        rsi_smoothed = self.simple_smooth(rsi_values.values, smooth_period)
        
        # حساب مستويات ديناميكية
        recent_rsi = rsi_smoothed[-30:]
        rsi_mean = np.nanmean(recent_rsi)
        rsi_std = np.nanstd(recent_rsi)
        
        overbought_level = min(80, rsi_mean + 1.5 * rsi_std)
        oversold_level = max(20, rsi_mean - 1.5 * rsi_std)
        
        current_rsi = rsi_smoothed[-1] if len(rsi_smoothed) > 0 else 50
        
        signal_strength = 0
        signal_type = "neutral"
        
        if current_rsi > overbought_level:
            signal_strength = min(100, (current_rsi - overbought_level) / (100 - overbought_level) * 100)
            signal_type = "sell"
        elif current_rsi < oversold_level:
            signal_strength = min(100, (oversold_level - current_rsi) / oversold_level * 100)
            signal_type = "buy"
        
        return {
            "value": current_rsi,
            "overbought_level": overbought_level,
            "oversold_level": oversold_level,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(rsi_smoothed)
        }
    
    def enhanced_macd(self, prices: np.ndarray, volume: np.ndarray = None) -> Dict:
        """
        مؤشر MACD محسن
        """
        fast_period = self.config["macd_fast"]
        slow_period = self.config["macd_slow"]
        signal_period = self.config["macd_signal"]
        
        prices_series = pd.Series(prices)
        macd_data = self.calculate_macd(prices_series, fast_period, slow_period, signal_period)
        
        current_macd = macd_data["macd"].iloc[-1] if len(macd_data["macd"]) > 0 else 0
        current_signal = macd_data["signal"].iloc[-1] if len(macd_data["signal"]) > 0 else 0
        current_histogram = macd_data["histogram"].iloc[-1] if len(macd_data["histogram"]) > 0 else 0
        
        signal_type = "neutral"
        signal_strength = 0
        
        if current_macd > current_signal and current_histogram > 0:
            signal_type = "buy"
            signal_strength = min(100, abs(current_histogram) * 1000)
        elif current_macd < current_signal and current_histogram < 0:
            signal_type = "sell"
            signal_strength = min(100, abs(current_histogram) * 1000)
        
        return {
            "macd_line": current_macd,
            "signal_line": current_signal,
            "histogram": current_histogram,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(macd_data["macd"].values)
        }
    
    def enhanced_stochastic(self, high: np.ndarray, low: np.ndarray, 
                           close: np.ndarray) -> Dict:
        """
        مؤشر Stochastic محسن
        """
        high_series = pd.Series(high)
        low_series = pd.Series(low)
        close_series = pd.Series(close)
        
        stoch_data = self.calculate_stochastic(high_series, low_series, close_series)
        
        current_k = stoch_data["k"].iloc[-1] if len(stoch_data["k"]) > 0 else 50
        current_d = stoch_data["d"].iloc[-1] if len(stoch_data["d"]) > 0 else 50
        
        signal_type = "neutral"
        signal_strength = 0
        
        if current_k > 80 and current_k > current_d:
            signal_type = "sell"
            signal_strength = min(100, (current_k - 80) / 20 * 100)
        elif current_k < 20 and current_k < current_d:
            signal_type = "buy"
            signal_strength = min(100, (20 - current_k) / 20 * 100)
        
        return {
            "k_value": current_k,
            "d_value": current_d,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(stoch_data["k"].values)
        }
    
    def enhanced_bollinger_bands(self, prices: np.ndarray) -> Dict:
        """
        نطاقات بولينجر محسنة
        """
        period = self.config["bb_period"]
        std_dev = self.config["bb_std"]
        
        prices_series = pd.Series(prices)
        bb_data = self.calculate_bollinger_bands(prices_series, period, std_dev)
        
        current_price = prices[-1]
        current_upper = bb_data["upper"].iloc[-1] if len(bb_data["upper"]) > 0 else current_price * 1.02
        current_lower = bb_data["lower"].iloc[-1] if len(bb_data["lower"]) > 0 else current_price * 0.98
        current_middle = bb_data["middle"].iloc[-1] if len(bb_data["middle"]) > 0 else current_price
        
        bb_position = (current_price - current_lower) / (current_upper - current_lower) * 100
        
        signal_type = "neutral"
        signal_strength = 0
        
        if bb_position > 80:
            signal_type = "sell"
            signal_strength = min(100, (bb_position - 80) / 20 * 100)
        elif bb_position < 20:
            signal_type = "buy"
            signal_strength = min(100, (20 - bb_position) / 20 * 100)
        
        return {
            "upper_band": current_upper,
            "middle_band": current_middle,
            "lower_band": current_lower,
            "bb_position": bb_position,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(bb_data["middle"].values)
        }
    
    def enhanced_williams_r(self, high: np.ndarray, low: np.ndarray, 
                           close: np.ndarray) -> Dict:
        """
        مؤشر Williams %R محسن
        """
        period = 14
        
        high_series = pd.Series(high)
        low_series = pd.Series(low)
        close_series = pd.Series(close)
        
        highest_high = high_series.rolling(window=period).max()
        lowest_low = low_series.rolling(window=period).min()
        
        williams_r = -100 * ((highest_high - close_series) / (highest_high - lowest_low))
        
        current_willr = williams_r.iloc[-1] if len(williams_r) > 0 else -50
        
        signal_type = "neutral"
        signal_strength = 0
        
        if current_willr > -20:
            signal_type = "sell"
            signal_strength = min(100, (current_willr + 20) / 20 * 100)
        elif current_willr < -80:
            signal_type = "buy"
            signal_strength = min(100, (-80 - current_willr) / 20 * 100)
        
        return {
            "value": current_willr,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(williams_r.values)
        }
    
    def enhanced_cci(self, high: np.ndarray, low: np.ndarray, 
                    close: np.ndarray) -> Dict:
        """
        مؤشر CCI محسن
        """
        period = 20
        
        high_series = pd.Series(high)
        low_series = pd.Series(low)
        close_series = pd.Series(close)
        
        typical_price = (high_series + low_series + close_series) / 3
        sma_tp = typical_price.rolling(window=period).mean()
        mad = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
        
        cci = (typical_price - sma_tp) / (0.015 * mad)
        
        current_cci = cci.iloc[-1] if len(cci) > 0 else 0
        
        signal_type = "neutral"
        signal_strength = 0
        
        if current_cci > 100:
            signal_type = "sell"
            signal_strength = min(100, (current_cci - 100) / 100 * 100)
        elif current_cci < -100:
            signal_type = "buy"
            signal_strength = min(100, (-100 - current_cci) / 100 * 100)
        
        return {
            "value": current_cci,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(cci.values)
        }
    
    def enhanced_adx(self, high: np.ndarray, low: np.ndarray, 
                    close: np.ndarray) -> Dict:
        """
        مؤشر ADX محسن
        """
        period = 14
        
        high_series = pd.Series(high)
        low_series = pd.Series(low)
        close_series = pd.Series(close)
        
        # حساب True Range
        tr1 = high_series - low_series
        tr2 = abs(high_series - close_series.shift(1))
        tr3 = abs(low_series - close_series.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # حساب Directional Movement
        plus_dm = high_series.diff()
        minus_dm = low_series.diff()
        
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0
        minus_dm = abs(minus_dm)
        
        # تمهيد
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
        
        # حساب ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        
        current_adx = adx.iloc[-1] if len(adx) > 0 else 25
        current_plus_di = plus_di.iloc[-1] if len(plus_di) > 0 else 25
        current_minus_di = minus_di.iloc[-1] if len(minus_di) > 0 else 25
        
        trend_strength = "weak"
        if current_adx > 40:
            trend_strength = "very_strong"
        elif current_adx > 30:
            trend_strength = "strong"
        elif current_adx > 20:
            trend_strength = "moderate"
        
        trend_direction = "neutral"
        signal_strength = 0
        
        if current_plus_di > current_minus_di and current_adx > 25:
            trend_direction = "bullish"
            signal_strength = min(100, (current_plus_di - current_minus_di) / current_plus_di * 100)
        elif current_minus_di > current_plus_di and current_adx > 25:
            trend_direction = "bearish"
            signal_strength = min(100, (current_minus_di - current_plus_di) / current_minus_di * 100)
        
        return {
            "adx": current_adx,
            "plus_di": current_plus_di,
            "minus_di": current_minus_di,
            "trend_strength": trend_strength,
            "trend_direction": trend_direction,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(adx.values)
        }
    
    def _calculate_quality_score(self, indicator_values: np.ndarray) -> float:
        """
        حساب نقاط الجودة للمؤشر
        """
        if len(indicator_values) < 10:
            return 50.0
        
        # إزالة القيم NaN
        clean_values = indicator_values[~np.isnan(indicator_values)]
        
        if len(clean_values) < 5:
            return 50.0
        
        # حساب الاستقرار
        stability = 100 - (np.std(clean_values[-20:]) / (np.mean(np.abs(clean_values[-20:])) + 1e-8) * 100)
        stability = max(0, min(100, stability))
        
        # حساب الاتساق
        if len(clean_values) > 10:
            recent_trend = np.diff(clean_values[-10:])
            consistency = 100 - (np.std(recent_trend) / (np.mean(np.abs(recent_trend)) + 1e-8) * 100)
            consistency = max(0, min(100, consistency))
        else:
            consistency = 50
        
        # النتيجة النهائية
        quality_score = (stability * 0.6 + consistency * 0.4)
        
        return round(quality_score, 1)
    
    def get_all_indicators(self, high: np.ndarray, low: np.ndarray, 
                          close: np.ndarray, volume: np.ndarray = None) -> Dict:
        """
        حساب جميع المؤشرات المحسنة
        """
        indicators = {}
        
        try:
            indicators["rsi"] = self.enhanced_rsi(close, high, low, volume)
        except Exception as e:
            indicators["rsi"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        try:
            indicators["macd"] = self.enhanced_macd(close, volume)
        except Exception as e:
            indicators["macd"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        try:
            indicators["stochastic"] = self.enhanced_stochastic(high, low, close)
        except Exception as e:
            indicators["stochastic"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        try:
            indicators["williams_r"] = self.enhanced_williams_r(high, low, close)
        except Exception as e:
            indicators["williams_r"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        try:
            indicators["cci"] = self.enhanced_cci(high, low, close)
        except Exception as e:
            indicators["cci"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        try:
            indicators["adx"] = self.enhanced_adx(high, low, close)
        except Exception as e:
            indicators["adx"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        try:
            indicators["bollinger_bands"] = self.enhanced_bollinger_bands(close)
        except Exception as e:
            indicators["bollinger_bands"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        # إضافة مؤشرات إضافية مبسطة
        try:
            # مؤشر المتوسط المتحرك البسيط
            sma_20 = pd.Series(close).rolling(window=20).mean().iloc[-1]
            sma_50 = pd.Series(close).rolling(window=50).mean().iloc[-1]
            current_price = close[-1]
            
            sma_signal = "neutral"
            sma_strength = 0
            
            if current_price > sma_20 > sma_50:
                sma_signal = "buy"
                sma_strength = min(100, (current_price - sma_20) / sma_20 * 1000)
            elif current_price < sma_20 < sma_50:
                sma_signal = "sell"
                sma_strength = min(100, (sma_20 - current_price) / sma_20 * 1000)
            
            indicators["sma"] = {
                "sma_20": sma_20,
                "sma_50": sma_50,
                "current_price": current_price,
                "signal_type": sma_signal,
                "signal_strength": sma_strength,
                "quality_score": 75.0
            }
        except Exception as e:
            indicators["sma"] = {"error": str(e), "signal_type": "neutral", "signal_strength": 0}
        
        return indicators

# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء بيانات تجريبية
    np.random.seed(42)
    n_points = 100
    
    # محاكاة أسعار
    base_price = 1.0850
    price_changes = np.random.normal(0, 0.001, n_points)
    prices = base_price + np.cumsum(price_changes)
    
    high = prices + np.random.uniform(0, 0.0005, n_points)
    low = prices - np.random.uniform(0, 0.0005, n_points)
    volume = np.random.normal(1000, 200, n_points)
    
    # إنشاء مثيل المؤشرات المحسنة
    indicators = SimplifiedTechnicalIndicators("EURUSD")
    
    # حساب جميع المؤشرات
    results = indicators.get_all_indicators(high, low, prices, volume)
    
    # طباعة النتائج
    for indicator_name, indicator_data in results.items():
        if "error" not in indicator_data:
            print(f"\n{indicator_name.upper()}:")
            for key, value in indicator_data.items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")
        else:
            print(f"\n{indicator_name.upper()}: خطأ - {indicator_data['error']}")

