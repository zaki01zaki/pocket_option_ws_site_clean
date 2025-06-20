from src import db
from datetime import datetime

class Notification(db.Model):
    """نموذج الإشعارات المرسلة"""
    __tablename__ = 'notifications_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel = db.Column(db.String(20), nullable=False)  # "telegram", "email", "sms"
    recipient = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)  # "success", "failed"
    error = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Notification {self.channel} {self.timestamp}>'


class NotificationSetting(db.Model):
    """نموذج إعدادات الإشعارات"""
    __tablename__ = 'notification_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel = db.Column(db.String(20), nullable=False)  # "telegram", "email", "sms"
    enabled = db.Column(db.Boolean, default=True)
    recipient = db.Column(db.String(120), nullable=False)
    min_confidence = db.Column(db.Float, default=0.7)
    
    def __repr__(self):
        return f'<NotificationSetting {self.channel} {self.enabled}>'
