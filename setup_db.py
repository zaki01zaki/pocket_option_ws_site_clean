from src import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("تم إنشاء قاعدة البيانات بنجاح!")
