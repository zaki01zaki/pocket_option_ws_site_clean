import logging
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABC, abstractmethod

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotificationChannel(ABC):
    """واجهة قناة الإشعارات الأساسية"""
    
    @abstractmethod
    def send_notification(self, recipient, subject, message):
        """إرسال إشعار عبر القناة"""
        pass
    
    @abstractmethod
    def is_configured(self):
        """التحقق من تكوين القناة"""
        pass


class TelegramChannel(NotificationChannel):
    """قناة إشعارات تيليجرام"""
    
    def __init__(self, bot_token=None):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}" if bot_token else None
    
    def configure(self, bot_token):
        """تكوين قناة تيليجرام"""
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        return self.is_configured()
    
    def is_configured(self):
        """التحقق من تكوين القناة"""
        if not self.bot_token or not self.api_url:
            return False
        
        try:
            response = requests.get(f"{self.api_url}/getMe")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"خطأ في التحقق من تكوين قناة تيليجرام: {str(e)}")
            return False
    
    def send_notification(self, recipient, subject, message):
        """إرسال إشعار عبر تيليجرام"""
        if not self.is_configured():
            logger.error("قناة تيليجرام غير مكونة بشكل صحيح")
            return False
        
        try:
            # في تيليجرام، recipient هو chat_id
            chat_id = recipient
            
            # دمج الموضوع والرسالة
            full_message = f"*{subject}*\n\n{message}"
            
            # إرسال الرسالة
            payload = {
                'chat_id': chat_id,
                'text': full_message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(f"{self.api_url}/sendMessage", json=payload)
            
            if response.status_code == 200:
                logger.info(f"تم إرسال إشعار تيليجرام بنجاح إلى {chat_id}")
                return True
            else:
                logger.error(f"فشل إرسال إشعار تيليجرام: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"خطأ في إرسال إشعار تيليجرام: {str(e)}")
            return False


class EmailChannel(NotificationChannel):
    """قناة إشعارات البريد الإلكتروني"""
    
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None, use_tls=True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
    
    def configure(self, smtp_server, smtp_port, username, password, use_tls=True):
        """تكوين قناة البريد الإلكتروني"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        return self.is_configured()
    
    def is_configured(self):
        """التحقق من تكوين القناة"""
        return all([self.smtp_server, self.smtp_port, self.username, self.password])
    
    def send_notification(self, recipient, subject, message):
        """إرسال إشعار عبر البريد الإلكتروني"""
        if not self.is_configured():
            logger.error("قناة البريد الإلكتروني غير مكونة بشكل صحيح")
            return False
        
        try:
            # إنشاء رسالة البريد الإلكتروني
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # إضافة نص الرسالة
            msg.attach(MIMEText(message, 'plain'))
            
            # الاتصال بخادم SMTP وإرسال الرسالة
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"تم إرسال إشعار بريد إلكتروني بنجاح إلى {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إرسال إشعار بريد إلكتروني: {str(e)}")
            return False


class SMSChannel(NotificationChannel):
    """قناة إشعارات الرسائل النصية (باستخدام Twilio)"""
    
    def __init__(self, account_sid=None, auth_token=None, from_number=None):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.client = None
        
        # محاولة استيراد مكتبة Twilio
        try:
            from twilio.rest import Client
            if self.account_sid and self.auth_token:
                self.client = Client(self.account_sid, self.auth_token)
        except ImportError:
            logger.warning("مكتبة Twilio غير مثبتة. يرجى تثبيتها باستخدام 'pip install twilio'")
    
    def configure(self, account_sid, auth_token, from_number):
        """تكوين قناة الرسائل النصية"""
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        
        try:
            from twilio.rest import Client
            self.client = Client(self.account_sid, self.auth_token)
            return self.is_configured()
        except ImportError:
            logger.error("مكتبة Twilio غير مثبتة. يرجى تثبيتها باستخدام 'pip install twilio'")
            return False
    
    def is_configured(self):
        """التحقق من تكوين القناة"""
        return all([self.account_sid, self.auth_token, self.from_number, self.client])
    
    def send_notification(self, recipient, subject, message):
        """إرسال إشعار عبر الرسائل النصية"""
        if not self.is_configured():
            logger.error("قناة الرسائل النصية غير مكونة بشكل صحيح")
            return False
        
        try:
            # في الرسائل النصية، نضيف الموضوع في بداية الرسالة
            full_message = f"{subject}: {message}"
            
            # إرسال الرسالة النصية
            sms = self.client.messages.create(
                body=full_message,
                from_=self.from_number,
                to=recipient
            )
            
            logger.info(f"تم إرسال إشعار رسالة نصية بنجاح إلى {recipient}, SID: {sms.sid}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إرسال إشعار رسالة نصية: {str(e)}")
            return False


class NotificationManager:
    """مدير الإشعارات المسؤول عن إدارة قنوات الإشعارات وإرسال الإشعارات"""
    
    def __init__(self):
        self.channels = {
            'telegram': TelegramChannel(),
            'email': EmailChannel(),
            'sms': SMSChannel()
        }
        self.enabled_channels = set()
    
    def configure_channel(self, channel_type, **config):
        """تكوين قناة إشعارات محددة"""
        if channel_type not in self.channels:
            logger.error(f"نوع القناة غير معروف: {channel_type}")
            return False
        
        channel = self.channels[channel_type]
        
        try:
            if channel_type == 'telegram':
                success = channel.configure(
                    bot_token=config.get('bot_token')
                )
            elif channel_type == 'email':
                success = channel.configure(
                    smtp_server=config.get('smtp_server'),
                    smtp_port=config.get('smtp_port'),
                    username=config.get('username'),
                    password=config.get('password'),
                    use_tls=config.get('use_tls', True)
                )
            elif channel_type == 'sms':
                success = channel.configure(
                    account_sid=config.get('account_sid'),
                    auth_token=config.get('auth_token'),
                    from_number=config.get('from_number')
                )
            else:
                success = False
            
            if success:
                self.enabled_channels.add(channel_type)
                logger.info(f"تم تكوين قناة {channel_type} بنجاح")
            else:
                logger.error(f"فشل تكوين قناة {channel_type}")
            
            return success
            
        except Exception as e:
            logger.error(f"خطأ في تكوين قناة {channel_type}: {str(e)}")
            return False
    
    def enable_channel(self, channel_type):
        """تمكين قناة إشعارات"""
        if channel_type not in self.channels:
            logger.error(f"نوع القناة غير معروف: {channel_type}")
            return False
        
        if self.channels[channel_type].is_configured():
            self.enabled_channels.add(channel_type)
            logger.info(f"تم تمكين قناة {channel_type}")
            return True
        else:
            logger.error(f"لا يمكن تمكين قناة {channel_type} لأنها غير مكونة بشكل صحيح")
            return False
    
    def disable_channel(self, channel_type):
        """تعطيل قناة إشعارات"""
        if channel_type in self.enabled_channels:
            self.enabled_channels.remove(channel_type)
            logger.info(f"تم تعطيل قناة {channel_type}")
            return True
        return False
    
    def send_notification(self, channel_type, recipient, subject, message):
        """إرسال إشعار عبر قناة محددة"""
        if channel_type not in self.channels:
            logger.error(f"نوع القناة غير معروف: {channel_type}")
            return False
        
        if channel_type not in self.enabled_channels:
            logger.error(f"قناة {channel_type} غير ممكنة")
            return False
        
        channel = self.channels[channel_type]
        return channel.send_notification(recipient, subject, message)
    
    def broadcast_notification(self, recipients, subject, message, channels=None):
        """إرسال إشعار عبر قنوات متعددة إلى مستلمين متعددين"""
        if channels is None:
            channels = list(self.enabled_channels)
        
        results = {}
        
        for channel_type in channels:
            if channel_type not in self.enabled_channels:
                logger.warning(f"قناة {channel_type} غير ممكنة، سيتم تخطيها")
                continue
            
            channel_recipients = recipients.get(channel_type, [])
            channel_results = []
            
            for recipient in channel_recipients:
                success = self.send_notification(channel_type, recipient, subject, message)
                channel_results.append({
                    'recipient': recipient,
                    'success': success
                })
            
            results[channel_type] = channel_results
        
        return results
    
    def send_signal_notification(self, signal, recipients):
        """إرسال إشعار بإشارة تداول"""
        # تحضير محتوى الإشعار
        direction = "شراء (CALL)" if signal['direction'] == 'call' else "بيع (PUT)"
        confidence = f"{signal['confidence'] * 100:.1f}%"
        timestamp = signal['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        subject = f"إشارة تداول جديدة: {direction} | الثقة: {confidence}"
        
        # إنشاء نص الرسالة
        message = f"""
تم توليد إشارة تداول جديدة:

الاتجاه: {direction}
مستوى الثقة: {confidence}
التوقيت: {timestamp}

التأكيدات الإيجابية:
"""
        
        # إضافة التأكيدات الإيجابية
        positive_confirmations = [name for name, confirmed in signal['confirmations'].items() if confirmed]
        for i, conf in enumerate(positive_confirmations[:10], 1):  # عرض أول 10 تأكيدات فقط
            message += f"- {conf}\n"
        
        if len(positive_confirmations) > 10:
            message += f"- و{len(positive_confirmations) - 10} تأكيدات أخرى\n"
        
        # إرسال الإشعار عبر جميع القنوات الممكنة
        return self.broadcast_notification(recipients, subject, message)


# مثال للاستخدام (للاختبار)
if __name__ == '__main__':
    # إنشاء مدير الإشعارات
    notification_manager = NotificationManager()
    
    # تكوين قنوات الإشعارات (أمثلة)
    telegram_config = {
        'bot_token': '1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    }
    
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'your_email@gmail.com',
        'password': 'your_password',
        'use_tls': True
    }
    
    sms_config = {
        'account_sid': 'AC1234567890abcdef1234567890abcdef',
        'auth_token': '1234567890abcdef1234567890abcdef',
        'from_number': '+12345678901'
    }
    
    # تكوين القنوات (تعليق لتجنب الأخطاء في الاختبار)
    # notification_manager.configure_channel('telegram', **telegram_config)
    # notification_manager.configure_channel('email', **email_config)
    # notification_manager.configure_channel('sms', **sms_config)
    
    # تمكين القنوات
    # notification_manager.enable_channel('telegram')
    # notification_manager.enable_channel('email')
    # notification_manager.enable_channel('sms')
    
    # إنشاء إشارة تداول وهمية
    from datetime import datetime
    import random
    
    dummy_signal = {
        'timestamp': datetime.now(),
        'direction': random.choice(['call', 'put']),
        'confidence': random.uniform(0.6, 0.95),
        'confirmations': {
            'RSI_Oversold': True,
            'MACD_Crossed_Up_Signal': True,
            'Price_Above_SMA20': True,
            'SMA10_Above_SMA20': True,
            'Stoch_Oversold': True,
            'Price_Touched_BB_Lower': True,
            'Volume_Above_SMA20': True,
            'RSI_Increasing': True,
            'MACD_Histogram_Positive': True,
            'Stoch_K_Crossed_Up_D': True,
            'Dummy_Confirmation_1': False,
            'Dummy_Confirmation_2': False
        }
    }
    
    # تحديد المستلمين
    recipients = {
        'telegram': ['123456789'],
        'email': ['recipient@example.com'],
        'sms': ['+12345678901']
    }
    
    # إرسال إشعار (تعليق لتجنب الأخطاء في الاختبار)
    # results = notification_manager.send_signal_notification(dummy_signal, recipients)
    # print(results)
