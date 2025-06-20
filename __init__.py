import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# تهيئة قاعدة البيانات
db = SQLAlchemy()

# تهيئة خدمة البريد الإلكتروني
mail = Mail()

def create_app(test_config=None):
    """إنشاء وتكوين تطبيق Flask"""
    
    # إنشاء وتكوين التطبيق
    app = Flask(__name__, instance_relative_config=True)
    
    # التكوين الافتراضي
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI', 'sqlite:///pocket_option_platform.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER=os.environ.get('MAIL_SERVER', 'smtp.gmail.com'),
        MAIL_PORT=int(os.environ.get('MAIL_PORT', 587)),
        MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS', 'True') == 'True',
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER'),
    )
    
    # تحميل تكوين الاختبار إذا تم تمريره
    if test_config is not None:
        app.config.update(test_config)
    
    # التأكد من وجود مجلد المثيل
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # تهيئة CORS
    CORS(app)
    
    # تهيئة قاعدة البيانات
    db.init_app(app)
    
    # تهيئة خدمة البريد الإلكتروني
    mail.init_app(app)
    
    # تسجيل النماذج
    from src.models import user, signal, notification, asset
    
    # تسجيل المسارات
    from src.routes import api, auth
    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    
    # تسجيل أمر تهيئة قاعدة البيانات
    @app.cli.command('init-db')
    def init_db_command():
        """تهيئة قاعدة البيانات وإنشاء الجداول."""
        db.create_all()
        print('تم تهيئة قاعدة البيانات.')
    
    return app
