from flask import Blueprint, jsonify, request, current_app
from src.models.user import User
from src import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """تسجيل مستخدم جديد"""
    data = request.json
    
    # التحقق من وجود البيانات المطلوبة
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': 'البيانات غير كاملة'
        }), 400
    
    # التحقق من عدم وجود مستخدم بنفس اسم المستخدم أو البريد الإلكتروني
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'success': False,
            'message': 'اسم المستخدم مستخدم بالفعل'
        }), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'success': False,
            'message': 'البريد الإلكتروني مستخدم بالفعل'
        }), 400
    
    # إنشاء مستخدم جديد
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    # حفظ المستخدم في قاعدة البيانات
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'تم تسجيل المستخدم بنجاح',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """تسجيل الدخول"""
    data = request.json
    
    # التحقق من وجود البيانات المطلوبة
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': 'البيانات غير كاملة'
        }), 400
    
    # البحث عن المستخدم
    user = User.query.filter_by(username=data['username']).first()
    
    # التحقق من وجود المستخدم وصحة كلمة المرور
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({
            'success': False,
            'message': 'اسم المستخدم أو كلمة المرور غير صحيحة'
        }), 401
    
    # تحديث آخر تسجيل دخول
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # إنشاء رمز الجلسة (في تطبيق حقيقي، يجب استخدام JWT أو طريقة أخرى آمنة)
    # هذا مجرد مثال بسيط
    
    return jsonify({
        'success': True,
        'message': 'تم تسجيل الدخول بنجاح',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'token': 'sample_token'  # في تطبيق حقيقي، يجب استخدام JWT أو طريقة أخرى آمنة
    })

@bp.route('/me', methods=['GET'])
def me():
    """الحصول على معلومات المستخدم الحالي"""
    # في تطبيق حقيقي، يجب التحقق من رمز الجلسة والحصول على المستخدم الحالي
    # هذا مجرد مثال بسيط
    
    # محاكاة المستخدم الحالي
    user = User.query.first()
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'المستخدم غير موجود'
        }), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

@bp.route('/logout', methods=['POST'])
def logout():
    """تسجيل الخروج"""
    # في تطبيق حقيقي، يجب إلغاء رمز الجلسة
    # هذا مجرد مثال بسيط
    
    return jsonify({
        'success': True,
        'message': 'تم تسجيل الخروج بنجاح'
    })
