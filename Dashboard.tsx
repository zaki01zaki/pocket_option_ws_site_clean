import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Stack,
  Chip, 
  Tooltip, 
  CircularProgress,
  useTheme,
  Button,
  IconButton,
  Divider
} from '@mui/material';
import { 
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Refresh as RefreshIcon,
  ArrowUpward as ArrowUpwardIcon,
  ArrowDownward as ArrowDownwardIcon,
  Timeline as TimelineIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

// مكون لوحة التحكم الرئيسية
const Dashboard: React.FC = () => {
  const theme = useTheme();
  
  // حالة المكون
  const [loading, setLoading] = useState<boolean>(false);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  
  // بيانات وهمية للإشارات
  const [signals, setSignals] = useState({
    active: 12,
    buy: 8,
    sell: 4,
    pending: 3
  });
  
  // بيانات وهمية للأصول
  const [assets, setAssets] = useState([
    { name: 'EURUSD', trend: 'up', confidence: 85, timeframe: '15m' },
    { name: 'GBPUSD', trend: 'down', confidence: 78, timeframe: '1h' },
    { name: 'BTCUSD', trend: 'up', confidence: 92, timeframe: '5m' },
    { name: 'GOLD', trend: 'up', confidence: 67, timeframe: '30m' }
  ]);
  
  // بيانات وهمية للإحصائيات
  const [stats, setStats] = useState({
    successRate: 76,
    totalSignals: 248,
    todaySignals: 24,
    avgConfidence: 82
  });
  
  // تحديث البيانات
  const refreshData = () => {
    setLoading(true);
    
    // محاكاة تحديث البيانات
    setTimeout(() => {
      setSignals({
        active: Math.floor(Math.random() * 10) + 8,
        buy: Math.floor(Math.random() * 8) + 5,
        sell: Math.floor(Math.random() * 6) + 2,
        pending: Math.floor(Math.random() * 5)
      });
      
      setAssets([
        { name: 'EURUSD', trend: Math.random() > 0.5 ? 'up' : 'down', confidence: Math.floor(Math.random() * 20) + 70, timeframe: '15m' },
        { name: 'GBPUSD', trend: Math.random() > 0.5 ? 'up' : 'down', confidence: Math.floor(Math.random() * 20) + 70, timeframe: '1h' },
        { name: 'BTCUSD', trend: Math.random() > 0.5 ? 'up' : 'down', confidence: Math.floor(Math.random() * 20) + 70, timeframe: '5m' },
        { name: 'GOLD', trend: Math.random() > 0.5 ? 'up' : 'down', confidence: Math.floor(Math.random() * 20) + 70, timeframe: '30m' }
      ]);
      
      setStats({
        successRate: Math.floor(Math.random() * 10) + 70,
        totalSignals: stats.totalSignals + Math.floor(Math.random() * 10),
        todaySignals: Math.floor(Math.random() * 10) + 20,
        avgConfidence: Math.floor(Math.random() * 10) + 75
      });
      
      setLastUpdate(new Date());
      setLoading(false);
    }, 1500);
  };
  
  // تحديث البيانات عند تحميل المكون
  useEffect(() => {
    refreshData();
    
    // تحديث البيانات كل 5 دقائق
    const interval = setInterval(() => {
      refreshData();
    }, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          لوحة التحكم
        </Typography>
        
        <Box>
          <Button 
            variant="outlined" 
            color="primary" 
            startIcon={<RefreshIcon />}
            onClick={refreshData}
            disabled={loading}
            sx={{ mr: 1 }}
          >
            تحديث البيانات
          </Button>
          
          <IconButton color="primary">
            <SettingsIcon />
          </IconButton>
        </Box>
      </Box>
      
      {/* آخر تحديث */}
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
        {loading ? (
          <CircularProgress size={16} sx={{ mr: 1 }} />
        ) : null}
        <Typography variant="body2" color="text.secondary">
          آخر تحديث: {lastUpdate.toLocaleTimeString()}
        </Typography>
      </Box>
      
      {/* بطاقات المعلومات */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 3 }}>
        <Box sx={{ flex: '1 1 250px', maxWidth: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(25% - 18px)' } }}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography color="text.secondary" variant="subtitle2" gutterBottom>
              الإشارات النشطة
            </Typography>
            <Typography variant="h3" sx={{ my: 'auto', fontWeight: 'bold', color: theme.palette.primary.main }}>
              {signals.active}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Chip 
                icon={<TrendingUpIcon />} 
                label={`شراء: ${signals.buy}`} 
                color="success" 
                size="small" 
                variant="outlined"
              />
              <Chip 
                icon={<TrendingDownIcon />} 
                label={`بيع: ${signals.sell}`} 
                color="error" 
                size="small" 
                variant="outlined"
              />
            </Box>
          </Paper>
        </Box>
        
        <Box sx={{ flex: '1 1 250px', maxWidth: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(25% - 18px)' } }}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography color="text.secondary" variant="subtitle2" gutterBottom>
              نسبة النجاح
            </Typography>
            <Typography variant="h3" sx={{ my: 'auto', fontWeight: 'bold', color: theme.palette.success.main }}>
              {stats.successRate}%
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                إجمالي الإشارات: {stats.totalSignals}
              </Typography>
              <Chip 
                label={`اليوم: ${stats.todaySignals}`} 
                size="small" 
                variant="outlined"
              />
            </Box>
          </Paper>
        </Box>
        
        <Box sx={{ flex: '1 1 250px', maxWidth: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(25% - 18px)' } }}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography color="text.secondary" variant="subtitle2" gutterBottom>
              متوسط الثقة
            </Typography>
            <Typography variant="h3" sx={{ my: 'auto', fontWeight: 'bold', color: theme.palette.info.main }}>
              {stats.avgConfidence}%
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
              <Chip 
                label="60 تأكيد" 
                size="small" 
                variant="outlined"
              />
            </Box>
          </Paper>
        </Box>
        
        <Box sx={{ flex: '1 1 250px', maxWidth: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(25% - 18px)' } }}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography color="text.secondary" variant="subtitle2" gutterBottom>
              إشارات قيد الانتظار
            </Typography>
            <Typography variant="h3" sx={{ my: 'auto', fontWeight: 'bold', color: theme.palette.warning.main }}>
              {signals.pending}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
              <Button 
                variant="text" 
                color="primary" 
                size="small" 
                endIcon={<NotificationsIcon />}
              >
                تفعيل الإشعارات
              </Button>
            </Box>
          </Paper>
        </Box>
      </Box>
      
      {/* أحدث الإشارات */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          أحدث الإشارات
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {assets.map((asset, index) => (
            <Paper key={index} variant="outlined" sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {asset.trend === 'up' ? (
                    <ArrowUpwardIcon sx={{ color: 'success.main', mr: 1 }} />
                  ) : (
                    <ArrowDownwardIcon sx={{ color: 'error.main', mr: 1 }} />
                  )}
                  <Typography variant="h6">
                    {asset.name}
                  </Typography>
                  <Chip 
                    label={asset.timeframe} 
                    size="small" 
                    sx={{ ml: 1 }}
                  />
                </Box>
                
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Tooltip title="نسبة الثقة">
                    <Chip 
                      label={`${asset.confidence}%`} 
                      color={asset.confidence > 80 ? 'success' : 'primary'} 
                      size="small" 
                      sx={{ mr: 1 }}
                    />
                  </Tooltip>
                  
                  <Button 
                    variant="contained" 
                    color={asset.trend === 'up' ? 'success' : 'error'} 
                    size="small" 
                    startIcon={asset.trend === 'up' ? <TrendingUpIcon /> : <TrendingDownIcon />}
                  >
                    {asset.trend === 'up' ? 'شراء' : 'بيع'}
                  </Button>
                </Box>
              </Box>
            </Paper>
          ))}
        </Box>
        
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
          <Button 
            variant="outlined" 
            color="primary" 
            endIcon={<TimelineIcon />}
          >
            عرض جميع الإشارات
          </Button>
        </Box>
      </Paper>
      
      {/* الأطر الزمنية النشطة */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          الأطر الزمنية النشطة
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {['1m', '5m', '15m', '30m', '1h', '4h', '1d'].map((timeframe, index) => (
            <Chip 
              key={index}
              label={timeframe} 
              color={['5m', '15m', '1h'].includes(timeframe) ? 'primary' : 'default'} 
              variant={['5m', '15m', '1h'].includes(timeframe) ? 'filled' : 'outlined'}
            />
          ))}
        </Box>
        
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            الأصول النشطة
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {['EURUSD', 'GBPUSD', 'USDJPY', 'BTCUSD', 'ETHUSD', 'GOLD', 'SILVER'].map((asset, index) => (
              <Chip 
                key={index}
                label={asset} 
                color={['EURUSD', 'GBPUSD', 'BTCUSD', 'GOLD'].includes(asset) ? 'primary' : 'default'} 
                variant={['EURUSD', 'GBPUSD', 'BTCUSD', 'GOLD'].includes(asset) ? 'filled' : 'outlined'}
              />
            ))}
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default Dashboard;
