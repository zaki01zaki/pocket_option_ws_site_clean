import React, { useState, useEffect } from 'react';

const AdvancedDataCollection = () => {
  const [dataStatus, setDataStatus] = useState({
    websocket: { active: false, last_update: null, error: null },
    apis: { active: false, last_update: null, error: null },
    simulator: { active: true, last_update: null, error: null }
  });
  
  const [latestPrices, setLatestPrices] = useState({
    websocket: [],
    apis: [],
    simulated: []
  });
  
  const [selectedAsset, setSelectedAsset] = useState('EURUSD');
  const [priceComparison, setPriceComparison] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // جلب حالة جمع البيانات
  const fetchDataStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/data-collection/status');
      const result = await response.json();
      if (result.status === 'success') {
        setDataStatus(result.data);
      }
    } catch (error) {
      console.error('خطأ في جلب حالة البيانات:', error);
    }
  };

  // جلب أحدث الأسعار
  const fetchLatestPrices = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/prices/latest');
      const result = await response.json();
      if (result.status === 'success') {
        setLatestPrices(result.data);
      }
    } catch (error) {
      console.error('خطأ في جلب الأسعار:', error);
    }
  };

  // مقارنة الأسعار
  const comparePrices = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/prices/compare?asset=${selectedAsset}`);
      const result = await response.json();
      if (result.status === 'success') {
        setPriceComparison(result.data);
      }
    } catch (error) {
      console.error('خطأ في مقارنة الأسعار:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // بدء جمع البيانات
  const startDataCollection = async (method) => {
    try {
      const response = await fetch('http://localhost:5000/api/data-collection/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ method })
      });
      const result = await response.json();
      if (result.status === 'success') {
        setDataStatus(result.data);
      }
    } catch (error) {
      console.error('خطأ في بدء جمع البيانات:', error);
    }
  };

  // إيقاف جمع البيانات
  const stopDataCollection = async (method) => {
    try {
      const response = await fetch('http://localhost:5000/api/data-collection/stop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ method })
      });
      const result = await response.json();
      if (result.status === 'success') {
        setDataStatus(result.data);
      }
    } catch (error) {
      console.error('خطأ في إيقاف جمع البيانات:', error);
    }
  };

  // تحسين المحاكاة
  const optimizeSimulation = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/simulation/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ asset: selectedAsset })
      });
      const result = await response.json();
      alert(result.message);
    } catch (error) {
      console.error('خطأ في تحسين المحاكاة:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDataStatus();
    fetchLatestPrices();
    
    // تحديث دوري كل 30 ثانية
    const interval = setInterval(() => {
      fetchDataStatus();
      fetchLatestPrices();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'غير متاح';
    return new Date(timestamp).toLocaleString('ar-SA');
  };

  const getStatusColor = (active, error) => {
    if (error) return 'text-red-600';
    if (active) return 'text-green-600';
    return 'text-gray-600';
  };

  const getStatusText = (active, error) => {
    if (error) return 'خطأ';
    if (active) return 'نشط';
    return 'متوقف';
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6" dir="rtl">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          نظام جمع البيانات المتقدم من Pocket Option
        </h1>

        {/* حالة الخدمات */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">WebSocket Scraper</h3>
            <div className={`text-sm ${getStatusColor(dataStatus.websocket.active, dataStatus.websocket.error)}`}>
              الحالة: {getStatusText(dataStatus.websocket.active, dataStatus.websocket.error)}
            </div>
            <div className="text-sm text-gray-600 mt-2">
              آخر تحديث: {formatTimestamp(dataStatus.websocket.last_update)}
            </div>
            {dataStatus.websocket.error && (
              <div className="text-sm text-red-600 mt-2">
                خطأ: {dataStatus.websocket.error}
              </div>
            )}
            <div className="mt-4 space-x-2 space-x-reverse">
              <button
                onClick={() => startDataCollection('websocket')}
                className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700"
                disabled={dataStatus.websocket.active}
              >
                تشغيل
              </button>
              <button
                onClick={() => stopDataCollection('websocket')}
                className="bg-red-600 text-white px-4 py-2 rounded text-sm hover:bg-red-700"
                disabled={!dataStatus.websocket.active}
              >
                إيقاف
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">APIs البديلة</h3>
            <div className={`text-sm ${getStatusColor(dataStatus.apis.active, dataStatus.apis.error)}`}>
              الحالة: {getStatusText(dataStatus.apis.active, dataStatus.apis.error)}
            </div>
            <div className="text-sm text-gray-600 mt-2">
              آخر تحديث: {formatTimestamp(dataStatus.apis.last_update)}
            </div>
            {dataStatus.apis.error && (
              <div className="text-sm text-red-600 mt-2">
                خطأ: {dataStatus.apis.error}
              </div>
            )}
            <div className="mt-4 space-x-2 space-x-reverse">
              <button
                onClick={() => startDataCollection('apis')}
                className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700"
                disabled={dataStatus.apis.active}
              >
                تشغيل
              </button>
              <button
                onClick={() => stopDataCollection('apis')}
                className="bg-red-600 text-white px-4 py-2 rounded text-sm hover:bg-red-700"
                disabled={!dataStatus.apis.active}
              >
                إيقاف
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">المحاكاة الذكية</h3>
            <div className={`text-sm ${getStatusColor(dataStatus.simulator.active, dataStatus.simulator.error)}`}>
              الحالة: {getStatusText(dataStatus.simulator.active, dataStatus.simulator.error)}
            </div>
            <div className="text-sm text-gray-600 mt-2">
              آخر تحديث: {formatTimestamp(dataStatus.simulator.last_update)}
            </div>
            <div className="mt-4 space-x-2 space-x-reverse">
              <button
                onClick={optimizeSimulation}
                className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700"
                disabled={isLoading}
              >
                تحسين النموذج
              </button>
            </div>
          </div>
        </div>

        {/* مقارنة الأسعار */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-lg font-semibold mb-4">مقارنة الأسعار</h3>
          
          <div className="flex items-center gap-4 mb-4">
            <select
              value={selectedAsset}
              onChange={(e) => setSelectedAsset(e.target.value)}
              className="border border-gray-300 rounded px-3 py-2"
            >
              <option value="EURUSD">EUR/USD</option>
              <option value="GBPUSD">GBP/USD</option>
              <option value="USDJPY">USD/JPY</option>
              <option value="BTCUSD">BTC/USD</option>
              <option value="ETHUSD">ETH/USD</option>
            </select>
            
            <button
              onClick={comparePrices}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              disabled={isLoading}
            >
              {isLoading ? 'جاري المقارنة...' : 'مقارنة الأسعار'}
            </button>
          </div>

          {priceComparison && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold mb-2">أفضل سعر من APIs</h4>
                {priceComparison.best_api_price ? (
                  <div className="bg-gray-50 p-4 rounded">
                    <div>المصدر: {priceComparison.best_api_price.source}</div>
                    <div>السعر: {priceComparison.best_api_price.price}</div>
                    <div>الوقت: {formatTimestamp(priceComparison.best_api_price.timestamp)}</div>
                  </div>
                ) : (
                  <div className="text-gray-500">لا توجد بيانات متاحة</div>
                )}
              </div>

              <div>
                <h4 className="font-semibold mb-2">السعر المحاكى</h4>
                <div className="bg-gray-50 p-4 rounded">
                  <div>السعر الحقيقي: {priceComparison.simulated_price.real_price}</div>
                  <div>السعر المحاكى: {priceComparison.simulated_price.simulated_price.toFixed(4)}</div>
                  <div>نقاط الجودة: {priceComparison.simulated_price.quality_score}%</div>
                  <div>الجلسة: {priceComparison.simulated_price.session}</div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* الأسعار المباشرة */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* أسعار WebSocket */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">أسعار WebSocket</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {latestPrices.websocket && latestPrices.websocket.length > 0 ? (
                latestPrices.websocket.slice(0, 5).map((price, index) => (
                  <div key={index} className="border-b pb-2">
                    <div className="font-medium">{price.asset_name}</div>
                    <div className="text-sm text-gray-600">
                      {price.price} - جودة: {price.quality_score}%
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-gray-500">لا توجد بيانات</div>
              )}
            </div>
          </div>

          {/* أسعار APIs */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">أسعار APIs</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {latestPrices.apis && latestPrices.apis.length > 0 ? (
                latestPrices.apis.slice(0, 5).map((price, index) => (
                  <div key={index} className="border-b pb-2">
                    <div className="font-medium">{price.asset_name}</div>
                    <div className="text-sm text-gray-600">
                      {price.price} - مصدر: {price.source}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-gray-500">لا توجد بيانات</div>
              )}
            </div>
          </div>

          {/* أسعار محاكاة */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">أسعار محاكاة</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {latestPrices.simulated && latestPrices.simulated.length > 0 ? (
                latestPrices.simulated.map((price, index) => (
                  <div key={index} className="border-b pb-2">
                    <div className="font-medium">{price.asset_name}</div>
                    <div className="text-sm text-gray-600">
                      {price.simulated_price.toFixed(4)} - جودة: {price.quality_score}%
                    </div>
                    <div className="text-xs text-gray-500">
                      {price.is_otc ? 'OTC' : 'عادي'} - {price.session}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-gray-500">لا توجد بيانات</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedDataCollection;

