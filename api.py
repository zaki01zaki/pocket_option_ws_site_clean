from flask import Blueprint, jsonify, request, current_app
from src.models.signal import Signal, Confirmation
from src.models.asset import Asset, Candle
from src import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/signals', methods=['GET'])
def get_signals():
    """الحصول على الإشارات"""
    timeframe = request.args.get('timeframe')
    asset = request.args.get('asset')
    limit = request.args.get('limit', 20, type=int)
    
    # بناء الاستعلام
    query = Signal.query
    
    # تطبيق الفلاتر
    if timeframe:
        query = query.filter(Signal.timeframe == timeframe)
    if asset:
        query = query.filter(Signal.asset == asset)
    
    # ترتيب النتائج وتحديد العدد
    signals = query.order_by(Signal.timestamp.desc()).limit(limit).all()
    
    # تحويل النتائج إلى JSON
    result = []
    for signal in signals:
        confirmations = []
        for conf in signal.confirmations:
            confirmations.append({
                'name': conf.name,
                'confirmed': conf.confirmed,
                'value': conf.value
            })
        
        result.append({
            'id': signal.id,
            'asset': signal.asset,
            'timeframe': signal.timeframe,
            'direction': signal.direction,
            'confidence': signal.confidence,
            'timestamp': signal.timestamp.isoformat(),
            'is_otc': signal.is_otc,
            'confirmations': confirmations
        })
    
    return jsonify({
        'success': True,
        'data': result
    })

@bp.route('/assets', methods=['GET'])
def get_assets():
    """الحصول على قائمة الأصول المتاحة"""
    assets = Asset.query.filter_by(is_active=True).all()
    
    result = []
    for asset in assets:
        result.append({
            'id': asset.id,
            'symbol': asset.symbol,
            'name': asset.name,
            'asset_type': asset.asset_type,
            'payout': asset.payout
        })
    
    return jsonify({
        'success': True,
        'data': result
    })

@bp.route('/charts/data', methods=['GET'])
def get_chart_data():
    """الحصول على بيانات الرسوم البيانية"""
    asset_symbol = request.args.get('asset')
    timeframe = request.args.get('timeframe', '1h')
    limit = request.args.get('limit', 100, type=int)
    
    # التحقق من وجود الأصل
    asset = Asset.query.filter_by(symbol=asset_symbol).first()
    if not asset:
        return jsonify({
            'success': False,
            'message': 'الأصل غير موجود'
        }), 404
    
    # الحصول على بيانات الشموع
    candles = Candle.query.filter_by(
        asset_id=asset.id,
        timeframe=timeframe
    ).order_by(Candle.timestamp.desc()).limit(limit).all()
    
    # تحويل النتائج إلى JSON
    result = []
    for candle in candles:
        result.append({
            'timestamp': candle.timestamp.isoformat(),
            'open': candle.open,
            'high': candle.high,
            'low': candle.low,
            'close': candle.close,
            'volume': candle.volume,
            'is_otc': candle.is_otc
        })
    
    return jsonify({
        'success': True,
        'data': {
            'asset': {
                'symbol': asset.symbol,
                'name': asset.name
            },
            'timeframe': timeframe,
            'candles': result
        }
    })

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    """الحصول على بيانات لوحة التحكم"""
    # الحصول على الإشارات الأخيرة
    recent_signals = Signal.query.order_by(Signal.timestamp.desc()).limit(5).all()
    signals = []
    for signal in recent_signals:
        signals.append({
            'id': signal.id,
            'asset': signal.asset,
            'timeframe': signal.timeframe,
            'direction': signal.direction,
            'confidence': signal.confidence,
            'timestamp': signal.timestamp.isoformat(),
            'is_otc': signal.is_otc
        })
    
    # الحصول على الأصول النشطة
    active_assets = Asset.query.filter_by(is_active=True).all()
    assets = []
    for asset in active_assets:
        assets.append({
            'id': asset.id,
            'symbol': asset.symbol,
            'name': asset.name,
            'asset_type': asset.asset_type,
            'payout': asset.payout
        })
    
    # إحصائيات بسيطة
    total_signals = Signal.query.count()
    call_signals = Signal.query.filter_by(direction='call').count()
    put_signals = Signal.query.filter_by(direction='put').count()
    
    return jsonify({
        'success': True,
        'data': {
            'signals': signals,
            'assets': assets,
            'stats': {
                'total_signals': total_signals,
                'call_signals': call_signals,
                'put_signals': put_signals
            }
        }
    })

@bp.route('/integration/status', methods=['GET'])
def integration_status():
    """الحصول على حالة الاتصال بـ Pocket Option"""
    # في تطبيق حقيقي، يجب التحقق من حالة الاتصال الفعلية
    # هذا مجرد مثال بسيط
    
    return jsonify({
        'success': True,
        'data': {
            'connected': True,
            'last_update': '2025-06-03T10:30:00Z',
            'mode': 'API',  # أو 'BROWSER'
            'status': 'active'
        }
    })
