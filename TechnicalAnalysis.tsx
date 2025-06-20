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
  ListItemIcon
} from '@mui/material';
import { 
  ShowChart as ShowChartIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Timeline as TimelineIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';

// مكون التحليل الفني
const TechnicalAnalysis: React.FC = () => {
  const theme = useTheme();
  
  // حالة المكون
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<string>('EURUSD');
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('15m');
  
  // بيانات وهمية للمؤشرات
  const [indicators, setIndicators] = useState({
    rsi: {
      value: 58.42,
      trend: 'neutral',
      signal: 'hold'
    },
    macd: {
      value: 0.0023,
      trend: 'bullish',
      signal: 'buy'
    },
    ma: {
      fast: 1.1234,
      slow: 1.1220,
      trend: 'bullish',
      signal: 'buy'
    },
    bb: {
      upper: 1.1280,
      middle: 1.1240,
      lower: 1.1200,
      width: 0.0080,
      trend: 'neutral',
      signal: 'hold'
    },
    stoch: {
      k: 75.32,
      d: 68.45,
      trend: 'bullish',
      signal: 'buy'
    }
  });
  
  // بيانات وهمية للتأكيدات
  const [confirmations, setConfirmations] = useState({
    bullish: 42,
    bearish: 18,
    total: 60,
    confidence: 70
  });
  
  // قائمة وهمية للتأكيدات
  const dummyConfirmations = [
    { name: 'RSI تصاعدي', active: true },
    { name: 'MACD تصاعدي', active: true },
    { name: 'تقاطع المتوسطات تصاعدي', active: true },
    { name: 'ستوكاستيك تصاعدي', active: true },
    { name: 'بولينجر باندز تصاعدي', active: false },
    { name: 'حجم التداول مرتفع', active: true },
    { name: 'نموذج شمعة إيجابي', active: true },
    { name: 'دعم قوي', active: true },
    { name: 'مستويات فيبوناتشي', active: false },
    { name: 'مؤشر ADX مرتفع', active: true },
    { name: 'مؤشر OBV تصاعدي', active: true },
    { name: 'تباعد إيجابي', active: false }
  ];
  
  // تحديث التحليل الفني
  const updateAnalysis = () => {
    setLoading(true);
    
    // محاكاة تحديث البيانات
    setTimeout(() => {
      setIndicators({
        rsi: {
          value: 58.42 + (Math.random() * 10 - 5),
          trend: Math.random() > 0.5 ? 'bullish' : 'neutral',
          signal: Math.random() > 0.5 ? 'buy' : 'hold'
        },
        macd: {
          value: 0.0023 + (Math.random() * 0.01 - 0.005),
          trend: Math.random() > 0.3 ? 'bullish' : 'bearish',
          signal: Math.random() > 0.3 ? 'buy' : 'sell'
        },
        ma: {
          fast: 1.1234 + (Math.random() * 0.01 - 0.005),
          slow: 1.1220 + (Math.random() * 0.01 - 0.005),
          trend: Math.random() > 0.4 ? 'bullish' : 'bearish',
          signal: Math.random() > 0.4 ? 'buy' : 'sell'
        },
        bb: {
          upper: 1.1280 + (Math.random() * 0.01 - 0.005),
          middle: 1.1240 + (Math.random() * 0.01 - 0.005),
          lower: 1.1200 + (Math.random() * 0.01 - 0.005),
          width: 0.0080 + (Math.random() * 0.002 - 0.001),
          trend: Math.random() > 0.5 ? 'neutral' : 'bullish',
          signal: Math.random() > 0.5 ? 'hold' : 'buy'
        },
        stoch: {
          k: 75.32 + (Math.random() * 10 - 5),
          d: 68.45 + (Math.random() * 10 - 5),
          trend: Math.random() > 0.4 ? 'bullish' : 'bearish',
          signal: Math.random() > 0.4 ? 'buy' : 'sell'
        }
      });
      
      const bullishCount = Math.floor(Math.random() * 20) + 30;
      const bearishCount = 60 - bullishCount;
      
      setConfirmations({
        bullish: bullishCount,
        bearish: bearishCount,
        total: 60,
        confidence: Math.round((bullishCount / 60) * 100)
      });
      
      setLoading(false);
    }, 1500);
  };
  
  // تغيير الأصل المحدد
  const handleAssetChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedAsset(event.target.value as string);
    updateAnalysis();
  };
  
  // تغيير الإطار الزمني المحدد
  const handleTimeframeChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedTimeframe(event.target.value as string);
    updateAnalysis();
  };
  
  // تحديث التحليل تلقائياً عند تحميل المكون
  useEffect(() => {
    updateAnalysis();
  }, []);
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          التحليل الفني
        </Typography>
        
        <Box>
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <RefreshIcon />}
            onClick={updateAnalysis}
            disabled={loading}
          >
            تحديث التحليل
          </Button>
        </Box>
      </Box>
      
      {/* أدوات التحكم */}
      <Paper sx={{ p: 2, mb: 3, display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2 }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>الأصل</InputLabel>
          <Select
            value={selectedAsset}
            label="الأصل"
            onChange={handleAssetChange}
          >
            <MenuItem value="EURUSD">EUR/USD</MenuItem>
            <MenuItem value="GBPUSD">GBP/USD</MenuItem>
            <MenuItem value="USDJPY">USD/JPY</MenuItem>
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
            <MenuItem value="1m">1 دقيقة</MenuItem>
            <MenuItem value="5m">5 دقائق</MenuItem>
            <MenuItem value="15m">15 دقيقة</MenuItem>
            <MenuItem value="30m">30 دقيقة</MenuItem>
            <MenuItem value="1h">1 ساعة</MenuItem>
            <MenuItem value="4h">4 ساعات</MenuItem>
            <MenuItem value="1d">يومي</MenuItem>
          </Select>
        </FormControl>
        
        <Box sx={{ display: 'flex', alignItems: 'center', ml: 'auto' }}>
          <Typography variant="body1" sx={{ mr: 1 }}>
            آخر تحديث:
          </Typography>
          <Typography variant="body1" fontWeight="bold">
            {new Date().toLocaleTimeString()}
          </Typography>
        </Box>
      </Paper>
      
      {/* ملخص التحليل */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          ملخص التحليل
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" gutterBottom>
              الاتجاه العام
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              {confirmations.confidence > 60 ? (
                <TrendingUpIcon sx={{ fontSize: 40, color: 'success.main', mr: 1 }} />
              ) : confirmations.confidence < 40 ? (
                <TrendingDownIcon sx={{ fontSize: 40, color: 'error.main', mr: 1 }} />
              ) : (
                <TimelineIcon sx={{ fontSize: 40, color: 'warning.main', mr: 1 }} />
              )}
              
              <Typography variant="h5" fontWeight="bold" color={
                confirmations.confidence > 60 ? 'success.main' : 
                confirmations.confidence < 40 ? 'error.main' : 
                'warning.main'
              }>
                {confirmations.confidence > 60 ? 'صعودي' : 
                 confirmations.confidence < 40 ? 'هبوطي' : 
                 'محايد'}
              </Typography>
            </Box>
            
            <Typography variant="subtitle1" gutterBottom>
              نسبة الثقة
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ 
                width: '100%', 
                height: 20, 
                bgcolor: 'grey.300', 
                borderRadius: 1, 
                mr: 1,
                overflow: 'hidden'
              }}>
                <Box sx={{ 
                  width: `${confirmations.confidence}%`, 
                  height: '100%', 
                  bgcolor: confirmations.confidence > 60 ? 'success.main' : 
                          confirmations.confidence < 40 ? 'error.main' : 
                          'warning.main',
                  transition: 'width 0.5s ease-in-out'
                }} />
              </Box>
              
              <Typography variant="h6" fontWeight="bold">
                {confirmations.confidence}%
              </Typography>
            </Box>
            
            <Typography variant="subtitle1" gutterBottom>
              التأكيدات
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Box sx={{ flex: 1, display: 'flex', alignItems: 'center' }}>
                <TrendingUpIcon sx={{ color: 'success.main', mr: 0.5 }} />
                <Typography variant="body1" sx={{ mr: 1 }}>
                  صعودي:
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {confirmations.bullish}
                </Typography>
              </Box>
              
              <Box sx={{ flex: 1, display: 'flex', alignItems: 'center' }}>
                <TrendingDownIcon sx={{ color: 'error.main', mr: 0.5 }} />
                <Typography variant="body1" sx={{ mr: 1 }}>
                  هبوطي:
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {confirmations.bearish}
                </Typography>
              </Box>
            </Box>
          </Box>
          
          <Divider orientation="vertical" flexItem />
          
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" gutterBottom>
              إشارات المؤشرات
            </Typography>
            
            <List dense>
              <ListItem>
                <ListItemIcon>
                  {indicators.rsi.signal === 'buy' ? (
                    <TrendingUpIcon color="success" />
                  ) : indicators.rsi.signal === 'sell' ? (
                    <TrendingDownIcon color="error" />
                  ) : (
                    <TimelineIcon color="warning" />
                  )}
                </ListItemIcon>
                <ListItemText 
                  primary="مؤشر القوة النسبية (RSI)" 
                  secondary={`${indicators.rsi.value.toFixed(2)} - ${
                    indicators.rsi.signal === 'buy' ? 'شراء' : 
                    indicators.rsi.signal === 'sell' ? 'بيع' : 
                    'انتظار'
                  }`}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  {indicators.macd.signal === 'buy' ? (
                    <TrendingUpIcon color="success" />
                  ) : indicators.macd.signal === 'sell' ? (
                    <TrendingDownIcon color="error" />
                  ) : (
                    <TimelineIcon color="warning" />
                  )}
                </ListItemIcon>
                <ListItemText 
                  primary="مؤشر MACD" 
                  secondary={`${indicators.macd.value.toFixed(4)} - ${
                    indicators.macd.signal === 'buy' ? 'شراء' : 
                    indicators.macd.signal === 'sell' ? 'بيع' : 
                    'انتظار'
                  }`}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  {indicators.ma.signal === 'buy' ? (
                    <TrendingUpIcon color="success" />
                  ) : indicators.ma.signal === 'sell' ? (
                    <TrendingDownIcon color="error" />
                  ) : (
                    <TimelineIcon color="warning" />
                  )}
                </ListItemIcon>
                <ListItemText 
                  primary="المتوسطات المتحركة" 
                  secondary={`سريع: ${indicators.ma.fast.toFixed(4)}, بطيء: ${indicators.ma.slow.toFixed(4)} - ${
                    indicators.ma.signal === 'buy' ? 'شراء' : 
                    indicators.ma.signal === 'sell' ? 'بيع' : 
                    'انتظار'
                  }`}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  {indicators.stoch.signal === 'buy' ? (
                    <TrendingUpIcon color="success" />
                  ) : indicators.stoch.signal === 'sell' ? (
                    <TrendingDownIcon color="error" />
                  ) : (
                    <TimelineIcon color="warning" />
                  )}
                </ListItemIcon>
                <ListItemText 
                  primary="مؤشر ستوكاستيك" 
                  secondary={`K: ${indicators.stoch.k.toFixed(2)}, D: ${indicators.stoch.d.toFixed(2)} - ${
                    indicators.stoch.signal === 'buy' ? 'شراء' : 
                    indicators.stoch.signal === 'sell' ? 'بيع' : 
                    'انتظار'
                  }`}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  {indicators.bb.signal === 'buy' ? (
                    <TrendingUpIcon color="success" />
                  ) : indicators.bb.signal === 'sell' ? (
                    <TrendingDownIcon color="error" />
                  ) : (
                    <TimelineIcon color="warning" />
                  )}
                </ListItemIcon>
                <ListItemText 
                  primary="بولينجر باندز" 
                  secondary={`عرض: ${indicators.bb.width.toFixed(4)} - ${
                    indicators.bb.signal === 'buy' ? 'شراء' : 
                    indicators.bb.signal === 'sell' ? 'بيع' : 
                    'انتظار'
                  }`}
                />
              </ListItem>
            </List>
          </Box>
        </Box>
      </Paper>
      
      {/* تفاصيل المؤشرات */}
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* مؤشر القوة النسبية RSI */}
        <Box sx={{ width: '100%' }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              مؤشر القوة النسبية (RSI)
            </Typography>
            
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
              <Box sx={{ flex: 1 }}>
                <Typography variant="subtitle1" gutterBottom>
                  القيمة الحالية
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h4" fontWeight="bold" color={
                    indicators.rsi.value > 70 ? 'error.main' : 
                    indicators.rsi.value < 30 ? 'success.main' : 
                    'text.primary'
                  }>
                    {indicators.rsi.value.toFixed(2)}
                  </Typography>
                </Box>
                
                <Box sx={{ 
                  width: '100%', 
                  height: 20, 
                  bgcolor: 'grey.300', 
                  borderRadius: 1, 
                  mb: 2,
                  position: 'relative'
                }}>
                  <Box sx={{ 
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '30%',
                    height: '100%',
                    bgcolor: 'success.main',
                    opacity: 0.3
                  }} />
                  
                  <Box sx={{ 
                    position: 'absolute',
                    top: 0,
                    right: 0,
                    width: '30%',
                    height: '100%',
                    bgcolor: 'error.main',
                    opacity: 0.3
                  }} />
                  
                  <Box sx={{ 
                    position: 'absolute',
                    top: 0,
                    left: `${indicators.rsi.value}%`,
                    width: 4,
                    height: '100%',
                    bgcolor: 'primary.main',
                    transform: 'translateX(-50%)'
                  }} />
                </Box>
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">
                    تشبع بيعي (30)
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary">
                    محايد
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary">
                    تشبع شرائي (70)
                  </Typography>
                </Box>
              </Box>
              
              <Box sx={{ flex: 1 }}>
                <Typography variant="subtitle1" gutterBottom>
                  التفسير
                </Typography>
                
                <Typography variant="body1" paragraph>
                  {indicators.rsi.value > 70 ? 
                    'المؤشر في منطقة التشبع الشرائي، مما قد يشير إلى احتمالية حدوث انعكاس هبوطي.' : 
                   indicators.rsi.value < 30 ? 
                    'المؤشر في منطقة التشبع البيعي، مما قد يشير إلى احتمالية حدوث انعكاس صعودي.' : 
                    'المؤشر في المنطقة المحايدة، مما يشير إلى عدم وجود تشبع في السوق حالياً.'
                  }
                </Typography>
                
                <Typography variant="subtitle1" gutterBottom>
                  الإشارة
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {indicators.rsi.signal === 'buy' ? (
                    <TrendingUpIcon sx={{ fontSize: 30, color: 'success.main', mr: 1 }} />
                  ) : indicators.rsi.signal === 'sell' ? (
                    <TrendingDownIcon sx={{ fontSize: 30, color: 'error.main', mr: 1 }} />
                  ) : (
                    <TimelineIcon sx={{ fontSize: 30, color: 'warning.main', mr: 1 }} />
                  )}
                  
                  <Typography variant="h6" fontWeight="bold" color={
                    indicators.rsi.signal === 'buy' ? 'success.main' : 
                    indicators.rsi.signal === 'sell' ? 'error.main' : 
                    'warning.main'
                  }>
                    {indicators.rsi.signal === 'buy' ? 'شراء' : 
                     indicators.rsi.signal === 'sell' ? 'بيع' : 
                     'انتظار'}
                  </Typography>
                </Box>
              </Box>
            </Box>
          </Paper>
        </Box>
        
        {/* المتوسطات المتحركة */}
        <Box sx={{ width: '100%' }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              المتوسطات المتحركة (MA)
            </Typography>
            
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
              <Box sx={{ flex: 1 }}>
                <Typography variant="subtitle1" gutterBottom>
                  القيم الحالية
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body1">المتوسط السريع (9):</Typography>
                    <Typography variant="body1" fontWeight="bold" color="primary.main">
                      {indicators.ma.fast.toFixed(4)}
                    </Typography>
                  </Box>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">المتوسط البطيء (21):</Typography>
                    <Typography variant="body1" fontWeight="bold" color="secondary.main">
                      {indicators.ma.slow.toFixed(4)}
                    </Typography>
                  </Box>
                </Box>
                
                <Typography variant="subtitle1" gutterBottom>
                  الفرق
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {indicators.ma.fast > indicators.ma.slow ? (
                    <TrendingUpIcon sx={{ color: 'success.main', mr: 1 }} />
                  ) : (
                    <TrendingDownIcon sx={{ color: 'error.main', mr: 1 }} />
                  )}
                  
                  <Typography variant="body1" fontWeight="bold" color={
                    indicators.ma.fast > indicators.ma.slow ? 'success.main' : 'error.main'
                  }>
                    {Math.abs(indicators.ma.fast - indicators.ma.slow).toFixed(4)} ({
                      indicators.ma.fast > indicators.ma.slow ? 'إيجابي' : 'سلبي'
                    })
                  </Typography>
                </Box>
                
                <Typography variant="subtitle1" gutterBottom>
                  الاتجاه
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {indicators.ma.trend === 'bullish' ? (
                    <TrendingUpIcon sx={{ fontSize: 30, color: 'success.main', mr: 1 }} />
                  ) : (
                    <TrendingDownIcon sx={{ fontSize: 30, color: 'error.main', mr: 1 }} />
                  )}
                  
                  <Typography variant="h6" fontWeight="bold" color={
                    indicators.ma.trend === 'bullish' ? 'success.main' : 'error.main'
                  }>
                    {indicators.ma.trend === 'bullish' ? 'صعودي' : 'هبوطي'}
                  </Typography>
                </Box>
              </Box>
              
              <Box sx={{ flex: 1 }}>
                <Typography variant="subtitle1" gutterBottom>
                  التفسير
                </Typography>
                
                <Typography variant="body1" paragraph>
                  {indicators.ma.fast > indicators.ma.slow ? 
                    'المتوسط السريع فوق المتوسط البطيء، مما يشير إلى اتجاه صعودي. هذا يعتبر إشارة إيجابية للشراء.' : 
                    'المتوسط السريع تحت المتوسط البطيء، مما يشير إلى اتجاه هبوطي. هذا يعتبر إشارة سلبية للبيع.'
                  }
                </Typography>
                
                <Typography variant="subtitle1" gutterBottom>
                  الإشارة
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {indicators.ma.signal === 'buy' ? (
                    <TrendingUpIcon sx={{ fontSize: 30, color: 'success.main', mr: 1 }} />
                  ) : indicators.ma.signal === 'sell' ? (
                    <TrendingDownIcon sx={{ fontSize: 30, color: 'error.main', mr: 1 }} />
                  ) : (
                    <TimelineIcon sx={{ fontSize: 30, color: 'warning.main', mr: 1 }} />
                  )}
                  
                  <Typography variant="h6" fontWeight="bold" color={
                    indicators.ma.signal === 'buy' ? 'success.main' : 
                    indicators.ma.signal === 'sell' ? 'error.main' : 
                    'warning.main'
                  }>
                    {indicators.ma.signal === 'buy' ? 'شراء' : 
                     indicators.ma.signal === 'sell' ? 'بيع' : 
                     'انتظار'}
                  </Typography>
                </Box>
              </Box>
            </Box>
          </Paper>
        </Box>
      </Box>
      
      {/* التأكيدات النشطة */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          التأكيدات النشطة
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1" gutterBottom>
            التأكيدات النشطة: {dummyConfirmations.filter(c => c.active).length} من أصل {dummyConfirmations.length}
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {dummyConfirmations.map((confirmation, index) => (
            <Box key={index}>
              <Tooltip title={confirmation.active ? 'تأكيد نشط' : 'تأكيد غير نشط'}>
                <Chip
                  label={confirmation.name}
                  color={confirmation.active ? 'primary' : 'default'}
                  variant={confirmation.active ? 'filled' : 'outlined'}
                />
              </Tooltip>
            </Box>
          ))}
        </Box>
      </Paper>
      
      {/* أزرار التحكم */}
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button 
          variant="contained" 
          color="primary" 
          size="large"
          startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <RefreshIcon />}
          onClick={updateAnalysis}
          disabled={loading}
        >
          تحديث التحليل
        </Button>
      </Box>
    </Box>
  );
};

export default TechnicalAnalysis;
