from src import db
import requests
from playwright.sync_api import sync_playwright
import json
import time
from datetime import datetime
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PocketOptionInterface:
    """واجهة موحدة للتكامل مع منصة Pocket Option"""
    
    def login(self, username, password):
        """تسجيل الدخول إلى المنصة"""
        pass
    
    def get_assets(self):
        """الحصول على قائمة الأصول المتاحة"""
        pass
    
    def get_candles(self, asset, timeframe, count=100):
        """الحصول على بيانات الشموع"""
        pass
    
    def subscribe_to_asset(self, asset):
        """الاشتراك في تحديثات الأصل في الوقت الفعلي"""
        pass
    
    def unsubscribe_from_asset(self, asset):
        """إلغاء الاشتراك في تحديثات الأصل"""
        pass
    
    def is_connected(self):
        """التحقق من حالة الاتصال"""
        pass


class PocketOptionAPIClient(PocketOptionInterface):
    """عميل API غير رسمي للتكامل مع منصة Pocket Option"""
    
    def __init__(self):
        self.base_url = "https://api.pocketoption.com"
        self.session = requests.Session()
        self.token = None
        self.connected = False
        self.last_request_time = None
        self.rate_limit_delay = 1  # ثانية واحدة بين الطلبات
    
    def _rate_limit(self):
        """تطبيق حد معدل الطلبات"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def login(self, username, password):
        """تسجيل الدخول إلى المنصة"""
        try:
            self._rate_limit()
            # هذا مجرد مثال، يجب تعديله وفقًا للواجهة الفعلية
            response = self.session.post(
                f"{self.base_url}/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.connected = True
                logger.info("تم تسجيل الدخول بنجاح")
                return True
            else:
                logger.error(f"فشل تسجيل الدخول: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تسجيل الدخول: {str(e)}")
            return False
    
    def get_assets(self):
        """الحصول على قائمة الأصول المتاحة"""
        try:
            self._rate_limit()
            # هذا مجرد مثال، يجب تعديله وفقًا للواجهة الفعلية
            response = self.session.get(
                f"{self.base_url}/assets",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"فشل الحصول على الأصول: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الحصول على الأصول: {str(e)}")
            return []
    
    def get_candles(self, asset, timeframe, count=100):
        """الحصول على بيانات الشموع"""
        try:
            self._rate_limit()
            # هذا مجرد مثال، يجب تعديله وفقًا للواجهة الفعلية
            response = self.session.get(
                f"{self.base_url}/candles",
                params={"asset": asset, "timeframe": timeframe, "count": count},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"فشل الحصول على الشموع: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الحصول على الشموع: {str(e)}")
            return []
    
    def subscribe_to_asset(self, asset):
        """الاشتراك في تحديثات الأصل في الوقت الفعلي"""
        try:
            self._rate_limit()
            # هذا مجرد مثال، يجب تعديله وفقًا للواجهة الفعلية
            response = self.session.post(
                f"{self.base_url}/subscribe",
                json={"asset": asset},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                logger.info(f"تم الاشتراك في الأصل {asset} بنجاح")
                return True
            else:
                logger.error(f"فشل الاشتراك في الأصل: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الاشتراك في الأصل: {str(e)}")
            return False
    
    def unsubscribe_from_asset(self, asset):
        """إلغاء الاشتراك في تحديثات الأصل"""
        try:
            self._rate_limit()
            # هذا مجرد مثال، يجب تعديله وفقًا للواجهة الفعلية
            response = self.session.post(
                f"{self.base_url}/unsubscribe",
                json={"asset": asset},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                logger.info(f"تم إلغاء الاشتراك في الأصل {asset} بنجاح")
                return True
            else:
                logger.error(f"فشل إلغاء الاشتراك في الأصل: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"حدث خطأ أثناء إلغاء الاشتراك في الأصل: {str(e)}")
            return False
    
    def is_connected(self):
        """التحقق من حالة الاتصال"""
        return self.connected


class PocketOptionBrowserClient(PocketOptionInterface):
    """عميل محاكاة المتصفح للتكامل مع منصة Pocket Option"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.connected = False
        self.base_url = "https://pocketoption.com"
    
    def _initialize_browser(self):
        """تهيئة المتصفح"""
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
    
    def _close_browser(self):
        """إغلاق المتصفح"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        
        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
    
    def login(self, username, password):
        """تسجيل الدخول إلى المنصة"""
        try:
            self._initialize_browser()
            
            # الانتقال إلى صفحة تسجيل الدخول
            self.page.goto(f"{self.base_url}/login")
            
            # انتظار ظهور نموذج تسجيل الدخول
            self.page.wait_for_selector('input[name="email"]')
            
            # إدخال اسم المستخدم وكلمة المرور
            self.page.fill('input[name="email"]', username)
            self.page.fill('input[name="password"]', password)
            
            # النقر على زر تسجيل الدخول
            self.page.click('button[type="submit"]')
            
            # انتظار الانتقال إلى الصفحة الرئيسية أو لوحة التحكم
            try:
                self.page.wait_for_selector('.dashboard', timeout=10000)
                self.connected = True
                logger.info("تم تسجيل الدخول بنجاح")
                return True
            except Exception:
                logger.error("فشل تسجيل الدخول: لم يتم العثور على لوحة التحكم")
                return False
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تسجيل الدخول: {str(e)}")
            return False
    
    def get_assets(self):
        """الحصول على قائمة الأصول المتاحة"""
        try:
            if not self.connected:
                logger.error("لم يتم تسجيل الدخول")
                return []
            
            # الانتقال إلى صفحة الأصول
            self.page.goto(f"{self.base_url}/trading")
            
            # انتظار تحميل قائمة الأصول
            self.page.wait_for_selector('.asset-list')
            
            # استخراج بيانات الأصول
            assets = self.page.evaluate('''() => {
                const assetElements = document.querySelectorAll('.asset-item');
                return Array.from(assetElements).map(element => {
                    return {
                        symbol: element.getAttribute('data-symbol'),
                        name: element.querySelector('.asset-name').textContent,
                        type: element.getAttribute('data-type'),
                        payout: parseFloat(element.querySelector('.payout').textContent)
                    };
                });
            }''')
            
            return assets
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الحصول على الأصول: {str(e)}")
            return []
    
    def get_candles(self, asset, timeframe, count=100):
        """الحصول على بيانات الشموع"""
        try:
            if not self.connected:
                logger.error("لم يتم تسجيل الدخول")
                return []
            
            # الانتقال إلى صفحة التداول
            self.page.goto(f"{self.base_url}/trading")
            
            # اختيار الأصل
            self.page.click('.asset-selector')
            self.page.fill('.asset-search input', asset)
            self.page.click(f'.asset-item[data-symbol="{asset}"]')
            
            # اختيار الإطار الزمني
            self.page.click('.timeframe-selector')
            self.page.click(f'.timeframe-item[data-value="{timeframe}"]')
            
            # انتظار تحميل الرسم البياني
            self.page.wait_for_selector('.chart-container')
            
            # استخراج بيانات الشموع
            candles = self.page.evaluate(f'''() => {{
                return window.chartData.slice(-{count});
            }}''')
            
            return candles
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الحصول على الشموع: {str(e)}")
            return []
    
    def subscribe_to_asset(self, asset):
        """الاشتراك في تحديثات الأصل في الوقت الفعلي"""
        try:
            if not self.connected:
                logger.error("لم يتم تسجيل الدخول")
                return False
            
            # الانتقال إلى صفحة التداول
            self.page.goto(f"{self.base_url}/trading")
            
            # اختيار الأصل
            self.page.click('.asset-selector')
            self.page.fill('.asset-search input', asset)
            self.page.click(f'.asset-item[data-symbol="{asset}"]')
            
            logger.info(f"تم الاشتراك في الأصل {asset} بنجاح")
            return True
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الاشتراك في الأصل: {str(e)}")
            return False
    
    def unsubscribe_from_asset(self, asset):
        """إلغاء الاشتراك في تحديثات الأصل"""
        # في محاكاة المتصفح، لا نحتاج إلى إلغاء الاشتراك بشكل صريح
        return True
    
    def is_connected(self):
        """التحقق من حالة الاتصال"""
        return self.connected
    
    def __del__(self):
        """المنظف"""
        self._close_browser()


class PocketOptionManager:
    """مدير التكامل مع منصة Pocket Option"""
    
    def __init__(self):
        self.api_client = PocketOptionAPIClient()
        self.browser_client = PocketOptionBrowserClient()
        self.active_client = None
        self.mode = None
    
    def login(self, username, password, mode="api"):
        """تسجيل الدخول إلى المنصة"""
        self.mode = mode
        
        if mode == "api":
            success = self.api_client.login(username, password)
            if success:
                self.active_client = self.api_client
                return True
            else:
                # إذا فشل تسجيل الدخول باستخدام API، نحاول باستخدام المتصفح
                logger.info("فشل تسجيل الدخول باستخدام API، جاري المحاولة باستخدام المتصفح...")
                self.mode = "browser"
                success = self.browser_client.login(username, password)
                if success:
                    self.active_client = self.browser_client
                    return True
                else:
                    return False
        elif mode == "browser":
            success = self.browser_client.login(username, password)
            if success:
                self.active_client = self.browser_client
                return True
            else:
                return False
        else:
            logger.error(f"وضع غير صالح: {mode}")
            return False
    
    def get_assets(self):
        """الحصول على قائمة الأصول المتاحة"""
        if not self.active_client:
            logger.error("لم يتم تسجيل الدخول")
            return []
        
        return self.active_client.get_assets()
    
    def get_candles(self, asset, timeframe, count=100):
        """الحصول على بيانات الشموع"""
        if not self.active_client:
            logger.error("لم يتم تسجيل الدخول")
            return []
        
        return self.active_client.get_candles(asset, timeframe, count)
    
    def subscribe_to_asset(self, asset):
        """الاشتراك في تحديثات الأصل في الوقت الفعلي"""
        if not self.active_client:
            logger.error("لم يتم تسجيل الدخول")
            return False
        
        return self.active_client.subscribe_to_asset(asset)
    
    def unsubscribe_from_asset(self, asset):
        """إلغاء الاشتراك في تحديثات الأصل"""
        if not self.active_client:
            logger.error("لم يتم تسجيل الدخول")
            return False
        
        return self.active_client.unsubscribe_from_asset(asset)
    
    def is_connected(self):
        """التحقق من حالة الاتصال"""
        if not self.active_client:
            return False
        
        return self.active_client.is_connected()
    
    def get_mode(self):
        """الحصول على وضع الاتصال الحالي"""
        return self.mode
