from src import db
from datetime import datetime

class Asset(db.Model):
    """نموذج الأصول المتاحة للتداول"""
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(20), nullable=False)  # "currency", "stock", "commodity", "index"
    is_active = db.Column(db.Boolean, default=True)
    payout = db.Column(db.Float)  # نسبة العائد
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات
    candles = db.relationship('Candle', backref='asset_data', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Asset {self.symbol} {self.name}>'


class Candle(db.Model):
    """نموذج بيانات الشموع"""
    __tablename__ = 'candles'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    timeframe = db.Column(db.String(10), nullable=False)  # "1m", "5m", "15m", "30m", "1h", "4h", "1d"
    timestamp = db.Column(db.DateTime, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float)
    is_otc = db.Column(db.Boolean, default=False)  # علامة OTC
    
    __table_args__ = (
        db.Index('idx_asset_timeframe_timestamp', 'asset_id', 'timeframe', 'timestamp'),
    )
    
    def __repr__(self):
        return f'<Candle {self.asset_id} {self.timeframe} {self.timestamp}>'


class Setting(db.Model):
    """نموذج إعدادات المنصة العامة"""
    __tablename__ = 'settings'
    
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Setting {self.key}>'
