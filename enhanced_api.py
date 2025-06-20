from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
sys.path.append('/home/ubuntu/pocket_option_trading_platform/backend/src/services')

from signal_stabilizer import EnhancedSignalProcessor
from single_pair_analyzer import SinglePairAnalyzer
from simplified_indicators import SimplifiedTechnicalIndicators
import numpy as np
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# إنشاء معالجات للأزواج المختلفة
processors = {
    'EURUSD': EnhancedSignalProcessor('EURUSD'),
    'GBPUSD': EnhancedSignalProcessor('GBPUSD'),
    'USDJPY': EnhancedSignalProcessor('USDJPY')
}

current_pair = 'EURUSD'
current_processor = processors[current_pair]

@app.route('/api/pairs', methods=['GET'])
def get_available_pairs():
    """الحصول على الأزواج المتاحة"""
    return jsonify({
        'pairs': list(processors.keys()),
        'current_pair': current_pair
    })

@app.route('/api/pair/select', methods=['POST'])
def select_pair():
    """اختيار زوج للتحليل"""
    global current_pair, current_processor
    
    data = request.get_json()
    pair = data.get('pair', 'EURUSD')
    
    if pair in processors:
        current_pair = pair
        current_processor = processors[pair]
        return jsonify({
            'success': True,
            'selected_pair': current_pair,
            'message': f'تم اختيار الزوج {pair} بنجاح'
        })
    else:
        return jsonify({
            'success': False,
            'error': f'الزوج {pair} غير متاح'
        }), 400

@app.route('/api/analysis/comprehensive', methods=['GET'])
def get_comprehensive_analysis():
    """الحصول على التحليل الشامل للزوج المختار"""
    try:
        # توليد بيانات عينة للاختبار
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        n_points = 100
        
        # أسعار أساسية حسب الزوج
        base_prices = {
            "EURUSD": 1.0850,
            "GBPUSD": 1.2650,
            "USDJPY": 149.50
        }
        
        base_price = base_prices.get(current_pair, 1.0850)
        volatility = 0.0008 if current_pair == 'EURUSD' else 0.0012 if current_pair == 'GBPUSD' else 0.0006
        
        price_changes = np.random.normal(0, volatility, n_points)
        closes = base_price + np.cumsum(price_changes)
        
        highs = closes + np.random.uniform(0, volatility * 0.5, n_points)
        lows = closes - np.random.uniform(0, volatility * 0.5, n_points)
        volumes = np.random.normal(1000, 200, n_points)
        
        # معالجة البيانات
        result = current_processor.process_market_data(highs, lows, closes, volumes)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'pair': current_pair
        }), 500

@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    """الحصول على المؤشرات الفنية المحسنة"""
    try:
        # توليد بيانات عينة
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        n_points = 50
        
        base_prices = {
            "EURUSD": 1.0850,
            "GBPUSD": 1.2650,
            "USDJPY": 149.50
        }
        
        base_price = base_prices.get(current_pair, 1.0850)
        volatility = 0.0008 if current_pair == 'EURUSD' else 0.0012 if current_pair == 'GBPUSD' else 0.0006
        
        price_changes = np.random.normal(0, volatility, n_points)
        closes = base_price + np.cumsum(price_changes)
        
        highs = closes + np.random.uniform(0, volatility * 0.5, n_points)
        lows = closes - np.random.uniform(0, volatility * 0.5, n_points)
        volumes = np.random.normal(1000, 200, n_points)
        
        # حساب المؤشرات
        indicators_calculator = SimplifiedTechnicalIndicators(current_pair)
        indicators = indicators_calculator.get_all_indicators(highs, lows, closes, volumes)
        
        return jsonify({
            'pair': current_pair,
            'timestamp': datetime.now().isoformat(),
            'indicators': indicators,
            'current_price': closes[-1]
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'pair': current_pair
        }), 500

@app.route('/api/stability/report', methods=['GET'])
def get_stability_report():
    """الحصول على تقرير الاستقرار"""
    try:
        stability_report = current_processor.stabilizer.get_stability_report()
        system_status = current_processor.get_system_status()
        
        return jsonify({
            'pair': current_pair,
            'stability_report': stability_report,
            'system_status': system_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'pair': current_pair
        }), 500

@app.route('/api/signals/history', methods=['GET'])
def get_signals_history():
    """الحصول على تاريخ الإشارات"""
    try:
        # محاكاة تاريخ الإشارات
        signals_history = []
        
        for i in range(10):
            timestamp = datetime.now() - timedelta(hours=i)
            signal_type = np.random.choice(['buy', 'sell', 'neutral'], p=[0.3, 0.3, 0.4])
            confidence = np.random.uniform(40, 95) if signal_type != 'neutral' else 0
            
            signals_history.append({
                'timestamp': timestamp.isoformat(),
                'signal_type': signal_type,
                'confidence': confidence,
                'pair': current_pair,
                'result': np.random.choice(['pending', 'success', 'failed'], p=[0.2, 0.5, 0.3])
            })
        
        return jsonify({
            'pair': current_pair,
            'signals': signals_history,
            'total_signals': len(signals_history)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'pair': current_pair
        }), 500

@app.route('/api/performance', methods=['GET'])
def get_performance_metrics():
    """الحصول على مقاييس الأداء"""
    try:
        # محاكاة مقاييس الأداء
        performance = {
            'pair': current_pair,
            'period': '30_days',
            'total_signals': np.random.randint(50, 150),
            'successful_signals': np.random.randint(30, 100),
            'success_rate': np.random.uniform(60, 85),
            'average_confidence': np.random.uniform(70, 90),
            'total_profit': np.random.uniform(-5, 25),
            'max_drawdown': np.random.uniform(2, 8),
            'sharpe_ratio': np.random.uniform(0.8, 2.5),
            'signals_per_day': np.random.uniform(1.5, 5.0),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(performance)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'pair': current_pair
        }), 500

@app.route('/api/config/update', methods=['POST'])
def update_configuration():
    """تحديث إعدادات النظام"""
    try:
        data = request.get_json()
        
        # تحديث إعدادات المعالج
        if 'signal_confidence_threshold' in data:
            current_processor.stabilizer.config.confirmation_threshold = data['signal_confidence_threshold'] / 100
        
        if 'max_signals_per_session' in data:
            current_processor.max_signals_per_session = data['max_signals_per_session']
        
        if 'volatility_threshold' in data:
            current_processor.stabilizer.config.noise_threshold = data['volatility_threshold']
        
        return jsonify({
            'success': True,
            'message': 'تم تحديث الإعدادات بنجاح',
            'pair': current_pair,
            'updated_config': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """فحص صحة النظام"""
    return jsonify({
        'status': 'healthy',
        'current_pair': current_pair,
        'available_pairs': list(processors.keys()),
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    })

if __name__ == '__main__':
    print("🚀 بدء تشغيل خادم النظام المحسن...")
    print(f"📊 الزوج الافتراضي: {current_pair}")
    print(f"🔧 الأزواج المتاحة: {list(processors.keys())}")
    print("🌐 الخادم متاح على: http://0.0.0.0:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

