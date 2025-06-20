import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import ta
from scipy import signal
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class EnhancedTechnicalIndicators:
    """
    مجموعة المؤشرات الفنية المحسنة الـ12 مع تقنيات تقليل التذبذب
    """
    
    def __init__(self, pair_name: str = "EURUSD"):
        self.pair_name = pair_name
        self.scaler = StandardScaler()
        self.outlier_detector = IsolationForest(contamination=0.1, random_state=42)
        
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
    
    def adaptive_smooth(self, data: np.ndarray, volatility: np.ndarray, 
                       base_period: int = 3) -> np.ndarray:
        """
        تمهيد متكيف بناءً على التقلبات
        """
        smoothed = np.zeros_like(data)
        
        for i in range(len(data)):
            if i < base_period:
                smoothed[i] = data[i]
                continue
            
            # تحديد فترة التمهيد بناءً على التقلب
            vol_factor = volatility[i] / np.mean(volatility[max(0, i-20):i+1])
            adaptive_period = max(2, min(10, int(base_period * vol_factor)))
            
            start_idx = max(0, i - adaptive_period + 1)
            smoothed[i] = np.mean(data[start_idx:i+1])
        
        return smoothed
    
    def kalman_filter(self, data: np.ndarray, process_variance: float = 1e-5,
                     measurement_variance: float = 1e-1) -> np.ndarray:
        """
        مرشح كالمان للتمهيد المتقدم
        """
        n = len(data)
        filtered = np.zeros(n)
        
        # حالة أولية
        x = data[0]  # التقدير الأولي
        P = 1.0      # تباين الخطأ الأولي
        
        for i in range(n):
            # التنبؤ
            x_pred = x
            P_pred = P + process_variance
            
            # التحديث
            K = P_pred / (P_pred + measurement_variance)
            x = x_pred + K * (data[i] - x_pred)
            P = (1 - K) * P_pred
            
            filtered[i] = x
        
        return filtered
    
    def enhanced_rsi(self, prices: np.ndarray, high: np.ndarray, 
                    low: np.ndarray, volume: np.ndarray = None) -> Dict:
        """
        مؤشر RSI محسن مع تقليل التذبذب
        """
        period = self.config["rsi_period"]
        smooth_period = self.config["rsi_smooth"]
        
        # تحويل إلى pandas Series
        prices_series = pd.Series(prices)
        
        # حساب RSI التقليدي
        rsi_traditional = ta.momentum.RSIIndicator(prices_series, window=period).rsi().values
        
        # حساب التقلبات
        high_series = pd.Series(high)
        low_series = pd.Series(low)
        volatility = ta.volatility.AverageTrueRange(high_series, low_series, prices_series, window=14).average_true_range().values
        
        # تطبيق التمهيد المتكيف
        rsi_smoothed = self.adaptive_smooth(rsi_traditional, volatility, smooth_period)
        
        # تطبيق مرشح كالمان
        rsi_filtered = self.kalman_filter(rsi_smoothed)
        
        # حساب مستويات ديناميكية
        rsi_mean = np.nanmean(rsi_filtered[-50:])
        rsi_std = np.nanstd(rsi_filtered[-50:])
        
        overbought_level = min(80, rsi_mean + 1.5 * rsi_std)
        oversold_level = max(20, rsi_mean - 1.5 * rsi_std)
        
        # إشارات محسنة
        current_rsi = rsi_filtered[-1] if len(rsi_filtered) > 0 else 50
        
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
            "traditional": rsi_traditional[-1] if len(rsi_traditional) > 0 else 50,
            "smoothed": rsi_smoothed[-1] if len(rsi_smoothed) > 0 else 50,
            "filtered": current_rsi,
            "overbought_level": overbought_level,
            "oversold_level": oversold_level,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(rsi_filtered, volatility)
        }
    
    def enhanced_macd(self, prices: np.ndarray, volume: np.ndarray = None) -> Dict:
        """
        مؤشر MACD محسن مع تأكيدات متعددة
        """
        fast_period = self.config["macd_fast"]
        slow_period = self.config["macd_slow"]
        signal_period = self.config["macd_signal"]
        
        # حساب MACD التقليدي
        macd_line, macd_signal, macd_histogram = talib.MACD(
            prices, fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period
        )
        
        # تطبيق مرشح كالمان على خطوط MACD
        macd_filtered = self.kalman_filter(macd_line)
        signal_filtered = self.kalman_filter(macd_signal)
        histogram_filtered = macd_filtered - signal_filtered
        
        # حساب قوة الاتجاه
        trend_strength = np.abs(macd_filtered[-1]) / (np.std(macd_filtered[-20:]) + 1e-8)
        
        # تحديد الإشارات
        current_macd = macd_filtered[-1]
        current_signal = signal_filtered[-1]
        current_histogram = histogram_filtered[-1]
        
        signal_type = "neutral"
        signal_strength = 0
        
        # إشارة الشراء
        if current_macd > current_signal and current_histogram > 0:
            if len(histogram_filtered) > 1 and histogram_filtered[-2] <= 0:
                signal_type = "buy"
                signal_strength = min(100, trend_strength * 30)
        
        # إشارة البيع
        elif current_macd < current_signal and current_histogram < 0:
            if len(histogram_filtered) > 1 and histogram_filtered[-2] >= 0:
                signal_type = "sell"
                signal_strength = min(100, trend_strength * 30)
        
        # تأكيد بالحجم إذا كان متاحاً
        volume_confirmation = 1.0
        if volume is not None and len(volume) > 20:
            recent_volume = np.mean(volume[-5:])
            avg_volume = np.mean(volume[-20:])
            volume_confirmation = min(2.0, recent_volume / (avg_volume + 1e-8))
        
        signal_strength *= volume_confirmation
        
        return {
            "macd_line": current_macd,
            "signal_line": current_signal,
            "histogram": current_histogram,
            "trend_strength": trend_strength,
            "signal_type": signal_type,
            "signal_strength": min(100, signal_strength),
            "volume_confirmation": volume_confirmation,
            "quality_score": self._calculate_quality_score(macd_filtered, None)
        }
    
    def enhanced_stochastic(self, high: np.ndarray, low: np.ndarray, 
                           close: np.ndarray) -> Dict:
        """
        مؤشر Stochastic محسن مع نطاقات ديناميكية
        """
        # حساب Stochastic التقليدي
        slowk, slowd = talib.STOCH(high, low, close, 
                                  fastk_period=14, slowk_period=3, slowd_period=3)
        
        # تطبيق التمهيد المتكيف
        volatility = talib.ATR(high, low, close, timeperiod=14)
        stoch_k_smooth = self.adaptive_smooth(slowk, volatility, 3)
        stoch_d_smooth = self.adaptive_smooth(slowd, volatility, 3)
        
        # حساب نطاقات ديناميكية
        recent_stoch = stoch_k_smooth[-30:]
        stoch_mean = np.nanmean(recent_stoch)
        stoch_std = np.nanstd(recent_stoch)
        
        upper_band = min(85, stoch_mean + 1.5 * stoch_std)
        lower_band = max(15, stoch_mean - 1.5 * stoch_std)
        
        current_k = stoch_k_smooth[-1] if len(stoch_k_smooth) > 0 else 50
        current_d = stoch_d_smooth[-1] if len(stoch_d_smooth) > 0 else 50
        
        # تحديد الإشارات
        signal_type = "neutral"
        signal_strength = 0
        
        if current_k > upper_band and current_k > current_d:
            signal_type = "sell"
            signal_strength = min(100, (current_k - upper_band) / (100 - upper_band) * 100)
        elif current_k < lower_band and current_k < current_d:
            signal_type = "buy"
            signal_strength = min(100, (lower_band - current_k) / lower_band * 100)
        
        return {
            "k_value": current_k,
            "d_value": current_d,
            "upper_band": upper_band,
            "lower_band": lower_band,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(stoch_k_smooth, volatility)
        }
    
    def enhanced_williams_r(self, high: np.ndarray, low: np.ndarray, 
                           close: np.ndarray) -> Dict:
        """
        مؤشر Williams %R محسن
        """
        # حساب Williams %R التقليدي
        willr = talib.WILLR(high, low, close, timeperiod=14)
        
        # تطبيق مرشح كالمان
        willr_filtered = self.kalman_filter(willr)
        
        # تحويل إلى نطاق 0-100
        willr_normalized = (willr_filtered + 100)
        
        # حساب مستويات ديناميكية
        recent_willr = willr_normalized[-30:]
        willr_mean = np.nanmean(recent_willr)
        willr_std = np.nanstd(recent_willr)
        
        overbought = min(85, willr_mean + 1.5 * willr_std)
        oversold = max(15, willr_mean - 1.5 * willr_std)
        
        current_willr = willr_normalized[-1] if len(willr_normalized) > 0 else 50
        
        signal_type = "neutral"
        signal_strength = 0
        
        if current_willr > overbought:
            signal_type = "sell"
            signal_strength = min(100, (current_willr - overbought) / (100 - overbought) * 100)
        elif current_willr < oversold:
            signal_type = "buy"
            signal_strength = min(100, (oversold - current_willr) / oversold * 100)
        
        return {
            "value": current_willr,
            "overbought_level": overbought,
            "oversold_level": oversold,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(willr_filtered, None)
        }
    
    def enhanced_cci(self, high: np.ndarray, low: np.ndarray, 
                    close: np.ndarray) -> Dict:
        """
        مؤشر CCI محسن مع تطبيع متكيف
        """
        # حساب CCI التقليدي
        cci = talib.CCI(high, low, close, timeperiod=20)
        
        # تطبيق مرشح كالمان
        cci_filtered = self.kalman_filter(cci)
        
        # تطبيع متكيف
        recent_cci = cci_filtered[-50:]
        cci_mean = np.nanmean(recent_cci)
        cci_std = np.nanstd(recent_cci)
        
        # تطبيع إلى نطاق -100 إلى 100
        if cci_std > 0:
            cci_normalized = ((cci_filtered - cci_mean) / cci_std) * 50
            cci_normalized = np.clip(cci_normalized, -100, 100)
        else:
            cci_normalized = cci_filtered
        
        current_cci = cci_normalized[-1] if len(cci_normalized) > 0 else 0
        
        signal_type = "neutral"
        signal_strength = 0
        
        if current_cci > 70:
            signal_type = "sell"
            signal_strength = min(100, (current_cci - 70) / 30 * 100)
        elif current_cci < -70:
            signal_type = "buy"
            signal_strength = min(100, (-70 - current_cci) / 30 * 100)
        
        return {
            "value": current_cci,
            "normalized": current_cci,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(cci_filtered, None)
        }
    
    def enhanced_adx(self, high: np.ndarray, low: np.ndarray, 
                    close: np.ndarray) -> Dict:
        """
        مؤشر ADX محسن لقياس قوة الاتجاه
        """
        # حساب ADX و DI
        adx = talib.ADX(high, low, close, timeperiod=14)
        plus_di = talib.PLUS_DI(high, low, close, timeperiod=14)
        minus_di = talib.MINUS_DI(high, low, close, timeperiod=14)
        
        # تطبيق التمهيد
        volatility = talib.ATR(high, low, close, timeperiod=14)
        adx_smooth = self.adaptive_smooth(adx, volatility, 3)
        plus_di_smooth = self.adaptive_smooth(plus_di, volatility, 3)
        minus_di_smooth = self.adaptive_smooth(minus_di, volatility, 3)
        
        current_adx = adx_smooth[-1] if len(adx_smooth) > 0 else 25
        current_plus_di = plus_di_smooth[-1] if len(plus_di_smooth) > 0 else 25
        current_minus_di = minus_di_smooth[-1] if len(minus_di_smooth) > 0 else 25
        
        # تحديد قوة الاتجاه
        trend_strength = "weak"
        if current_adx > 40:
            trend_strength = "very_strong"
        elif current_adx > 30:
            trend_strength = "strong"
        elif current_adx > 20:
            trend_strength = "moderate"
        
        # تحديد اتجاه الاتجاه
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
            "quality_score": self._calculate_quality_score(adx_smooth, volatility)
        }
    
    def enhanced_bollinger_bands(self, prices: np.ndarray) -> Dict:
        """
        نطاقات بولينجر محسنة مع انحراف معياري متكيف
        """
        period = self.config["bb_period"]
        std_dev = self.config["bb_std"]
        
        # حساب نطاقات بولينجر التقليدية
        bb_upper, bb_middle, bb_lower = talib.BBANDS(
            prices, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev
        )
        
        # حساب التقلبات
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns[-20:]) if len(returns) >= 20 else np.std(returns)
        
        # تعديل الانحراف المعياري بناءً على التقلبات
        adaptive_std = std_dev * (1 + volatility * 10)
        
        # إعادة حساب النطاقات مع الانحراف المتكيف
        bb_upper_adaptive, bb_middle_adaptive, bb_lower_adaptive = talib.BBANDS(
            prices, timeperiod=period, nbdevup=adaptive_std, nbdevdn=adaptive_std
        )
        
        current_price = prices[-1]
        current_upper = bb_upper_adaptive[-1] if len(bb_upper_adaptive) > 0 else current_price * 1.02
        current_lower = bb_lower_adaptive[-1] if len(bb_lower_adaptive) > 0 else current_price * 0.98
        current_middle = bb_middle_adaptive[-1] if len(bb_middle_adaptive) > 0 else current_price
        
        # حساب موقع السعر في النطاق
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
            "bandwidth": (current_upper - current_lower) / current_middle * 100,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(bb_middle_adaptive, None)
        }
    
    def enhanced_parabolic_sar(self, high: np.ndarray, low: np.ndarray) -> Dict:
        """
        مؤشر Parabolic SAR محسن
        """
        # حساب Parabolic SAR التقليدي
        sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
        
        # تطبيق مرشح للتقلبات المفاجئة
        volatility = talib.ATR(high, low, (high + low) / 2, timeperiod=14)
        
        # تحديد الاتجاه
        current_price = (high[-1] + low[-1]) / 2
        current_sar = sar[-1] if len(sar) > 0 else current_price
        
        trend_direction = "bullish" if current_price > current_sar else "bearish"
        
        # حساب قوة الإشارة
        distance = abs(current_price - current_sar) / current_price * 100
        signal_strength = min(100, distance * 50)
        
        return {
            "sar_value": current_sar,
            "current_price": current_price,
            "trend_direction": trend_direction,
            "distance_percent": distance,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(sar, volatility)
        }
    
    def enhanced_ichimoku(self, high: np.ndarray, low: np.ndarray, 
                         close: np.ndarray) -> Dict:
        """
        مؤشر Ichimoku محسن
        """
        # حساب خطوط Ichimoku
        tenkan_sen = (talib.MAX(high, 9) + talib.MIN(low, 9)) / 2
        kijun_sen = (talib.MAX(high, 26) + talib.MIN(low, 26)) / 2
        
        # تطبيق التمهيد
        volatility = talib.ATR(high, low, close, timeperiod=14)
        tenkan_smooth = self.adaptive_smooth(tenkan_sen, volatility, 2)
        kijun_smooth = self.adaptive_smooth(kijun_sen, volatility, 3)
        
        current_price = close[-1]
        current_tenkan = tenkan_smooth[-1] if len(tenkan_smooth) > 0 else current_price
        current_kijun = kijun_smooth[-1] if len(kijun_smooth) > 0 else current_price
        
        # تحديد الإشارات
        signal_type = "neutral"
        signal_strength = 0
        
        if current_tenkan > current_kijun and current_price > current_tenkan:
            signal_type = "buy"
            signal_strength = min(100, (current_tenkan - current_kijun) / current_kijun * 1000)
        elif current_tenkan < current_kijun and current_price < current_tenkan:
            signal_type = "sell"
            signal_strength = min(100, (current_kijun - current_tenkan) / current_kijun * 1000)
        
        return {
            "tenkan_sen": current_tenkan,
            "kijun_sen": current_kijun,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(tenkan_smooth, volatility)
        }
    
    def enhanced_atr(self, high: np.ndarray, low: np.ndarray, 
                    close: np.ndarray) -> Dict:
        """
        مؤشر ATR محسن مع تطبيع ديناميكي
        """
        # حساب ATR التقليدي
        atr = talib.ATR(high, low, close, timeperiod=14)
        
        # تطبيق متوسط متحرك متكيف
        atr_smooth = self.adaptive_smooth(atr, atr, 5)
        
        # تطبيع بناءً على السعر
        atr_normalized = (atr_smooth / close) * 100
        
        current_atr = atr_smooth[-1] if len(atr_smooth) > 0 else 0
        current_atr_norm = atr_normalized[-1] if len(atr_normalized) > 0 else 0
        
        # تحديد مستوى التقلب
        volatility_level = "low"
        if current_atr_norm > 1.5:
            volatility_level = "very_high"
        elif current_atr_norm > 1.0:
            volatility_level = "high"
        elif current_atr_norm > 0.5:
            volatility_level = "moderate"
        
        return {
            "atr_value": current_atr,
            "atr_normalized": current_atr_norm,
            "volatility_level": volatility_level,
            "quality_score": self._calculate_quality_score(atr_smooth, None)
        }
    
    def enhanced_obv(self, close: np.ndarray, volume: np.ndarray) -> Dict:
        """
        مؤشر OBV محسن مع تحليل تدفق الأموال
        """
        if volume is None:
            # محاكاة الحجم إذا لم يكن متاحاً
            volume = np.random.normal(1000, 200, len(close))
        
        # حساب OBV التقليدي
        obv = talib.OBV(close, volume)
        
        # تطبيق التمهيد
        obv_smooth = self.adaptive_smooth(obv, np.abs(np.diff(close, prepend=close[0])), 5)
        
        # حساب اتجاه OBV
        obv_trend = np.diff(obv_smooth[-10:])
        trend_direction = "bullish" if np.mean(obv_trend) > 0 else "bearish"
        
        # حساب قوة الإشارة
        obv_change = (obv_smooth[-1] - obv_smooth[-10]) / abs(obv_smooth[-10]) * 100
        signal_strength = min(100, abs(obv_change) * 10)
        
        return {
            "obv_value": obv_smooth[-1] if len(obv_smooth) > 0 else 0,
            "trend_direction": trend_direction,
            "obv_change_percent": obv_change,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(obv_smooth, None)
        }
    
    def enhanced_mfi(self, high: np.ndarray, low: np.ndarray, 
                    close: np.ndarray, volume: np.ndarray) -> Dict:
        """
        مؤشر Money Flow Index محسن
        """
        if volume is None:
            volume = np.random.normal(1000, 200, len(close))
        
        # حساب MFI التقليدي
        mfi = talib.MFI(high, low, close, volume, timeperiod=14)
        
        # تطبيق مرشح كالمان
        mfi_filtered = self.kalman_filter(mfi)
        
        # حساب مستويات ديناميكية
        recent_mfi = mfi_filtered[-30:]
        mfi_mean = np.nanmean(recent_mfi)
        mfi_std = np.nanstd(recent_mfi)
        
        overbought = min(85, mfi_mean + 1.5 * mfi_std)
        oversold = max(15, mfi_mean - 1.5 * mfi_std)
        
        current_mfi = mfi_filtered[-1] if len(mfi_filtered) > 0 else 50
        
        signal_type = "neutral"
        signal_strength = 0
        
        if current_mfi > overbought:
            signal_type = "sell"
            signal_strength = min(100, (current_mfi - overbought) / (100 - overbought) * 100)
        elif current_mfi < oversold:
            signal_type = "buy"
            signal_strength = min(100, (oversold - current_mfi) / oversold * 100)
        
        return {
            "mfi_value": current_mfi,
            "overbought_level": overbought,
            "oversold_level": oversold,
            "signal_type": signal_type,
            "signal_strength": signal_strength,
            "quality_score": self._calculate_quality_score(mfi_filtered, None)
        }
    
    def _calculate_quality_score(self, indicator_values: np.ndarray, 
                                volatility: np.ndarray = None) -> float:
        """
        حساب نقاط الجودة للمؤشر
        """
        if len(indicator_values) < 10:
            return 50.0
        
        # حساب الاستقرار
        stability = 100 - (np.std(indicator_values[-20:]) / (np.mean(np.abs(indicator_values[-20:])) + 1e-8) * 100)
        stability = max(0, min(100, stability))
        
        # حساب الاتساق
        recent_trend = np.diff(indicator_values[-10:])
        consistency = 100 - (np.std(recent_trend) / (np.mean(np.abs(recent_trend)) + 1e-8) * 100)
        consistency = max(0, min(100, consistency))
        
        # حساب قوة الإشارة
        signal_strength = min(100, np.abs(indicator_values[-1]) / (np.std(indicator_values[-20:]) + 1e-8) * 20)
        
        # النتيجة النهائية
        quality_score = (stability * 0.4 + consistency * 0.3 + signal_strength * 0.3)
        
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
            indicators["rsi"] = {"error": str(e)}
        
        try:
            indicators["macd"] = self.enhanced_macd(close, volume)
        except Exception as e:
            indicators["macd"] = {"error": str(e)}
        
        try:
            indicators["stochastic"] = self.enhanced_stochastic(high, low, close)
        except Exception as e:
            indicators["stochastic"] = {"error": str(e)}
        
        try:
            indicators["williams_r"] = self.enhanced_williams_r(high, low, close)
        except Exception as e:
            indicators["williams_r"] = {"error": str(e)}
        
        try:
            indicators["cci"] = self.enhanced_cci(high, low, close)
        except Exception as e:
            indicators["cci"] = {"error": str(e)}
        
        try:
            indicators["adx"] = self.enhanced_adx(high, low, close)
        except Exception as e:
            indicators["adx"] = {"error": str(e)}
        
        try:
            indicators["bollinger_bands"] = self.enhanced_bollinger_bands(close)
        except Exception as e:
            indicators["bollinger_bands"] = {"error": str(e)}
        
        try:
            indicators["parabolic_sar"] = self.enhanced_parabolic_sar(high, low)
        except Exception as e:
            indicators["parabolic_sar"] = {"error": str(e)}
        
        try:
            indicators["ichimoku"] = self.enhanced_ichimoku(high, low, close)
        except Exception as e:
            indicators["ichimoku"] = {"error": str(e)}
        
        try:
            indicators["atr"] = self.enhanced_atr(high, low, close)
        except Exception as e:
            indicators["atr"] = {"error": str(e)}
        
        try:
            indicators["obv"] = self.enhanced_obv(close, volume)
        except Exception as e:
            indicators["obv"] = {"error": str(e)}
        
        try:
            indicators["mfi"] = self.enhanced_mfi(high, low, close, volume)
        except Exception as e:
            indicators["mfi"] = {"error": str(e)}
        
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
    indicators = EnhancedTechnicalIndicators("EURUSD")
    
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

