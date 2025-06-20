
# Trading Platform - Pocket Option Real-Time Prices

## 🛠️ وصف المشروع
نظام متكامل يقوم باستخراج روابط WebSocket الحية من Pocket Option بشكل تلقائي، والاتصال بها لجلب الأسعار الحقيقية في الوقت الفعلي.

## ✅ مميزات النظام
- استخراج دوري لرابط WebSocket الحي.
- بث الأسعار الحية باستخدام WebSocket API.
- API يعرض أحدث الأسعار عبر `/latest-prices`.
- واجهة أمامية تفاعلية مع بث لحظي للأسعار.

## 🚀 خطوات التشغيل
```bash
pip install -r requirements.txt
python pocket_option_ws_auto.py
```

- الواجهة الأمامية: `http://localhost:8000/static/index.html`
- API الأسعار: `http://localhost:8000/latest-prices`
- WebSocket: `ws://localhost:8000/ws`

## 📂 هيكلة المشروع
- pocket_option_ws_auto.py → الكود الخلفي
- static/index.html → الواجهة الأمامية
- requirements.txt → الحزم المطلوبة
- render.yaml → ملف نشر Render.com
- start.sh → أمر بدء السيرفر

## ✨ تم التطوير بواسطة
zaki zaza
