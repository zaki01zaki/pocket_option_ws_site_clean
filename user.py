from src import db
from datetime import datetime

class User(db.Model):
    """نموذج المستخدم"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # العلاقات
    signals = db.relationship('Signal', backref='user', lazy=True)
    notification_settings = db.relationship('NotificationSetting', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
