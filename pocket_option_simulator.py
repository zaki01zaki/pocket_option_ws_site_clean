import numpy as np
import pandas as pd
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class PocketOptionSimulator:
    """
    محاكي متقدم لأسعار Pocket Option بناءً على أنماط السوق الحقيقية
    """
    
    def __init__(self):
        self.db_path = 'pocket_option_simulation.db'
        self.model_path = 'pocket_option_model.pkl'
        self.scaler_path = 'pocket_option_scaler.pkl'
        
        self.setup_database()
        self.setup_logging()
        
        # معاملات المحاكاة
        self.simulation_params = {
            'base_spread': 0.0002,  # السبريد الأساسي
            'volatility_factor': 1.2,  # عامل التقلب
            'trend_strength': 0.3,  # قوة الاتجاه
            'noise_level': 0.1,  # مستوى الضوضاء
            'otc_premium': 0.0005,  # علاوة OTC
            'market_hours_factor': 0.8,  # عامل ساعات السوق
        }
        
        # أنماط الأصول المختلفة
        self.asset_patterns = {
            'EURUSD': {
                'volatility': 0.0008,
                'trend_persistence': 0.6,
                'mean_reversion': 0.4,
                'session_bias': {'asian': -0.1, 'london': 0.2, 'ny': 0.1}
            },
            'GBPUSD': {
                'volatility': 0.0012,
                'trend_persistence': 0.5,
                'mean_reversion': 0.5,
                'session_bias': {'asian': 0.0, 'london': 0.3, 'ny': 0.0}
            },
            'USDJPY': {
                'volatility': 0.0010,
                'trend_persistence': 0.7,
                'mean_reversion': 0.3,
                'session_bias': {'asian': 0.2, 'london': 0.0, 'ny': -0.1}
            },
            'BTCUSD': {
                'volatility': 0.0200,
                'trend_persistence': 0.4,
                'mean_reversion': 0.6,
                'session_bias': {'asian': 0.1, 'london': 0.1, 'ny': 0.1}
            },
            'ETHUSD': {
                'volatility': 0.0250,
                'trend_persistence': 0.3,
                'mean_reversion': 0.7,
                'session_bias': {'asian': 0.0, 'london': 0.2, 'ny': 0.0}
            }
        }
        
        # تحميل النماذج المدربة إذا كانت موجودة
        self.load_models()
    
    def setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('pocket_option_simulator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """إعداد قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول البيانات المحاكاة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulated_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                asset_name TEXT NOT NULL,
                real_price REAL NOT NULL,
                simulated_price REAL NOT NULL,
                spread REAL,
                volatility REAL,
                trend_factor REAL,
                noise_factor REAL,
                is_otc BOOLEAN DEFAULT 0,
                session_type TEXT,
                quality_score REAL
            )
        ''')
        
        # جدول أنماط التداول
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                asset_name TEXT NOT NULL,
                pattern_type TEXT,
                pattern_strength REAL,
                duration_minutes INTEGER,
                success_rate REAL
            )
        ''')
        
        # جدول إحصائيات الأداء
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulation_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                asset_name TEXT NOT NULL,
                accuracy_score REAL,
                mean_error REAL,
                std_error REAL,
                correlation REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_market_session(self, timestamp: datetime) -> str:
        """تحديد جلسة السوق الحالية"""
        hour = timestamp.hour
        
        if 0 <= hour < 8:
            return 'asian'
        elif 8 <= hour < 16:
            return 'london'
        else:
            return 'ny'
    
    def calculate_volatility(self, asset_name: str, historical_prices: List[float]) -> float:
        """حساب التقلب بناءً على البيانات التاريخية"""
        if len(historical_prices) < 2:
            return self.asset_patterns.get(asset_name, {}).get('volatility', 0.001)
        
        # حساب العوائد
        returns = []
        for i in range(1, len(historical_prices)):
            ret = (historical_prices[i] - historical_prices[i-1]) / historical_prices[i-1]
            returns.append(ret)
        
        # حساب الانحراف المعياري
        volatility = np.std(returns) if returns else 0.001
        
        # تطبيق عامل التقلب
        return volatility * self.simulation_params['volatility_factor']
    
    def detect_trend(self, historical_prices: List[float], window: int = 20) -> Tuple[float, str]:
        """كشف الاتجاه وقوته"""
        if len(historical_prices) < window:
            return 0.0, 'sideways'
        
        recent_prices = historical_prices[-window:]
        
        # حساب المتوسط المتحرك البسيط
        sma_short = np.mean(recent_prices[-5:])
        sma_long = np.mean(recent_prices[-15:])
        
        # حساب قوة الاتجاه
        trend_strength = (sma_short - sma_long) / sma_long
        
        # تحديد نوع الاتجاه
        if trend_strength > 0.001:
            trend_type = 'uptrend'
        elif trend_strength < -0.001:
            trend_type = 'downtrend'
        else:
            trend_type = 'sideways'
        
        return trend_strength, trend_type
    
    def apply_pocket_option_adjustments(self, real_price: float, asset_name: str, 
                                      timestamp: datetime, is_otc: bool = False) -> Dict:
        """تطبيق تعديلات Pocket Option على السعر الحقيقي"""
        
        # الحصول على أنماط الأصل
        asset_pattern = self.asset_patterns.get(asset_name, self.asset_patterns['EURUSD'])
        
        # تحديد جلسة السوق
        session = self.get_market_session(timestamp)
        session_bias = asset_pattern['session_bias'].get(session, 0.0)
        
        # حساب السبريد
        base_spread = self.simulation_params['base_spread']
        if is_otc:
            base_spread += self.simulation_params['otc_premium']
        
        # تطبيق عامل ساعات السوق
        if session == 'asian' and asset_name.startswith('EUR'):
            base_spread *= 1.5  # سبريد أعلى خارج ساعات العمل الرئيسية
        
        # حساب التقلب
        volatility = asset_pattern['volatility']
        
        # إضافة ضوضاء عشوائية
        noise = np.random.normal(0, volatility * self.simulation_params['noise_level'])
        
        # تطبيق انحياز الجلسة
        session_adjustment = real_price * session_bias * 0.001
        
        # حساب السعر المحاكى
        simulated_price = real_price + session_adjustment + noise
        
        # تطبيق السبريد
        bid_price = simulated_price - (base_spread / 2)
        ask_price = simulated_price + (base_spread / 2)
        
        # حساب نقاط الجودة
        quality_score = self.calculate_quality_score(asset_name, session, is_otc)
        
        return {
            'real_price': real_price,
            'simulated_price': simulated_price,
            'bid_price': bid_price,
            'ask_price': ask_price,
            'spread': base_spread,
            'volatility': volatility,
            'session_bias': session_bias,
            'noise': noise,
            'quality_score': quality_score,
            'session': session,
            'is_otc': is_otc
        }
    
    def calculate_quality_score(self, asset_name: str, session: str, is_otc: bool) -> float:
        """حساب نقاط الجودة للأصل"""
        base_quality = 85.0
        
        # تعديل بناءً على الأصل
        if asset_name in ['EURUSD', 'GBPUSD', 'USDJPY']:
            base_quality += 5.0
        elif asset_name.startswith('BTC') or asset_name.startswith('ETH'):
            base_quality -= 10.0
        
        # تعديل بناءً على الجلسة
        if session == 'london':
            base_quality += 3.0
        elif session == 'asian':
            base_quality -= 2.0
        
        # تعديل OTC
        if is_otc:
            base_quality -= 5.0
        
        # إضافة تقلب عشوائي
        random_factor = np.random.normal(0, 2.0)
        
        final_quality = max(60.0, min(95.0, base_quality + random_factor))
        return round(final_quality, 1)
    
    def generate_market_patterns(self, asset_name: str, duration_hours: int = 24) -> List[Dict]:
        """توليد أنماط السوق لفترة محددة"""
        patterns = []
        current_time = datetime.now()
        
        # أنماط مختلفة للتداول
        pattern_types = [
            {'name': 'trend_following', 'probability': 0.3, 'duration': 60},
            {'name': 'mean_reversion', 'probability': 0.25, 'duration': 30},
            {'name': 'breakout', 'probability': 0.2, 'duration': 45},
            {'name': 'consolidation', 'probability': 0.15, 'duration': 90},
            {'name': 'news_spike', 'probability': 0.1, 'duration': 15}
        ]
        
        for hour in range(duration_hours):
            timestamp = current_time + timedelta(hours=hour)
            
            # اختيار نمط عشوائي
            pattern = np.random.choice(
                pattern_types, 
                p=[p['probability'] for p in pattern_types]
            )
            
            # حساب قوة النمط
            strength = np.random.uniform(0.3, 0.9)
            
            # حساب معدل النجاح المتوقع
            success_rate = self.calculate_pattern_success_rate(
                pattern['name'], asset_name, timestamp
            )
            
            patterns.append({
                'timestamp': timestamp,
                'asset_name': asset_name,
                'pattern_type': pattern['name'],
                'pattern_strength': strength,
                'duration_minutes': pattern['duration'],
                'success_rate': success_rate
            })
        
        return patterns
    
    def calculate_pattern_success_rate(self, pattern_type: str, asset_name: str, 
                                     timestamp: datetime) -> float:
        """حساب معدل نجاح النمط"""
        base_rates = {
            'trend_following': 0.65,
            'mean_reversion': 0.60,
            'breakout': 0.55,
            'consolidation': 0.70,
            'news_spike': 0.45
        }
        
        base_rate = base_rates.get(pattern_type, 0.50)
        
        # تعديل بناءً على الأصل
        asset_pattern = self.asset_patterns.get(asset_name, {})
        
        if pattern_type == 'trend_following':
            base_rate += asset_pattern.get('trend_persistence', 0.5) * 0.2
        elif pattern_type == 'mean_reversion':
            base_rate += asset_pattern.get('mean_reversion', 0.5) * 0.2
        
        # تعديل بناءً على الوقت
        session = self.get_market_session(timestamp)
        if session == 'london':
            base_rate += 0.05
        elif session == 'asian':
            base_rate -= 0.03
        
        # إضافة تقلب عشوائي
        random_factor = np.random.normal(0, 0.05)
        
        final_rate = max(0.3, min(0.9, base_rate + random_factor))
        return round(final_rate, 2)
    
    def train_ml_model(self, historical_data: pd.DataFrame):
        """تدريب نموذج التعلم الآلي"""
        try:
            # إعداد الميزات
            features = []
            targets = []
            
            for _, row in historical_data.iterrows():
                # الميزات: السعر الحقيقي، التقلب، الجلسة، etc.
                feature_vector = [
                    row['real_price'],
                    row['volatility'],
                    1 if row['session_type'] == 'london' else 0,
                    1 if row['session_type'] == 'ny' else 0,
                    1 if row['is_otc'] else 0,
                    row['trend_factor'],
                    row['noise_factor']
                ]
                
                features.append(feature_vector)
                targets.append(row['simulated_price'])
            
            X = np.array(features)
            y = np.array(targets)
            
            # تقسيم البيانات
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # تطبيع البيانات
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # تدريب النموذج
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            model.fit(X_train_scaled, y_train)
            
            # تقييم النموذج
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            self.logger.info(f"نتائج التدريب - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
            
            # حفظ النموذج والمقياس
            joblib.dump(model, self.model_path)
            joblib.dump(scaler, self.scaler_path)
            
            self.model = model
            self.scaler = scaler
            
            return True
        
        except Exception as e:
            self.logger.error(f"خطأ في تدريب النموذج: {e}")
            return False
    
    def load_models(self):
        """تحميل النماذج المدربة"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.logger.info("تم تحميل النماذج المدربة بنجاح")
            else:
                self.model = None
                self.scaler = None
                self.logger.info("لم يتم العثور على نماذج مدربة")
        
        except Exception as e:
            self.logger.error(f"خطأ في تحميل النماذج: {e}")
            self.model = None
            self.scaler = None
    
    def predict_with_ml(self, real_price: float, asset_name: str, 
                       timestamp: datetime, is_otc: bool = False) -> Optional[float]:
        """التنبؤ باستخدام نموذج التعلم الآلي"""
        if not self.model or not self.scaler:
            return None
        
        try:
            # إعداد الميزات
            session = self.get_market_session(timestamp)
            asset_pattern = self.asset_patterns.get(asset_name, {})
            
            feature_vector = [
                real_price,
                asset_pattern.get('volatility', 0.001),
                1 if session == 'london' else 0,
                1 if session == 'ny' else 0,
                1 if is_otc else 0,
                0.0,  # trend_factor - سيتم حسابه لاحقاً
                0.0   # noise_factor - سيتم حسابه لاحقاً
            ]
            
            # تطبيع البيانات
            feature_vector_scaled = self.scaler.transform([feature_vector])
            
            # التنبؤ
            predicted_price = self.model.predict(feature_vector_scaled)[0]
            
            return predicted_price
        
        except Exception as e:
            self.logger.error(f"خطأ في التنبؤ: {e}")
            return None
    
    def simulate_price(self, real_price: float, asset_name: str, 
                      timestamp: datetime = None, is_otc: bool = False) -> Dict:
        """محاكاة سعر Pocket Option"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # محاولة استخدام نموذج التعلم الآلي أولاً
        ml_prediction = self.predict_with_ml(real_price, asset_name, timestamp, is_otc)
        
        if ml_prediction:
            # استخدام التنبؤ من النموذج
            result = self.apply_pocket_option_adjustments(
                ml_prediction, asset_name, timestamp, is_otc
            )
            result['prediction_method'] = 'machine_learning'
        else:
            # استخدام المحاكاة التقليدية
            result = self.apply_pocket_option_adjustments(
                real_price, asset_name, timestamp, is_otc
            )
            result['prediction_method'] = 'traditional'
        
        # حفظ النتيجة في قاعدة البيانات
        self.save_simulation_result(result, asset_name, timestamp)
        
        return result
    
    def save_simulation_result(self, result: Dict, asset_name: str, timestamp: datetime):
        """حفظ نتيجة المحاكاة في قاعدة البيانات"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO simulated_prices 
                (asset_name, real_price, simulated_price, spread, volatility, 
                 trend_factor, noise_factor, is_otc, session_type, quality_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                asset_name,
                result['real_price'],
                result['simulated_price'],
                result['spread'],
                result['volatility'],
                result.get('trend_factor', 0),
                result['noise'],
                result['is_otc'],
                result['session'],
                result['quality_score']
            ))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            self.logger.error(f"خطأ في حفظ نتيجة المحاكاة: {e}")
    
    def get_simulation_accuracy(self, asset_name: str, days: int = 7) -> Dict:
        """حساب دقة المحاكاة"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT real_price, simulated_price
                FROM simulated_prices
                WHERE asset_name = ?
                AND datetime(timestamp) > datetime('now', '-{} days')
            '''.format(days), (asset_name,))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return {'accuracy': 0, 'mean_error': 0, 'std_error': 0}
            
            real_prices = [r[0] for r in results]
            simulated_prices = [r[1] for r in results]
            
            # حساب الأخطاء
            errors = [abs(r - s) / r for r, s in zip(real_prices, simulated_prices)]
            
            accuracy = 1 - np.mean(errors)
            mean_error = np.mean(errors)
            std_error = np.std(errors)
            correlation = np.corrcoef(real_prices, simulated_prices)[0, 1]
            
            return {
                'accuracy': round(accuracy, 3),
                'mean_error': round(mean_error, 4),
                'std_error': round(std_error, 4),
                'correlation': round(correlation, 3),
                'sample_size': len(results)
            }
        
        except Exception as e:
            self.logger.error(f"خطأ في حساب دقة المحاكاة: {e}")
            return {'accuracy': 0, 'mean_error': 0, 'std_error': 0}
    
    def optimize_parameters(self, asset_name: str):
        """تحسين معاملات المحاكاة للأصل"""
        try:
            # جلب البيانات التاريخية
            conn = sqlite3.connect(self.db_path)
            historical_data = pd.read_sql_query('''
                SELECT * FROM simulated_prices
                WHERE asset_name = ?
                ORDER BY timestamp DESC
                LIMIT 1000
            ''', conn, params=(asset_name,))
            conn.close()
            
            if len(historical_data) < 100:
                self.logger.warning(f"بيانات غير كافية لتحسين معاملات {asset_name}")
                return False
            
            # تدريب نموذج جديد
            success = self.train_ml_model(historical_data)
            
            if success:
                self.logger.info(f"تم تحسين معاملات {asset_name} بنجاح")
                return True
            else:
                return False
        
        except Exception as e:
            self.logger.error(f"خطأ في تحسين المعاملات: {e}")
            return False

# مثال على الاستخدام
if __name__ == "__main__":
    simulator = PocketOptionSimulator()
    
    # محاكاة أسعار مختلفة
    assets = ['EURUSD', 'GBPUSD', 'BTCUSD']
    real_prices = [1.0850, 1.2650, 45000.0]
    
    for asset, price in zip(assets, real_prices):
        result = simulator.simulate_price(price, asset)
        print(f"{asset}: Real={price}, Simulated={result['simulated_price']:.4f}, Quality={result['quality_score']}%")
    
    # حساب دقة المحاكاة
    for asset in assets:
        accuracy = simulator.get_simulation_accuracy(asset)
        print(f"دقة محاكاة {asset}: {accuracy}")

