import React, { useState, useEffect } from 'react';

const EnhancedTradingPlatform = () => {
  const [selectedPair, setSelectedPair] = useState('EURUSD');
  const [analysisData, setAnalysisData] = useState(null);
  const [indicators, setIndicators] = useState(null);
  const [stabilityReport, setStabilityReport] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  const availablePairs = ['EURUSD', 'GBPUSD', 'USDJPY'];

  const API_BASE = 'http://localhost:5000/api';

  // تحديث البيانات
  const fetchData = async () => {
    setLoading(true);
    try {
      // اختيار الزوج
      await fetch(`${API_BASE}/pair/select`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pair: selectedPair })
      });

      // الحصول على التحليل الشامل
      const analysisResponse = await fetch(`${API_BASE}/analysis/comprehensive`);
      const analysisData = await analysisResponse.json();
      setAnalysisData(analysisData);

      // الحصول على المؤشرات
      const indicatorsResponse = await fetch(`${API_BASE}/indicators`);
      const indicatorsData = await indicatorsResponse.json();
      setIndicators(indicatorsData);

      // الحصول على تقرير الاستقرار
      const stabilityResponse = await fetch(`${API_BASE}/stability/report`);
      const stabilityData = await stabilityResponse.json();
      setStabilityReport(stabilityData);

      // الحصول على الأداء
      const performanceResponse = await fetch(`${API_BASE}/performance`);
      const performanceData = await performanceResponse.json();
      setPerformance(performanceData);

      setLastUpdate(new Date().toLocaleTimeString('ar-SA'));
    } catch (error) {
      console.error('خطأ في جلب البيانات:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // تحديث كل 30 ثانية
    return () => clearInterval(interval);
  }, [selectedPair]);

  const getSignalColor = (signalType) => {
    switch (signalType) {
      case 'buy': return 'text-green-600 bg-green-100';
      case 'sell': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'text-green-600';
    if (confidence >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4" dir="rtl">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">
                منصة التداول الذكية المحسنة
              </h1>
              <p className="text-gray-600 mt-2">
                نظام التحليل المركز مع تحسين استقرار الإشارات
              </p>
            </div>
            <div className="text-left">
              <div className="text-sm text-gray-500">آخر تحديث</div>
              <div className="text-lg font-semibold">{lastUpdate}</div>
            </div>
          </div>
        </div>

        {/* Pair Selection */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">اختيار الزوج للتحليل المركز</h2>
          <div className="flex gap-4">
            {availablePairs.map(pair => (
              <button
                key={pair}
                onClick={() => setSelectedPair(pair)}
                className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                  selectedPair === pair
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {pair}
              </button>
            ))}
          </div>
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-blue-800">
              <strong>التركيز على زوج واحد:</strong> يوفر تحليلاً أعمق وأكثر دقة مع إشارات مخصصة لخصائص الزوج المختار
            </p>
          </div>
        </div>

        {loading && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-6 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">جاري تحديث البيانات...</p>
          </div>
        )}

        {/* Main Analysis */}
        {analysisData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Signal Analysis */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold mb-4">تحليل الإشارة المحسنة</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span>نوع الإشارة:</span>
                  <span className={`px-3 py-1 rounded-full font-semibold ${getSignalColor(analysisData.signal?.signal_type)}`}>
                    {analysisData.signal?.signal_type === 'buy' ? 'شراء' : 
                     analysisData.signal?.signal_type === 'sell' ? 'بيع' : 'محايد'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>مستوى الثقة:</span>
                  <span className={`font-bold ${getConfidenceColor(analysisData.signal?.confidence || 0)}`}>
                    {(analysisData.signal?.confidence || 0).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>نقاط التأكيد:</span>
                  <span className="font-semibold">
                    {(analysisData.signal?.confirmation_score || 0).toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>النقاط الإجمالية:</span>
                  <span className="font-bold text-blue-600">
                    {(analysisData.analysis_summary?.overall_score || 0).toFixed(1)}
                  </span>
                </div>
              </div>
            </div>

            {/* Trend Analysis */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold mb-4">تحليل الاتجاه</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span>الاتجاه العام:</span>
                  <span className={`font-semibold ${
                    analysisData.analysis_summary?.trend_direction === 'bullish' ? 'text-green-600' :
                    analysisData.analysis_summary?.trend_direction === 'bearish' ? 'text-red-600' : 'text-gray-600'
                  }`}>
                    {analysisData.analysis_summary?.trend_direction === 'bullish' ? 'صاعد' :
                     analysisData.analysis_summary?.trend_direction === 'bearish' ? 'هابط' : 'محايد'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>مستوى التقلب:</span>
                  <span className="font-semibold">
                    {analysisData.analysis_summary?.volatility_level || 'متوسط'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>قوة الجلسة:</span>
                  <span className="font-semibold">
                    {((analysisData.analysis_summary?.session_strength || 0) * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>أصوات المؤشرات:</span>
                  <span className="text-sm">
                    شراء: {analysisData.analysis_summary?.indicator_votes?.buy || 0} | 
                    بيع: {analysisData.analysis_summary?.indicator_votes?.sell || 0} | 
                    محايد: {analysisData.analysis_summary?.indicator_votes?.neutral || 0}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Enhanced Indicators */}
        {indicators && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-xl font-bold mb-4">المؤشرات الفنية المحسنة (12 مؤشر)</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(indicators.indicators || {}).map(([name, data]) => (
                <div key={name} className="border rounded-lg p-4">
                  <h4 className="font-semibold mb-2 capitalize">{name.replace('_', ' ')}</h4>
                  {data.error ? (
                    <p className="text-red-500 text-sm">خطأ: {data.error}</p>
                  ) : (
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>الإشارة:</span>
                        <span className={`px-2 py-1 rounded text-xs ${getSignalColor(data.signal_type)}`}>
                          {data.signal_type === 'buy' ? 'شراء' : 
                           data.signal_type === 'sell' ? 'بيع' : 'محايد'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>القوة:</span>
                        <span className="font-semibold">{(data.signal_strength || 0).toFixed(1)}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>الجودة:</span>
                        <span className="font-semibold">{(data.quality_score || 0).toFixed(1)}</span>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Stability Report */}
        {stabilityReport && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold mb-4">تقرير الاستقرار</h3>
              {stabilityReport.stability_report?.status === 'success' ? (
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>استقرار النظام:</span>
                    <span className="font-bold text-blue-600">
                      {stabilityReport.stability_report.overall_stability?.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>استقرار الثقة:</span>
                    <span className="font-semibold">
                      {stabilityReport.stability_report.stability_metrics?.confidence_stability?.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>اتساق الاتجاه:</span>
                    <span className="font-semibold">
                      {stabilityReport.stability_report.stability_metrics?.trend_consistency?.toFixed(1)}%
                    </span>
                  </div>
                  <div className="mt-4">
                    <h4 className="font-semibold mb-2">التوصيات:</h4>
                    <ul className="text-sm space-y-1">
                      {stabilityReport.stability_report.recommendations?.map((rec, index) => (
                        <li key={index} className="text-gray-600">• {rec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">بيانات غير كافية لتقرير الاستقرار</p>
              )}
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold mb-4">حالة النظام</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span>حالة النظام:</span>
                  <span className="px-3 py-1 bg-green-100 text-green-600 rounded-full text-sm font-semibold">
                    نشط
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>نقاط الاستقرار:</span>
                  <span className="font-bold">
                    {stabilityReport.system_status?.stability_score?.toFixed(1) || '0.0'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>إشارات اليوم:</span>
                  <span className="font-semibold">
                    {stabilityReport.system_status?.session_signals || 0} / {stabilityReport.system_status?.max_session_signals || 5}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Performance Metrics */}
        {performance && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-xl font-bold mb-4">مقاييس الأداء (30 يوم)</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{performance.total_signals}</div>
                <div className="text-sm text-gray-600">إجمالي الإشارات</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{performance.success_rate?.toFixed(1)}%</div>
                <div className="text-sm text-gray-600">معدل النجاح</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">{performance.average_confidence?.toFixed(1)}%</div>
                <div className="text-sm text-gray-600">متوسط الثقة</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{performance.signals_per_day?.toFixed(1)}</div>
                <div className="text-sm text-gray-600">إشارات/يوم</div>
              </div>
            </div>
          </div>
        )}

        {/* Refresh Button */}
        <div className="text-center">
          <button
            onClick={fetchData}
            disabled={loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {loading ? 'جاري التحديث...' : 'تحديث البيانات'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedTradingPlatform;

