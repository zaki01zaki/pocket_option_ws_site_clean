import os
import time
import json
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PocketOptionDataCollector:
    """آلية جمع البيانات الحية من منصة Pocket Option"""
    
    def __init__(self, headless=False, data_dir=None):
        """تهيئة آلية جمع البيانات"""
        self.headless = headless
        self.driver = None
        self.is_logged_in = False
        self.data_dir = data_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        
        # إنشاء مجلد البيانات إذا لم يكن موجوداً
        os.makedirs(self.data_dir, exist_ok=True)
        
        # الأطر الزمنية المدعومة
        self.timeframes = {
            '1m': '1 دقيقة',
            '5m': '5 دقائق',
            '15m': '15 دقيقة',
            '30m': '30 دقيقة',
            '1h': '1 ساعة',
            '4h': '4 ساعات',
            '1d': 'يومي'
        }
        
        # الأصول المدعومة (سيتم تحديثها بعد تسجيل الدخول)
        self.assets = {}
        
        logger.info("تم تهيئة آلية جمع البيانات")
    
    def initialize_browser(self):
        """تهيئة متصفح Chrome"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(60)
            logger.info("تم تهيئة المتصفح بنجاح")
            return True
        except Exception as e:
            logger.error(f"فشل في تهيئة المتصفح: {str(e)}")
            return False
    
    def login(self, email=None, password=None):
        """تسجيل الدخول إلى منصة Pocket Option
        
        إذا لم يتم توفير البريد الإلكتروني وكلمة المرور، سيتم طلب تسجيل الدخول اليدوي
        """
        if self.driver is None:
            if not self.initialize_browser():
                return False
        
        try:
            # الانتقال إلى صفحة تسجيل الدخول
            self.driver.get("https://pocketoption.com/en/login/")
            logger.info("تم الانتقال إلى صفحة تسجيل الدخول")
            
            # انتظار تحميل الصفحة
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-form"))
            )
            
            if email and password:
                # تسجيل الدخول تلقائياً
                logger.info("محاولة تسجيل الدخول تلقائياً")
                
                # إدخال البريد الإلكتروني
                email_input = self.driver.find_element(By.NAME, "email")
                email_input.clear()
                email_input.send_keys(email)
                
                # إدخال كلمة المرور
                password_input = self.driver.find_element(By.NAME, "password")
                password_input.clear()
                password_input.send_keys(password)
                
                # النقر على زر تسجيل الدخول
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                login_button.click()
                
                # انتظار الانتقال إلى لوحة التحكم
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.url_contains("/en/cabinet/")
                    )
                    self.is_logged_in = True
                    logger.info("تم تسجيل الدخول تلقائياً بنجاح")
                except TimeoutException:
                    logger.warning("فشل تسجيل الدخول التلقائي، قد تكون هناك حاجة للتحقق البشري")
                    # التحقق من وجود رسالة خطأ
                    try:
                        error_message = self.driver.find_element(By.CLASS_NAME, "error-message").text
                        logger.error(f"رسالة الخطأ: {error_message}")
                    except NoSuchElementException:
                        pass
            else:
                # تسجيل الدخول اليدوي
                logger.info("يرجى تسجيل الدخول يدوياً في نافذة المتصفح")
                logger.info("سيتم انتظار الانتقال إلى لوحة التحكم...")
                
                # انتظار الانتقال إلى لوحة التحكم (بعد تسجيل الدخول اليدوي)
                try:
                    WebDriverWait(self.driver, 300).until(  # انتظار لمدة 5 دقائق كحد أقصى
                        EC.url_contains("/en/cabinet/")
                    )
                    self.is_logged_in = True
                    logger.info("تم تسجيل الدخول يدوياً بنجاح")
                except TimeoutException:
                    logger.error("انتهت مهلة انتظار تسجيل الدخول اليدوي")
                    return False
            
            # الانتقال إلى منصة التداول
            if self.is_logged_in:
                self.driver.get("https://pocketoption.com/en/cabinet/demo-quick-high-low/")
                logger.info("تم الانتقال إلى منصة التداول")
                
                # انتظار تحميل منصة التداول
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "chart-container"))
                )
                
                # تحديث قائمة الأصول المتاحة
                self._update_assets_list()
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تسجيل الدخول: {str(e)}")
            return False
    
    def _update_assets_list(self):
        """تحديث قائمة الأصول المتاحة"""
        try:
            # النقر على قائمة الأصول
            asset_selector = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".asset-selector"))
            )
            asset_selector.click()
            
            # انتظار ظهور قائمة الأصول
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".asset-list"))
            )
            
            # استخراج الأصول المتاحة
            asset_elements = self.driver.find_elements(By.CSS_SELECTOR, ".asset-list .asset-item")
            
            for element in asset_elements:
                try:
                    asset_id = element.get_attribute("data-asset-id")
                    asset_name = element.find_element(By.CSS_SELECTOR, ".asset-name").text
                    self.assets[asset_name] = asset_id
                except Exception as e:
                    logger.warning(f"فشل في استخراج معلومات الأصل: {str(e)}")
            
            # إغلاق قائمة الأصول
            self.driver.find_element(By.CSS_SELECTOR, "body").click()
            
            logger.info(f"تم تحديث قائمة الأصول: {len(self.assets)} أصل متاح")
            
        except Exception as e:
            logger.error(f"فشل في تحديث قائمة الأصول: {str(e)}")
    
    def select_asset(self, asset_name):
        """اختيار أصل للتداول"""
        if not self.is_logged_in:
            logger.error("يجب تسجيل الدخول أولاً")
            return False
        
        try:
            # النقر على قائمة الأصول
            asset_selector = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".asset-selector"))
            )
            asset_selector.click()
            
            # انتظار ظهور قائمة الأصول
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".asset-list"))
            )
            
            # البحث عن الأصل المطلوب
            asset_elements = self.driver.find_elements(By.CSS_SELECTOR, ".asset-list .asset-item")
            
            for element in asset_elements:
                try:
                    current_asset_name = element.find_element(By.CSS_SELECTOR, ".asset-name").text
                    if current_asset_name.lower() == asset_name.lower():
                        element.click()
                        logger.info(f"تم اختيار الأصل: {asset_name}")
                        time.sleep(2)  # انتظار تحديث الرسم البياني
                        return True
                except Exception as e:
                    logger.warning(f"فشل في التحقق من الأصل: {str(e)}")
            
            logger.error(f"الأصل غير موجود: {asset_name}")
            
            # إغلاق قائمة الأصول
            self.driver.find_element(By.CSS_SELECTOR, "body").click()
            
            return False
            
        except Exception as e:
            logger.error(f"فشل في اختيار الأصل: {str(e)}")
            return False
    
    def select_timeframe(self, timeframe):
        """اختيار الإطار الزمني"""
        if not self.is_logged_in:
            logger.error("يجب تسجيل الدخول أولاً")
            return False
        
        if timeframe not in self.timeframes:
            logger.error(f"الإطار الزمني غير مدعوم: {timeframe}")
            return False
        
        try:
            # النقر على قائمة الأطر الزمنية
            timeframe_selector = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".timeframe-selector"))
            )
            timeframe_selector.click()
            
            # انتظار ظهور قائمة الأطر الزمنية
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".timeframe-list"))
            )
            
            # البحث عن الإطار الزمني المطلوب
            timeframe_elements = self.driver.find_elements(By.CSS_SELECTOR, ".timeframe-list .timeframe-item")
            
            for element in timeframe_elements:
                try:
                    if element.text.strip() == self.timeframes[timeframe]:
                        element.click()
                        logger.info(f"تم اختيار الإطار الزمني: {timeframe}")
                        time.sleep(2)  # انتظار تحديث الرسم البياني
                        return True
                except Exception as e:
                    logger.warning(f"فشل في التحقق من الإطار الزمني: {str(e)}")
            
            logger.error(f"الإطار الزمني غير موجود: {timeframe}")
            
            # إغلاق قائمة الأطر الزمنية
            self.driver.find_element(By.CSS_SELECTOR, "body").click()
            
            return False
            
        except Exception as e:
            logger.error(f"فشل في اختيار الإطار الزمني: {str(e)}")
            return False
    
    def collect_candle_data(self, num_candles=100):
        """جمع بيانات الشموع من الرسم البياني الحالي"""
        if not self.is_logged_in:
            logger.error("يجب تسجيل الدخول أولاً")
            return None
        
        try:
            # تنفيذ سكريبت JavaScript لاستخراج بيانات الشموع
            script = """
            return (function() {
                // الوصول إلى كائن الرسم البياني
                var chart = window.chart || window.mainChart;
                if (!chart) {
                    return { error: "لم يتم العثور على كائن الرسم البياني" };
                }
                
                try {
                    // استخراج بيانات الشموع
                    var candles = chart.series[0].data;
                    var result = [];
                    
                    for (var i = 0; i < candles.length; i++) {
                        var candle = candles[i];
                        result.push({
                            timestamp: candle.x,
                            open: candle.open,
                            high: candle.high,
                            low: candle.low,
                            close: candle.close,
                            volume: candle.volume || 0
                        });
                    }
                    
                    // استخراج معلومات الأصل والإطار الزمني
                    var assetInfo = {
                        name: chart.options.title.text || document.querySelector('.asset-name').textContent,
                        timeframe: document.querySelector('.timeframe-selector').textContent.trim()
                    };
                    
                    return {
                        asset: assetInfo,
                        candles: result
                    };
                } catch (e) {
                    return { error: e.toString() };
                }
            })();
            """
            
            # تنفيذ السكريبت
            result = self.driver.execute_script(script)
            
            if 'error' in result:
                logger.error(f"فشل في استخراج بيانات الشموع: {result['error']}")
                return None
            
            # تحويل البيانات إلى DataFrame
            candles_data = result['candles']
            
            if not candles_data:
                logger.warning("لم يتم العثور على بيانات شموع")
                return None
            
            # تحويل الطوابع الزمنية إلى تواريخ
            for candle in candles_data:
                candle['timestamp'] = datetime.fromtimestamp(candle['timestamp'] / 1000)
            
            # إنشاء DataFrame
            df = pd.DataFrame(candles_data)
            
            # ترتيب البيانات حسب الوقت
            df = df.sort_values('timestamp')
            
            # اقتصار البيانات على العدد المطلوب
            if len(df) > num_candles:
                df = df.tail(num_candles)
            
            logger.info(f"تم جمع {len(df)} شمعة لـ {result['asset']['name']} على الإطار الزمني {result['asset']['timeframe']}")
            
            return {
                'asset': result['asset'],
                'data': df
            }
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء جمع بيانات الشموع: {str(e)}")
            return None
    
    def save_candle_data(self, candle_data, filename=None):
        """حفظ بيانات الشموع في ملف CSV"""
        if candle_data is None or 'data' not in candle_data:
            logger.error("لا توجد بيانات شموع لحفظها")
            return False
        
        try:
            asset_name = candle_data['asset']['name'].replace(' ', '_')
            timeframe = candle_data['asset']['timeframe'].replace(' ', '_')
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{asset_name}_{timeframe}_{timestamp}.csv"
            
            filepath = os.path.join(self.data_dir, filename)
            
            # حفظ البيانات
            candle_data['data'].to_csv(filepath, index=False)
            
            logger.info(f"تم حفظ بيانات الشموع في {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"فشل في حفظ بيانات الشموع: {str(e)}")
            return False
    
    def collect_and_save_data(self, asset_name, timeframe, num_candles=100, filename=None):
        """جمع وحفظ بيانات الشموع لأصل وإطار زمني محددين"""
        if not self.select_asset(asset_name):
            return False
        
        if not self.select_timeframe(timeframe):
            return False
        
        # انتظار تحديث الرسم البياني
        time.sleep(3)
        
        # جمع البيانات
        candle_data = self.collect_candle_data(num_candles)
        
        if candle_data is None:
            return False
        
        # حفظ البيانات
        return self.save_candle_data(candle_data, filename)
    
    def collect_multiple_assets(self, assets, timeframe, num_candles=100):
        """جمع بيانات لعدة أصول على إطار زمني محدد"""
        results = {}
        
        for asset in assets:
            logger.info(f"جمع بيانات الأصل: {asset}")
            
            filepath = self.collect_and_save_data(asset, timeframe, num_candles)
            
            if filepath:
                results[asset] = filepath
            else:
                results[asset] = None
                logger.warning(f"فشل في جمع بيانات الأصل: {asset}")
        
        return results
    
    def collect_multiple_timeframes(self, asset_name, timeframes, num_candles=100):
        """جمع بيانات لأصل محدد على عدة أطر زمنية"""
        results = {}
        
        for timeframe in timeframes:
            if timeframe not in self.timeframes:
                logger.warning(f"الإطار الزمني غير مدعوم: {timeframe}")
                results[timeframe] = None
                continue
            
            logger.info(f"جمع بيانات الإطار الزمني: {timeframe}")
            
            filepath = self.collect_and_save_data(asset_name, timeframe, num_candles)
            
            if filepath:
                results[timeframe] = filepath
            else:
                results[timeframe] = None
                logger.warning(f"فشل في جمع بيانات الإطار الزمني: {timeframe}")
        
        return results
    
    def setup_data_collection_schedule(self, assets, timeframes, interval_minutes=5):
        """إعداد جدول لجمع البيانات بشكل دوري"""
        logger.info(f"بدء جدول جمع البيانات كل {interval_minutes} دقائق")
        
        try:
            while True:
                start_time = datetime.now()
                logger.info(f"بدء دورة جمع البيانات في {start_time}")
                
                for asset in assets:
                    for timeframe in timeframes:
                        if timeframe in self.timeframes:
                            logger.info(f"جمع بيانات {asset} على الإطار الزمني {timeframe}")
                            self.collect_and_save_data(asset, timeframe)
                        else:
                            logger.warning(f"الإطار الزمني غير مدعوم: {timeframe}")
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # حساب وقت الانتظار حتى الدورة التالية
                wait_seconds = max(0, interval_minutes * 60 - duration)
                
                if wait_seconds > 0:
                    logger.info(f"انتظار {wait_seconds} ثانية حتى الدورة التالية")
                    time.sleep(wait_seconds)
                
        except KeyboardInterrupt:
            logger.info("تم إيقاف جدول جمع البيانات")
        except Exception as e:
            logger.error(f"حدث خطأ أثناء جدول جمع البيانات: {str(e)}")
    
    def close(self):
        """إغلاق المتصفح وتنظيف الموارد"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("تم إغلاق المتصفح")
            except Exception as e:
                logger.error(f"فشل في إغلاق المتصفح: {str(e)}")
            
            self.driver = None
            self.is_logged_in = False


# مثال للاستخدام (للاختبار)
if __name__ == '__main__':
    # إنشاء آلية جمع البيانات
    collector = PocketOptionDataCollector(headless=False)
    
    try:
        # تسجيل الدخول (يدوياً)
        if collector.login():
            # جمع بيانات لأصل وإطار زمني محددين
            collector.collect_and_save_data("EUR/USD", "1m", num_candles=100)
            
            # جمع بيانات لعدة أصول
            assets = ["EUR/USD", "GBP/USD", "USD/JPY"]
            collector.collect_multiple_assets(assets, "5m", num_candles=50)
            
            # جمع بيانات لعدة أطر زمنية
            timeframes = ["1m", "5m", "15m"]
            collector.collect_multiple_timeframes("EUR/USD", timeframes, num_candles=50)
            
            # إعداد جدول لجمع البيانات (تعليق لتجنب التشغيل المستمر في الاختبار)
            # collector.setup_data_collection_schedule(["EUR/USD"], ["1m", "5m"], interval_minutes=1)
    finally:
        # إغلاق المتصفح
        collector.close()
