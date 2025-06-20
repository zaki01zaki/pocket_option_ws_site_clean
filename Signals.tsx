import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Stack,
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Button, 
  Divider, 
  Chip, 
  Tooltip, 
  CircularProgress,
  useTheme,
  IconButton,
  TextField,
  Switch,
  FormControlLabel,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Card,
  CardContent,
  CardActions,
  Slider,
  SelectChangeEvent
} from '@mui/material';
import { 
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Timeline as TimelineIcon,
  Refresh as RefreshIcon,
  Notifications as NotificationsIcon,
  NotificationsActive as NotificationsActiveIcon,
  NotificationsOff as NotificationsOffIcon,
  History as HistoryIcon
} from '@mui/icons-material';

// مكون الإشارات
const Signals: React.FC = () => {
  const theme = useTheme();
  
  // حالة المكون
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<string>('all');
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('all');
  const [selectedSignalType, setSelectedSignalType] = useState<string>('all');
  const [minConfidence, setMinConfidence] = useState<number>(60);
  
  // بيانات وهمية للإشارات
  const [signals, setSignals] = useState<any[]>([
    {
      id: 1,
      asset: 'EURUSD',
      timeframe: '15m',
      type: 'buy',
      confidence: 85,
      timestamp: new Date(Date.now() - 5 * 60000),
      indicators: {
        rsi: 'buy',
        macd: 'buy',
        ma: 'buy',
        bb: 'neutral',
        stoch: 'buy'
      },
      confirmations: 48,
      status: 'active'
    },
    {
      id: 2,
      asset: 'GBPUSD',
      timeframe: '1h',
      type: 'sell',
      confidence: 72,
      timestamp: new Date(Date.now() - 35 * 60000),
      indicators: {
        rsi: 'sell',
        macd: 'sell',
        ma: 'sell',
        bb: 'neutral',
        stoch: 'neutral'
      },
      confirmations: 39,
      status: 'active'
    },
    {
      id: 3,
      asset: 'BTCUSD',
      timeframe: '5m',
      type: 'buy',
      confidence: 65,
      timestamp: new Date(Date.now() - 120 * 60000),
      indicators: {
        rsi: 'buy',
        macd: 'neutral',
        ma: 'buy',
        bb: 'buy',
        stoch: 'neutral'
      },
      confirmations: 35,
      status: 'expired'
    },
    {
      id: 4,
      asset: 'GOLD',
      timeframe: '30m',
      type: 'sell',
      confidence: 78,
      timestamp: new Date(Date.now() - 180 * 60000),
      indicators: {
        rsi: 'sell',
        macd: 'sell',
        ma: 'sell',
        bb: 'sell',
        stoch: 'neutral'
      },
      confirmations: 42,
      status: 'completed'
    },
    {
      id: 5,
      asset: 'EURUSD',
      timeframe: '1h',
      type: 'buy',
      confidence: 92,
      timestamp: new Date(Date.now() - 240 * 60000),
      indicators: {
        rsi: 'buy',
        macd: 'buy',
        ma: 'buy',
        bb: 'buy',
        stoch: 'buy'
      },
      confirmations: 52,
      status: 'completed'
    }
  ]);
  
  // تحديث الإشارات
  const updateSignals = () => {
    setLoading(true);
    
    // محاكاة تحديث البيانات
    setTimeout(() => {
      // إضافة إشارة جديدة
      const newSignal = {
        id: signals.length + 1,
        asset: ['EURUSD', 'GBPUSD', 'BTCUSD', 'GOLD'][Math.floor(Math.random() * 4)],
        timeframe: ['5m', '15m', '30m', '1h'][Math.floor(Math.random() * 4)],
        type: Math.random() > 0.5 ? 'buy' : 'sell',
        confidence: Math.floor(Math.random() * 30) + 65,
        timestamp: new Date(),
        indicators: {
          rsi: ['buy', 'sell', 'neutral'][Math.floor(Math.random() * 3)],
          macd: ['buy', 'sell', 'neutral'][Math.floor(Math.random() * 3)],
          ma: ['buy', 'sell', 'neutral'][Math.floor(Math.random() * 3)],
          bb: ['buy', 'sell', 'neutral'][Math.floor(Math.random() * 3)],
          stoch: ['buy', 'sell', 'neutral'][Math.floor(Math.random() * 3)]
        },
        confirmations: Math.floor(Math.random() * 20) + 30,
        status: 'active'
      };
      
      setSignals([newSignal, ...signals]);
      setLoading(false);
    }, 1500);
  };
  
  // تصفية الإشارات
  const filteredSignals = signals.filter(signal => {
    if (selectedAsset !== 'all' && signal.asset !== selectedAsset) return false;
    if (selectedTimeframe !== 'all' && signal.timeframe !== selectedTimeframe) return false;
    if (selectedSignalType !== 'all' && signal.type !== selectedSignalType) return false;
    if (signal.confidence < minConfidence) return false;
    return true;
  });
  
  // تغيير الأصل المحدد
  const handleAssetChange = (event: SelectChangeEvent) => {
    setSelectedAsset(event.target.value);
  };
  
  // تغيير الإطار الزمني المحدد
  const handleTimeframeChange = (event: SelectChangeEvent) => {
    setSelectedTimeframe(event.target.value);
  };
  
  // تغيير نوع الإشارة المحدد
  const handleSignalTypeChange = (event: SelectChangeEvent) => {
    setSelectedSignalType(event.target.value);
  };
  
  // تغيير الحد الأدنى للثقة
  const handleMinConfidenceChange = (event: Event, value: number | number[]) => {
    setMinConfidence(value as number);
  };
  
  // تنسيق الوقت
  const formatTime = (date: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'الآن';
    if (diffMins < 60) return `منذ ${diffMins} دقيقة`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `منذ ${diffHours} ساعة`;
    
    const diffDays = Math.floor(diffHours / 24);
    return `منذ ${diffDays} يوم`;
  };
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          إشارات التداول
        </Typography>
        
        <Box>
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <RefreshIcon />}
            onClick={updateSignals}
            disabled={loading}
          >
            تحديث الإشارات
          </Button>
        </Box>
      </Box>
      
      {/* أدوات التصفية */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          تصفية الإشارات
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>الأصل</InputLabel>
            <Select
              value={selectedAsset}
              label="الأصل"
              onChange={handleAssetChange}
            >
              <MenuItem value="all">جميع الأصول</MenuItem>
              <MenuItem value="EURUSD">EUR/USD</MenuItem>
              <MenuItem value="GBPUSD">GBP/USD</MenuItem>
              <MenuItem value="BTCUSD">BTC/USD</MenuItem>
              <MenuItem value="GOLD">GOLD</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>الإطار الزمني</InputLabel>
            <Select
              value={selectedTimeframe}
              label="الإطار الزمني"
              onChange={handleTimeframeChange}
            >
              <MenuItem value="all">جميع الأطر الزمنية</MenuItem>
              <MenuItem value="5m">5 دقائق</MenuItem>
              <MenuItem value="15m">15 دقيقة</MenuItem>
              <MenuItem value="30m">30 دقيقة</MenuItem>
              <MenuItem value="1h">1 ساعة</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>نوع الإشارة</InputLabel>
            <Select
              value={selectedSignalType}
              label="نوع الإشارة"
              onChange={handleSignalTypeChange}
            >
              <MenuItem value="all">جميع الإشارات</MenuItem>
              <MenuItem value="buy">إشارات شراء</MenuItem>
              <MenuItem value="sell">إشارات بيع</MenuItem>
            </Select>
          </FormControl>
        </Box>
        
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            الحد الأدنى لنسبة الثقة: {minConfidence}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={minConfidence}
              onChange={handleMinConfidenceChange}
              min={50}
              max={95}
              step={5}
              marks={[
                { value: 50, label: '50%' },
                { value: 70, label: '70%' },
                { value: 95, label: '95%' }
              ]}
            />
          </Box>
        </Box>
      </Paper>
      
      {/* قائمة الإشارات */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          الإشارات النشطة ({filteredSignals.filter(s => s.status === 'active').length})
        </Typography>
        
        {filteredSignals.filter(s => s.status === 'active').length === 0 ? (
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="body1">
              لا توجد إشارات نشطة تطابق معايير التصفية
            </Typography>
          </Paper>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {filteredSignals
              .filter(s => s.status === 'active')
              .map(signal => (
                <Paper key={signal.id} sx={{ 
                  p: 2, 
                  borderLeft: 6, 
                  borderColor: signal.type === 'buy' ? 'success.main' : 'error.main' 
                }}>
                  <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
                    <Box sx={{ flex: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                        <Typography variant="h6" color={signal.type === 'buy' ? 'success.main' : 'error.main'}>
                          {signal.type === 'buy' ? 'إشارة شراء' : 'إشارة بيع'} - {signal.asset}
                        </Typography>
                        
                        <Chip 
                          label={`${signal.confidence}%`} 
                          color={
                            signal.confidence >= 80 ? 'success' : 
                            signal.confidence >= 65 ? 'primary' : 
                            'warning'
                          } 
                        />
                      </Box>
                      
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                          الإطار الزمني:
                        </Typography>
                        <Typography variant="body2" fontWeight="bold">
                          {signal.timeframe}
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mx: 2 }}>
                          |
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                          التأكيدات:
                        </Typography>
                        <Typography variant="body2" fontWeight="bold">
                          {signal.confirmations}/60
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mx: 2 }}>
                          |
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                          الوقت:
                        </Typography>
                        <Typography variant="body2" fontWeight="bold">
                          {formatTime(signal.timestamp)}
                        </Typography>
                      </Box>
                      
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        <Tooltip title="مؤشر القوة النسبية">
                          <Chip 
                            label="RSI" 
                            size="small"
                            color={
                              signal.indicators.rsi === 'buy' ? 'success' : 
                              signal.indicators.rsi === 'sell' ? 'error' : 
                              'default'
                            }
                            variant={signal.indicators.rsi === 'neutral' ? 'outlined' : 'filled'}
                          />
                        </Tooltip>
                        
                        <Tooltip title="مؤشر MACD">
                          <Chip 
                            label="MACD" 
                            size="small"
                            color={
                              signal.indicators.macd === 'buy' ? 'success' : 
                              signal.indicators.macd === 'sell' ? 'error' : 
                              'default'
                            }
                            variant={signal.indicators.macd === 'neutral' ? 'outlined' : 'filled'}
                          />
                        </Tooltip>
                        
                        <Tooltip title="المتوسطات المتحركة">
                          <Chip 
                            label="MA" 
                            size="small"
                            color={
                              signal.indicators.ma === 'buy' ? 'success' : 
                              signal.indicators.ma === 'sell' ? 'error' : 
                              'default'
                            }
                            variant={signal.indicators.ma === 'neutral' ? 'outlined' : 'filled'}
                          />
                        </Tooltip>
                        
                        <Tooltip title="بولينجر باندز">
                          <Chip 
                            label="BB" 
                            size="small"
                            color={
                              signal.indicators.bb === 'buy' ? 'success' : 
                              signal.indicators.bb === 'sell' ? 'error' : 
                              'default'
                            }
                            variant={signal.indicators.bb === 'neutral' ? 'outlined' : 'filled'}
                          />
                        </Tooltip>
                        
                        <Tooltip title="ستوكاستيك">
                          <Chip 
                            label="Stoch" 
                            size="small"
                            color={
                              signal.indicators.stoch === 'buy' ? 'success' : 
                              signal.indicators.stoch === 'sell' ? 'error' : 
                              'default'
                            }
                            variant={signal.indicators.stoch === 'neutral' ? 'outlined' : 'filled'}
                          />
                        </Tooltip>
                      </Box>
                    </Box>
                    
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Button 
                        variant="outlined" 
                        color="primary" 
                        size="small"
                        startIcon={<NotificationsIcon />}
                      >
                        تنبيه
                      </Button>
                      
                      <Button 
                        variant="outlined" 
                        color="secondary" 
                        size="small"
                        startIcon={<HistoryIcon />}
                      >
                        التفاصيل
                      </Button>
                    </Box>
                  </Box>
                </Paper>
              ))}
          </Box>
        )}
      </Box>
      
      {/* سجل الإشارات */}
      <Box>
        <Typography variant="h6" gutterBottom>
          سجل الإشارات ({filteredSignals.filter(s => s.status !== 'active').length})
        </Typography>
        
        {filteredSignals.filter(s => s.status !== 'active').length === 0 ? (
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="body1">
              لا توجد إشارات سابقة تطابق معايير التصفية
            </Typography>
          </Paper>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {filteredSignals
              .filter(s => s.status !== 'active')
              .map(signal => (
                <Paper key={signal.id} sx={{ 
                  p: 2, 
                  borderLeft: 6, 
                  borderColor: signal.type === 'buy' ? 'success.main' : 'error.main',
                  opacity: 0.7
                }}>
                  <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
                    <Box sx={{ flex: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                        <Typography variant="h6" color={signal.type === 'buy' ? 'success.main' : 'error.main'}>
                          {signal.type === 'buy' ? 'إشارة شراء' : 'إشارة بيع'} - {signal.asset}
                        </Typography>
                        
                        <Chip 
                          label={signal.status === 'completed' ? 'مكتملة' : 'منتهية'} 
                          color={signal.status === 'completed' ? 'success' : 'default'} 
                          variant={signal.status === 'completed' ? 'filled' : 'outlined'}
                        />
                      </Box>
                      
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                          الإطار الزمني:
                        </Typography>
                        <Typography variant="body2" fontWeight="bold">
                          {signal.timeframe}
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mx: 2 }}>
                          |
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                          الثقة:
                        </Typography>
                        <Typography variant="body2" fontWeight="bold">
                          {signal.confidence}%
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mx: 2 }}>
                          |
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                          الوقت:
                        </Typography>
                        <Typography variant="body2" fontWeight="bold">
                          {formatTime(signal.timestamp)}
                        </Typography>
                      </Box>
                    </Box>
                    
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Button 
                        variant="outlined" 
                        color="secondary" 
                        size="small"
                        startIcon={<HistoryIcon />}
                      >
                        التفاصيل
                      </Button>
                    </Box>
                  </Box>
                </Paper>
              ))}
          </Box>
        )}
      </Box>
      
      {/* أزرار التحكم */}
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Button 
          variant="outlined" 
          color="primary" 
          startIcon={<NotificationsActiveIcon />}
        >
          تفعيل جميع التنبيهات
        </Button>
        
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <RefreshIcon />}
          onClick={updateSignals}
          disabled={loading}
        >
          تحديث الإشارات
        </Button>
      </Box>
    </Box>
  );
};

export default Signals;
