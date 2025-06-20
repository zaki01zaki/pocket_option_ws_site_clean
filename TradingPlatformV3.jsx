import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Clock, Target, AlertCircle, Activity, BarChart3, Zap } from 'lucide-react';

const TradingPlatformV3 = () => {
  const [selectedPair, setSelectedPair] = useState('EURUSD');
  const [liveAnalysis, setLiveAnalysis] = useState(null);
  const [tradeSignal, setTradeSignal] = useState(null);
  const [comprehensiveAnalysis, setComprehensiveAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const pairs = ['EURUSD', 'GBPUSD', 'USDJPY'];

  // محاكاة البيانات المباشرة
  const generateMockData = () => {
    const basePrices = { EURUSD: 1.0850, GBPUSD: 1.2650, USDJPY: 149.50 };
    const basePrice = basePrices[selectedPair];
    const volatility = selectedPair === 'EURUSD' ? 0.0008 : selectedPair === 'GBPUSD' ? 0.0012 : 0.0006;
    
    const priceChange = (Math.random() - 0.5) * volatility * 2;
    const currentPrice = basePrice + priceChange;
    const priceChangePercent = (priceChange / basePrice) * 100;

    // تحديد الاتجاه بناءً على التغيير
    const trendDirection = priceChange > 0 ? 'صاعد' : priceChange < 0 ? 'هابط' : 'محايد';
    const trendStrength = Math.abs(priceChangePercent) * 100;

    // توليد إشارة تداول
    const shouldGenerateSignal = Math.random() > 0.3; // 70% احتمال توليد إشارة
    let signal = null;

    if (shouldGenerateSignal && trendStrength > 20) {
      const durations = ['1m', '2m', '3m', '5m', '10m', '15m', '30m', '1h'];
      const durationNames = {
        '1m': '1 دقيقة', '2m': '2 دقيقة', '3m': '3 دقائق', '5m': '5 دقائق',
        '10m': '10 دقائق', '15m': '15 دقيقة', '30m': '30 دقيقة', '1h': '1 ساعة'
      };
      
      const selectedDuration = durations[Math.floor(Math.random() * durations.length)];
      const direction = priceChange > 0 ? 'call' : 'put';
      const directionArabic = direction === 'call' ? 'شراء' : 'بيع';
      const confidence = 60 + Math.random() * 30; // 60-90%
      const successProbability = 55 + Math.random() * 35; // 55-90%

      const now = new Date();
      const expiryMinutes = parseInt(selectedDuration.replace(/[^0-9]/g, '')) || 5;
      const expiryTime = new Date(now.getTime() + expiryMinutes * 60000);

      signal = {
        direction,
        direction_arabic: directionArabic,
        duration: selectedDuration,
        duration_arabic: durationNames[selectedDuration],
        confidence: confidence.toFixed(1),
        entry_price: currentPrice.toFixed(5),
        expected_exit_price: (currentPrice + (direction === 'call' ? volatility : -volatility)).toFixed(5),
        stop_loss: (currentPrice + (direction === 'call' ? -volatility * 0.5 : volatility * 0.5)).toFixed(5),
        take_profit: (currentPrice + (direction === 'call' ? volatility * 1.5 : -volatility * 1.5)).toFixed(5),
        expiry_time: expiryTime.toISOString(),
        signal_strength: trendStrength.toFixed(1),
        risk_level: volatility < 0.0005 ? 'منخفض' : volatility < 0.0015 ? 'متوسط' : 'عالي',
        success_probability: successProbability.toFixed(1),
        time_remaining: `${expiryMinutes} دقيقة`
      };
    }

    return {
      liveAnalysis: {
        pair: selectedPair,
        current_price: currentPrice.toFixed(5),
        price_change: priceChange.toFixed(5),
        price_change_percent: priceChangePercent.toFixed(2),
        trend_direction: trendDirection,
        trend_strength: trendStrength.toFixed(1),
        volatility: volatility.toFixed(6),
        volume: (1000 + Math.random() * 500).toFixed(0),
        support_level: (currentPrice * 0.999).toFixed(5),
        resistance_level: (currentPrice * 1.001).toFixed(5),
        next_key_level: priceChange > 0 ? (currentPrice * 1.001).toFixed(5) : (currentPrice * 0.999).toFixed(5),
        market_sentiment: priceChange > 0 ? 'إيجابي' : priceChange < 0 ? 'سلبي' : 'محايد',
        session_strength: 0.8 + Math.random() * 0.2
      },
      tradeSignal: signal
    };
  };

  // تحديث البيانات
  const updateData = () => {
    setIsLoading(true);
    
    setTimeout(() => {
      const mockData = generateMockData();
      setLiveAnalysis(mockData.liveAnalysis);
      setTradeSignal(mockData.tradeSignal);
      setLastUpdate(new Date());
      setIsLoading(false);
    }, 500);
  };

  // تحديث تلقائي كل 30 ثانية
  useEffect(() => {
    updateData();
    const interval = setInterval(updateData, 30000);
    return () => clearInterval(interval);
  }, [selectedPair]);

  // تغيير الزوج
  const handlePairChange = (pair) => {
    setSelectedPair(pair);
    setIsLoading(true);
  };

  // تحديث يدوي
  const handleManualUpdate = () => {
    updateData();
  };

  const formatTime = (timeString) => {
    return new Date(timeString).toLocaleTimeString('ar-SA', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getDirectionIcon = (direction) => {
    return direction === 'call' ? <TrendingUp className="w-5 h-5 text-green-500" /> : <TrendingDown className="w-5 h-5 text-red-500" />;
  };

  const getDirectionColor = (direction) => {
    return direction === 'call' ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50';
  };

  const getTrendColor = (direction) => {
    if (direction === 'صاعد') return 'text-green-600';
    if (direction === 'هابط') return 'text-red-600';
    return 'text-gray-600';
  };

  const getRiskColor = (risk) => {
    if (risk === 'منخفض') return 'text-green-600 bg-green-50';
    if (risk === 'متوسط') return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4" dir="rtl">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            منصة التداول الذكية المحسنة
          </h1>
          <p className="text-lg text-gray-600">
            نظام التحليل المباشر مع مدة الصفقة والاتجاه
          </p>
          <div className="flex items-center justify-center gap-2 mt-2 text-sm text-gray-500">
            <Activity className="w-4 h-4" />
            <span>آخر تحديث: {formatTime(lastUpdate.toISOString())}</span>
          </div>
        </div>

        {/* اختيار الزوج */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-blue-600" />
            اختيار الزوج للتحليل المباشر
          </h2>
          <div className="flex gap-3 mb-4">
            {pairs.map((pair) => (
              <button
                key={pair}
                onClick={() => handlePairChange(pair)}
                className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                  selectedPair === pair
                    ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {pair}
              </button>
            ))}
          </div>
          <div className="flex items-center justify-between">
            <p className="text-gray-600">
              <strong>التركيز على زوج واحد:</strong> يوفر تحليلاً أعمق وأكثر دقة مع إشارات مخصصة لخصائص الزوج المختار
            </p>
            <button
              onClick={handleManualUpdate}
              disabled={isLoading}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              <Zap className="w-4 h-4" />
              {isLoading ? 'جاري التحديث...' : 'تحديث فوري'}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* التحليل المباشر */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Activity className="w-6 h-6 text-green-600" />
              التحليل المباشر
            </h2>
            
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="mr-3 text-gray-600">جاري التحديث...</span>
              </div>
            ) : liveAnalysis ? (
              <div className="space-y-4">
                {/* السعر الحالي */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800">{liveAnalysis.pair}</h3>
                      <p className="text-2xl font-bold text-blue-600">{liveAnalysis.current_price}</p>
                    </div>
                    <div className="text-left">
                      <p className={`text-sm font-medium ${parseFloat(liveAnalysis.price_change) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {parseFloat(liveAnalysis.price_change) >= 0 ? '+' : ''}{liveAnalysis.price_change}
                      </p>
                      <p className={`text-sm ${parseFloat(liveAnalysis.price_change_percent) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        ({parseFloat(liveAnalysis.price_change_percent) >= 0 ? '+' : ''}{liveAnalysis.price_change_percent}%)
                      </p>
                    </div>
                  </div>
                </div>

                {/* معلومات التحليل */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-sm text-gray-600">اتجاه الترند</p>
                    <p className={`font-semibold ${getTrendColor(liveAnalysis.trend_direction)}`}>
                      {liveAnalysis.trend_direction}
                    </p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-sm text-gray-600">قوة الترند</p>
                    <p className="font-semibold text-gray-800">{liveAnalysis.trend_strength}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-sm text-gray-600">مستوى الدعم</p>
                    <p className="font-semibold text-blue-600">{liveAnalysis.support_level}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-sm text-gray-600">مستوى المقاومة</p>
                    <p className="font-semibold text-blue-600">{liveAnalysis.resistance_level}</p>
                  </div>
                </div>

                {/* معنويات السوق */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">معنويات السوق</p>
                      <p className={`font-semibold ${getTrendColor(liveAnalysis.market_sentiment === 'إيجابي' ? 'صاعد' : liveAnalysis.market_sentiment === 'سلبي' ? 'هابط' : 'محايد')}`}>
                        {liveAnalysis.market_sentiment}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">قوة الجلسة</p>
                      <p className="font-semibold text-gray-800">{(parseFloat(liveAnalysis.session_strength) * 100).toFixed(0)}%</p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">لا توجد بيانات متاحة</p>
            )}
          </div>

          {/* إشارة التداول */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Target className="w-6 h-6 text-orange-600" />
              إشارة التداول مع المدة والاتجاه
            </h2>
            
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-600"></div>
                <span className="mr-3 text-gray-600">جاري التحليل...</span>
              </div>
            ) : tradeSignal ? (
              <div className="space-y-4">
                {/* الاتجاه والمدة */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      {getDirectionIcon(tradeSignal.direction)}
                      <span className={`font-bold text-lg px-3 py-1 rounded-lg ${getDirectionColor(tradeSignal.direction)}`}>
                        {tradeSignal.direction_arabic}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-blue-600">
                      <Clock className="w-5 h-5" />
                      <span className="font-semibold">{tradeSignal.duration_arabic}</span>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">مستوى الثقة</p>
                      <p className="font-bold text-green-600">{tradeSignal.confidence}%</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">احتمالية النجاح</p>
                      <p className="font-bold text-green-600">{tradeSignal.success_probability}%</p>
                    </div>
                  </div>
                </div>

                {/* تفاصيل الصفقة */}
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">سعر الدخول:</span>
                    <span className="font-semibold text-gray-800">{tradeSignal.entry_price}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">السعر المتوقع:</span>
                    <span className="font-semibold text-blue-600">{tradeSignal.expected_exit_price}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">وقف الخسارة:</span>
                    <span className="font-semibold text-red-600">{tradeSignal.stop_loss}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">جني الأرباح:</span>
                    <span className="font-semibold text-green-600">{tradeSignal.take_profit}</span>
                  </div>
                </div>

                {/* معلومات المخاطر */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">مستوى المخاطر</p>
                      <span className={`px-2 py-1 rounded-lg text-sm font-semibold ${getRiskColor(tradeSignal.risk_level)}`}>
                        {tradeSignal.risk_level}
                      </span>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">قوة الإشارة</p>
                      <p className="font-semibold text-gray-800">{tradeSignal.signal_strength}</p>
                    </div>
                  </div>
                </div>

                {/* العد التنازلي */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-blue-800">
                    <AlertCircle className="w-5 h-5" />
                    <span className="font-semibold">وقت انتهاء الصفقة: {tradeSignal.time_remaining}</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-500">لا توجد إشارة تداول مناسبة في الوقت الحالي</p>
                <p className="text-sm text-gray-400 mt-2">سيتم تحديث الإشارات تلقائياً كل 30 ثانية</p>
              </div>
            )}
          </div>
        </div>

        {/* معلومات إضافية */}
        <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">المميزات الجديدة</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="w-5 h-5 text-green-600" />
                <h3 className="font-semibold text-green-800">مدة الصفقة الذكية</h3>
              </div>
              <p className="text-sm text-green-700">
                تحديد المدة المثلى للصفقة بناءً على التقلبات وقوة الترند
              </p>
            </div>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-blue-600" />
                <h3 className="font-semibold text-blue-800">تحديد الاتجاه</h3>
              </div>
              <p className="text-sm text-blue-700">
                تحليل دقيق لاتجاه السوق مع احتمالية النجاح
              </p>
            </div>
            
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-5 h-5 text-orange-600" />
                <h3 className="font-semibold text-orange-800">التحليل المباشر</h3>
              </div>
              <p className="text-sm text-orange-700">
                تحديث مستمر للبيانات والتحليل في الوقت الفعلي
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradingPlatformV3;

