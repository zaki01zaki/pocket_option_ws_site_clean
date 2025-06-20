import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
from simplified_indicators import SimplifiedTechnicalIndicators
from single_pair_analyzer import SinglePairAnalyzer
import logging

@dataclass
class StabilityConfig:
    """
    إعدادات نظام تقليل التذبذب والاستقرار
    """
    noise_threshold: float = 0.1
    signal_persistence_periods: int = 3
    confirmation_threshold: float = 0.7
    volatility_adjustment_factor: float = 0.5
    trend_consistency_window: int = 10
    outlier_detection_threshold: float = 2.0

class SignalStabilizer:
    """
    نظام تقليل التذبذب وتحسين استقرار الإشارات
    """
    
    def __init__(self, pair_name: str = "EURUSD"):
        self.pair_name = pair_name
        self.config = StabilityConfig()
        self.signal_history = []
        self.confidence_history = []
        self.volatility_history = []
        self.trend_history = []
        
        # إعداد نظام التسجيل
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"SignalStabilizer_{pair_name}")
    
    def add_signal_data(self, signal_type: str, confidence: float, 
                       volatility: float, trend_strength: float, timestamp: datetime = None):
        """
        إضافة بيانات إشارة جديدة للتحليل
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        signal_data = {
            'timestamp': timestamp,
            'signal_type': signal_type,
            'confidence': confidence,
            'volatility': volatility,
            'trend_strength': trend_strength
        }
        
        self.signal_history.append(signal_data)
        self.confidence_history.append(confidence)
        self.volatility_history.append(volatility)
        self.trend_history.append(trend_strength)
        
        # الاحتفاظ بآخر 100 إشارة فقط
        if len(self.signal_history) > 100:
            self.signal_history = self.signal_history[-100:]
            self.confidence_history = self.confidence_history[-100:]
            self.volatility_history = self.volatility_history[-100:]
            self.trend_history = self.trend_history[-100:]
    
    def detect_signal_outliers(self, recent_signals: List[Dict]) -> List[bool]:
        """
        كشف الإشارات الشاذة
        """
        if len(recent_signals) < 5:
            return [False] * len(recent_signals)
        
        confidences = [s['confidence'] for s in recent_signals]
        mean_confidence = np.mean(confidences)
        std_confidence = np.std(confidences)
        
        outliers = []
        for confidence in confidences:
            z_score = abs(confidence - mean_confidence) / (std_confidence + 1e-8)
            is_outlier = z_score > self.config.outlier_detection_threshold
            outliers.append(is_outlier)
        
        return outliers
    
    def calculate_signal_persistence(self, signal_type: str, window: int = None) -> float:
        """
        حساب استمرارية الإشارة
        """
        if window is None:
            window = self.config.signal_persistence_periods
        
        if len(self.signal_history) < window:
            return 0.0
        
        recent_signals = self.signal_history[-window:]
        same_type_count = sum(1 for s in recent_signals if s['signal_type'] == signal_type)
        
        return same_type_count / window
    
    def calculate_volatility_adjustment(self, current_volatility: float) -> float:
        """
        حساب تعديل التقلبات
        """
        if len(self.volatility_history) < 10:
            return 1.0
        
        avg_volatility = np.mean(self.volatility_history[-20:])
        volatility_ratio = current_volatility / (avg_volatility + 1e-8)
        
        # تقليل قوة الإشارة في حالة التقلبات العالية
        if volatility_ratio > 1.5:
            adjustment = 1.0 - (volatility_ratio - 1.0) * self.config.volatility_adjustment_factor
            return max(0.3, adjustment)
        elif volatility_ratio < 0.5:
            adjustment = 1.0 + (1.0 - volatility_ratio) * self.config.volatility_adjustment_factor
            return min(1.5, adjustment)
        
        return 1.0
    
    def calculate_trend_consistency(self, current_trend: str) -> float:
        """
        حساب اتساق الاتجاه
        """
        window = self.config.trend_consistency_window
        
        if len(self.signal_history) < window:
            return 0.5
        
        recent_signals = self.signal_history[-window:]
        
        # تحويل أنواع الإشارات إلى اتجاهات
        trend_mapping = {'buy': 'bullish', 'sell': 'bearish', 'neutral': 'neutral'}
        recent_trends = [trend_mapping.get(s['signal_type'], 'neutral') for s in recent_signals]
        
        # حساب اتساق الاتجاه
        if current_trend == 'neutral':
            return 0.5
        
        consistent_count = sum(1 for trend in recent_trends if trend == current_trend)
        consistency = consistent_count / window
        
        return consistency
    
    def apply_noise_filter(self, signal_strength: float, confidence: float) -> Tuple[float, float]:
        """
        تطبيق مرشح الضوضاء
        """
        # تطبيق عتبة الضوضاء
        if signal_strength < self.config.noise_threshold:
            return 0.0, 0.0
        
        # تطبيق تمهيد على قوة الإشارة
        if len(self.confidence_history) >= 3:
            recent_confidences = self.confidence_history[-3:]
            smoothed_confidence = np.mean(recent_confidences + [confidence])
        else:
            smoothed_confidence = confidence
        
        # تطبيق تمهيد على قوة الإشارة
        smoothed_strength = signal_strength * 0.7 + (signal_strength * 0.3)
        
        return smoothed_strength, smoothed_confidence
    
    def calculate_confirmation_score(self, signal_data: Dict) -> float:
        """
        حساب نقاط التأكيد للإشارة
        """
        signal_type = signal_data['signal_type']
        confidence = signal_data['confidence']
        volatility = signal_data['volatility']
        trend_strength = signal_data['trend_strength']
        
        # حساب استمرارية الإشارة
        persistence = self.calculate_signal_persistence(signal_type)
        
        # حساب تعديل التقلبات
        volatility_adjustment = self.calculate_volatility_adjustment(volatility)
        
        # حساب اتساق الاتجاه
        trend_mapping = {'buy': 'bullish', 'sell': 'bearish', 'neutral': 'neutral'}
        current_trend = trend_mapping.get(signal_type, 'neutral')
        trend_consistency = self.calculate_trend_consistency(current_trend)
        
        # حساب النقاط النهائية
        confirmation_score = (
            confidence * 0.4 +
            persistence * 100 * 0.3 +
            trend_consistency * 100 * 0.2 +
            trend_strength * 0.1
        ) * volatility_adjustment
        
        return min(100, max(0, confirmation_score))
    
    def stabilize_signal(self, signal_data: Dict) -> Dict:
        """
        تحسين استقرار الإشارة
        """
        # إضافة البيانات إلى التاريخ
        self.add_signal_data(
            signal_data['signal_type'],
            signal_data['confidence'],
            signal_data.get('volatility', 0.5),
            signal_data.get('trend_strength', 50)
        )
        
        # تطبيق مرشح الضوضاء
        original_strength = signal_data.get('signal_strength', signal_data['confidence'])
        filtered_strength, filtered_confidence = self.apply_noise_filter(
            original_strength, signal_data['confidence']
        )
        
        # حساب نقاط التأكيد
        confirmation_score = self.calculate_confirmation_score(signal_data)
        
        # كشف الإشارات الشاذة
        recent_signals = self.signal_history[-5:] if len(self.signal_history) >= 5 else self.signal_history
        outliers = self.detect_signal_outliers(recent_signals)
        is_current_outlier = outliers[-1] if outliers else False
        
        # تحديد حالة الإشارة النهائية
        final_signal_type = signal_data['signal_type']
        final_confidence = filtered_confidence
        final_strength = filtered_strength
        
        # إلغاء الإشارة إذا كانت شاذة أو ضعيفة التأكيد
        if is_current_outlier or confirmation_score < self.config.confirmation_threshold * 100:
            final_signal_type = 'neutral'
            final_confidence = 0
            final_strength = 0
        
        # إنشاء الإشارة المحسنة
        stabilized_signal = {
            'signal_type': final_signal_type,
            'confidence': final_confidence,
            'signal_strength': final_strength,
            'confirmation_score': confirmation_score,
            'is_outlier': is_current_outlier,
            'persistence': self.calculate_signal_persistence(signal_data['signal_type']),
            'volatility_adjustment': self.calculate_volatility_adjustment(signal_data.get('volatility', 0.5)),
            'trend_consistency': self.calculate_trend_consistency(
                {'buy': 'bullish', 'sell': 'bearish', 'neutral': 'neutral'}.get(signal_data['signal_type'], 'neutral')
            ),
            'stability_metrics': {
                'original_confidence': signal_data['confidence'],
                'filtered_confidence': filtered_confidence,
                'original_strength': original_strength,
                'filtered_strength': filtered_strength,
                'noise_filtered': abs(original_strength - filtered_strength) > 0.01
            }
        }
        
        return stabilized_signal
    
    def get_stability_report(self) -> Dict:
        """
        الحصول على تقرير الاستقرار
        """
        if len(self.signal_history) < 10:
            return {
                "status": "insufficient_data",
                "message": "بيانات غير كافية لتقرير الاستقرار"
            }
        
        # حساب إحصائيات الاستقرار
        recent_signals = self.signal_history[-20:]
        
        # تنوع الإشارات
        signal_types = [s['signal_type'] for s in recent_signals]
        buy_count = signal_types.count('buy')
        sell_count = signal_types.count('sell')
        neutral_count = signal_types.count('neutral')
        
        # استقرار الثقة
        confidences = [s['confidence'] for s in recent_signals]
        confidence_stability = 100 - (np.std(confidences) / (np.mean(confidences) + 1e-8) * 100)
        confidence_stability = max(0, min(100, confidence_stability))
        
        # استقرار التقلبات
        volatilities = self.volatility_history[-20:] if len(self.volatility_history) >= 20 else self.volatility_history
        volatility_stability = 100 - (np.std(volatilities) / (np.mean(volatilities) + 1e-8) * 100)
        volatility_stability = max(0, min(100, volatility_stability))
        
        # اتساق الاتجاه
        trend_changes = 0
        for i in range(1, len(recent_signals)):
            if recent_signals[i]['signal_type'] != recent_signals[i-1]['signal_type']:
                trend_changes += 1
        
        trend_consistency = max(0, 100 - (trend_changes / len(recent_signals) * 100))
        
        # النقاط الإجمالية للاستقرار
        overall_stability = (confidence_stability * 0.4 + volatility_stability * 0.3 + trend_consistency * 0.3)
        
        return {
            "status": "success",
            "overall_stability": overall_stability,
            "signal_distribution": {
                "buy_signals": buy_count,
                "sell_signals": sell_count,
                "neutral_signals": neutral_count,
                "total_signals": len(recent_signals)
            },
            "stability_metrics": {
                "confidence_stability": confidence_stability,
                "volatility_stability": volatility_stability,
                "trend_consistency": trend_consistency
            },
            "recommendations": self._generate_stability_recommendations(overall_stability, confidence_stability, trend_consistency)
        }
    
    def _generate_stability_recommendations(self, overall_stability: float, 
                                          confidence_stability: float, trend_consistency: float) -> List[str]:
        """
        توليد توصيات تحسين الاستقرار
        """
        recommendations = []
        
        if overall_stability < 60:
            recommendations.append("النظام يحتاج إلى تحسين عام في الاستقرار")
        
        if confidence_stability < 50:
            recommendations.append("يُنصح بزيادة عتبة الثقة لتقليل التذبذب")
        
        if trend_consistency < 40:
            recommendations.append("يُنصح بزيادة فترة تأكيد الاتجاه")
        
        if overall_stability > 80:
            recommendations.append("النظام يعمل بشكل مستقر وموثوق")
        
        if not recommendations:
            recommendations.append("النظام يعمل بشكل مقبول مع إمكانية تحسينات طفيفة")
        
        return recommendations

class EnhancedSignalProcessor:
    """
    معالج الإشارات المحسن مع تقليل التذبذب
    """
    
    def __init__(self, pair_name: str = "EURUSD"):
        self.pair_name = pair_name
        self.analyzer = SinglePairAnalyzer(pair_name)
        self.stabilizer = SignalStabilizer(pair_name)
        self.indicators = SimplifiedTechnicalIndicators(pair_name)
        
        # إعدادات المعالجة
        self.min_confirmation_signals = 3
        self.signal_timeout_minutes = 15
        self.max_signals_per_session = 5
        
        # تتبع الإشارات النشطة
        self.active_signals = []
        self.session_signal_count = 0
        self.last_session_reset = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    def reset_session_if_needed(self):
        """
        إعادة تعيين عداد الجلسة إذا لزم الأمر
        """
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if current_date > self.last_session_reset:
            self.session_signal_count = 0
            self.last_session_reset = current_date
    
    def process_market_data(self, high: np.ndarray, low: np.ndarray, 
                           close: np.ndarray, volume: np.ndarray = None) -> Dict:
        """
        معالجة بيانات السوق وتوليد إشارات محسنة
        """
        self.reset_session_if_needed()
        
        # الحصول على التحليل الشامل
        analysis = self.analyzer.comprehensive_analysis()
        
        if "error" in analysis:
            return analysis
        
        # استخراج بيانات الإشارة الأولية
        indicators = analysis['indicators']
        trend_analysis = analysis['trend_analysis']
        volatility_analysis = analysis['volatility_analysis']
        session_analysis = analysis['session_analysis']
        
        # جمع إشارات المؤشرات
        signal_votes = {'buy': 0, 'sell': 0, 'neutral': 0}
        total_strength = 0
        indicator_count = 0
        
        for indicator_name, indicator_data in indicators.items():
            if 'signal_type' in indicator_data and 'signal_strength' in indicator_data:
                signal_type = indicator_data['signal_type']
                signal_strength = indicator_data['signal_strength']
                
                signal_votes[signal_type] += 1
                total_strength += signal_strength
                indicator_count += 1
        
        # تحديد الإشارة الأولية
        if signal_votes['buy'] > signal_votes['sell'] and signal_votes['buy'] >= self.min_confirmation_signals:
            primary_signal = 'buy'
            primary_confidence = (signal_votes['buy'] / indicator_count) * 100
        elif signal_votes['sell'] > signal_votes['buy'] and signal_votes['sell'] >= self.min_confirmation_signals:
            primary_signal = 'sell'
            primary_confidence = (signal_votes['sell'] / indicator_count) * 100
        else:
            primary_signal = 'neutral'
            primary_confidence = 50
        
        # إعداد بيانات الإشارة للتحسين
        signal_data = {
            'signal_type': primary_signal,
            'confidence': primary_confidence,
            'signal_strength': total_strength / indicator_count if indicator_count > 0 else 0,
            'volatility': volatility_analysis.get('current_volatility', 0.5),
            'trend_strength': trend_analysis.get('trend_confidence', 50)
        }
        
        # تطبيق تحسين الاستقرار
        stabilized_signal = self.stabilizer.stabilize_signal(signal_data)
        
        # فحص قيود الجلسة
        if self.session_signal_count >= self.max_signals_per_session:
            stabilized_signal['signal_type'] = 'neutral'
            stabilized_signal['confidence'] = 0
            stabilized_signal['reason'] = 'session_limit_reached'
        
        # فحص قوة الجلسة
        if session_analysis['strength'] < 0.6:
            stabilized_signal['confidence'] *= session_analysis['strength']
            if stabilized_signal['confidence'] < 30:
                stabilized_signal['signal_type'] = 'neutral'
                stabilized_signal['reason'] = 'weak_session'
        
        # تحديث عداد الإشارات
        if stabilized_signal['signal_type'] != 'neutral':
            self.session_signal_count += 1
        
        # إنشاء التقرير النهائي
        enhanced_signal = {
            'pair_name': self.pair_name,
            'timestamp': datetime.now().isoformat(),
            'signal': stabilized_signal,
            'analysis_summary': {
                'overall_score': analysis['overall_score'],
                'trend_direction': trend_analysis['overall_trend'],
                'volatility_level': volatility_analysis['volatility_level'],
                'session_strength': session_analysis['strength'],
                'indicator_votes': signal_votes,
                'total_indicators': indicator_count
            },
            'stability_report': self.stabilizer.get_stability_report(),
            'session_info': {
                'signals_today': self.session_signal_count,
                'max_signals': self.max_signals_per_session,
                'session_active': session_analysis['recommended_trading']
            }
        }
        
        return enhanced_signal
    
    def get_system_status(self) -> Dict:
        """
        الحصول على حالة النظام
        """
        stability_report = self.stabilizer.get_stability_report()
        
        return {
            'pair_name': self.pair_name,
            'system_status': 'active',
            'stability_score': stability_report.get('overall_stability', 0),
            'session_signals': self.session_signal_count,
            'max_session_signals': self.max_signals_per_session,
            'last_update': datetime.now().isoformat(),
            'recommendations': stability_report.get('recommendations', [])
        }

# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء معالج الإشارات المحسن
    processor = EnhancedSignalProcessor("EURUSD")
    
    # توليد بيانات عينة
    np.random.seed(42)
    n_points = 50
    
    base_price = 1.0850
    price_changes = np.random.normal(0, 0.0008, n_points)
    closes = base_price + np.cumsum(price_changes)
    
    highs = closes + np.random.uniform(0, 0.0005, n_points)
    lows = closes - np.random.uniform(0, 0.0005, n_points)
    volumes = np.random.normal(1000, 200, n_points)
    
    # معالجة البيانات
    result = processor.process_market_data(highs, lows, closes, volumes)
    
    # طباعة النتائج
    print("=== تقرير الإشارة المحسنة ===")
    print(f"الزوج: {result['pair_name']}")
    print(f"نوع الإشارة: {result['signal']['signal_type']}")
    print(f"مستوى الثقة: {result['signal']['confidence']:.2f}%")
    print(f"نقاط التأكيد: {result['signal']['confirmation_score']:.2f}")
    print(f"النقاط الإجمالية: {result['analysis_summary']['overall_score']:.2f}")
    
    print("\n=== تقرير الاستقرار ===")
    stability = result['stability_report']
    if stability['status'] == 'success':
        print(f"استقرار النظام: {stability['overall_stability']:.2f}%")
        print(f"استقرار الثقة: {stability['stability_metrics']['confidence_stability']:.2f}%")
        print(f"اتساق الاتجاه: {stability['stability_metrics']['trend_consistency']:.2f}%")
        print("التوصيات:")
        for rec in stability['recommendations']:
            print(f"  - {rec}")
    
    print("\n=== حالة النظام ===")
    status = processor.get_system_status()
    print(f"حالة النظام: {status['system_status']}")
    print(f"نقاط الاستقرار: {status['stability_score']:.2f}")
    print(f"إشارات الجلسة: {status['session_signals']}/{status['max_session_signals']}")

