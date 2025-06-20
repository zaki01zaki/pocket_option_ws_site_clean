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
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import { 
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Timeline as TimelineIcon
} from '@mui/icons-material';

// مكون قائمة الإشارات
const SignalsList: React.FC = () => {
  const theme = useTheme();
  
  // حالة المكون
  const [loading, setLoading] = useState<boolean>(false);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  
  // بيانات وهمية للإشارات
  const [signals, setSignals] = useState([
    { 
      id: 1, 
      asset: 'EURUSD', 
      direction: 'buy', 
      confidence: 87, 
      timeframe: '15m', 
      timestamp: new Date(Date.now() - 15 * 60000), 
      status: 'active',
      result: null,
      confirmations: 42
    },
    { 
      id: 2, 
      asset: 'GBPUSD', 
      direction: 'sell', 
      confidence: 82, 
      timeframe: '1h', 
      timestamp: new Date(Date.now() - 45 * 60000), 
      status: 'active',
      result: null,
      confirmations: 38
    },
    { 
      id: 3, 
      asset: 'BTCUSD', 
      direction: 'buy', 
      confidence: 91, 
      timeframe: '5m', 
      timestamp: new Date(Date.now() - 120 * 60000), 
      status: 'completed',
      result: 'win',
      confirmations: 51
    },
    { 
      id: 4, 
      asset: 'GOLD', 
      direction: 'buy', 
      confidence: 76, 
      timeframe: '30m', 
      timestamp: new Date(Date.now() - 180 * 60000), 
      status: 'completed',
      result: 'loss',
      confirmations: 32
    },
    { 
      id: 5, 
      asset: 'USDJPY', 
      direction: 'sell', 
      confidence: 84, 
      timeframe: '15m', 
      timestamp: new Date(Date.now() - 240 * 60000), 
      status: 'completed',
      result: 'win',
      confirmations: 45
    },
    { 
      id: 6, 
      asset: 'ETHUSD', 
      direction: 'buy', 
      confidence: 79, 
      timeframe: '5m', 
      timestamp: new Date(Date.now() - 300 * 60000), 
      status: 'completed',
      result: 'win',
      confirmations: 36
    },
    { 
      id: 7, 
      asset: 'SILVER', 
      direction: 'sell', 
      confidence: 72, 
      timeframe: '1h', 
      timestamp: new Date(Date.now() - 360 * 60000), 
      status: 'completed',
      result: 'loss',
      confirmations: 30
    },
    { 
      id: 8, 
      asset: 'AUDUSD', 
      direction: 'buy', 
      confidence: 68, 
      timeframe: '30m', 
      timestamp: new Date(Date.now() - 420 * 60000), 
      status: 'completed',
      result: 'win',
      confirmations: 33
    }
  ]);
  
  // تحديث البيانات
  const refreshData = () => {
    setLoading(true);
    
    // محاكاة تحديث البيانات
    setTimeout(() => {
      // إضافة إشارة جديدة
      const newSignal = { 
        id: signals.length + 1, 
        asset: ['EURUSD', 'GBPUSD', 'BTCUSD', 'GOLD', 'USDJPY'][Math.floor(Math.random() * 5)], 
        direction: Math.random() > 0.5 ? 'buy' : 'sell', 
        confidence: Math.floor(Math.random() * 20) + 70, 
        timeframe: ['5m', '15m', '30m', '1h'][Math.floor(Math.random() * 4)], 
        timestamp: new Date(), 
        status: 'active',
        result: null,
        confirmations: Math.floor(Math.random() * 20) + 30
      };
      
      setSignals([newSignal, ...signals.slice(0, 7)]);
      setLastUpdate(new Date());
      setLoading(false);
    }, 1500);
  };
  
  // تحديث البيانات عند تحميل المكون
  useEffect(() => {
    // تحديث البيانات كل 5 دقائق
    const interval = setInterval(() => {
      refreshData();
    }, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, [signals]);
  
  // تنسيق التاريخ
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };
  
  // تنسيق المدة
  const formatDuration = (timestamp: Date) => {
    const now = new Date();
    const diffMinutes = Math.floor((now.getTime() - timestamp.getTime()) / (1000 * 60));
    
    if (diffMinutes < 1) return 'الآن';
    if (diffMinutes < 60) return `منذ ${diffMinutes} دقيقة`;
    
    const hours = Math.floor(diffMinutes / 60);
    return `منذ ${hours} ساعة`;
  };
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          قائمة الإشارات
        </Typography>
        
        <Box>
          <Button 
            variant="outlined" 
            color="primary" 
            startIcon={loading ? <CircularProgress size={20} /> : <TimelineIcon />}
            onClick={refreshData}
            disabled={loading}
          >
            تحديث الإشارات
          </Button>
        </Box>
      </Box>
      
      {/* آخر تحديث */}
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
        <Typography variant="body2" color="text.secondary">
          آخر تحديث: {lastUpdate.toLocaleTimeString()}
        </Typography>
      </Box>
      
      {/* ملخص الإشارات */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
        <Chip 
          icon={<TrendingUpIcon />} 
          label={`شراء: ${signals.filter(s => s.direction === 'buy' && s.status === 'active').length}`} 
          color="success" 
          variant="outlined"
        />
        
        <Chip 
          icon={<TrendingDownIcon />} 
          label={`بيع: ${signals.filter(s => s.direction === 'sell' && s.status === 'active').length}`} 
          color="error" 
          variant="outlined"
        />
        
        <Chip 
          icon={<CheckCircleIcon />} 
          label={`ناجحة: ${signals.filter(s => s.result === 'win').length}`} 
          color="success" 
          variant="outlined"
        />
        
        <Chip 
          icon={<CancelIcon />} 
          label={`خاسرة: ${signals.filter(s => s.result === 'loss').length}`} 
          color="error" 
          variant="outlined"
        />
      </Box>
      
      {/* قائمة الإشارات */}
      <Paper sx={{ mb: 3 }}>
        <List>
          {signals.map((signal, index) => (
            <React.Fragment key={signal.id}>
              <ListItem 
                sx={{ 
                  bgcolor: signal.status === 'active' ? 'rgba(0, 0, 0, 0.02)' : 'transparent',
                  borderLeft: signal.status === 'active' ? `4px solid ${signal.direction === 'buy' ? theme.palette.success.main : theme.palette.error.main}` : 'none',
                  pl: signal.status === 'active' ? 2 : 3
                }}
              >
                <ListItemIcon>
                  {signal.direction === 'buy' ? (
                    <TrendingUpIcon color={signal.status === 'active' ? 'success' : 'disabled'} />
                  ) : (
                    <TrendingDownIcon color={signal.status === 'active' ? 'error' : 'disabled'} />
                  )}
                </ListItemIcon>
                
                <ListItemText 
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mr: 1 }}>
                        {signal.asset}
                      </Typography>
                      <Chip 
                        label={signal.timeframe} 
                        size="small" 
                        sx={{ mr: 1 }}
                      />
                      <Chip 
                        label={signal.direction === 'buy' ? 'شراء' : 'بيع'} 
                        color={signal.direction === 'buy' ? 'success' : 'error'} 
                        size="small" 
                        variant="outlined"
                        sx={{ mr: 1 }}
                      />
                      {signal.result && (
                        <Chip 
                          label={signal.result === 'win' ? 'ناجحة' : 'خاسرة'} 
                          color={signal.result === 'win' ? 'success' : 'error'} 
                          size="small" 
                        />
                      )}
                    </Box>
                  }
                  secondary={
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                      <Typography variant="body2" color="text.secondary" sx={{ mr: 2 }}>
                        {formatTime(signal.timestamp)} ({formatDuration(signal.timestamp)})
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        التأكيدات: {signal.confirmations}/60
                      </Typography>
                    </Box>
                  }
                />
                
                <Box>
                  <Tooltip title="نسبة الثقة">
                    <Chip 
                      label={`${signal.confidence}%`} 
                      color={
                        signal.confidence >= 85 ? 'success' : 
                        signal.confidence >= 75 ? 'primary' : 
                        'default'
                      } 
                      size="small" 
                    />
                  </Tooltip>
                </Box>
              </ListItem>
              
              {index < signals.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Paper>
      
      {/* تصفية الإشارات */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          تصفية الإشارات
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          <Typography variant="subtitle2" sx={{ mr: 1 }}>
            الأصول:
          </Typography>
          {['الكل', 'EURUSD', 'GBPUSD', 'BTCUSD', 'GOLD', 'USDJPY'].map((asset, index) => (
            <Chip 
              key={index}
              label={asset} 
              color={asset === 'الكل' ? 'primary' : 'default'} 
              variant={asset === 'الكل' ? 'filled' : 'outlined'}
              size="small"
            />
          ))}
        </Box>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          <Typography variant="subtitle2" sx={{ mr: 1 }}>
            الأطر الزمنية:
          </Typography>
          {['الكل', '5m', '15m', '30m', '1h', '4h'].map((timeframe, index) => (
            <Chip 
              key={index}
              label={timeframe} 
              color={timeframe === 'الكل' ? 'primary' : 'default'} 
              variant={timeframe === 'الكل' ? 'filled' : 'outlined'}
              size="small"
            />
          ))}
        </Box>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          <Typography variant="subtitle2" sx={{ mr: 1 }}>
            الحالة:
          </Typography>
          {['الكل', 'نشطة', 'مكتملة', 'ناجحة', 'خاسرة'].map((status, index) => (
            <Chip 
              key={index}
              label={status} 
              color={status === 'الكل' ? 'primary' : 'default'} 
              variant={status === 'الكل' ? 'filled' : 'outlined'}
              size="small"
            />
          ))}
        </Box>
      </Paper>
    </Box>
  );
};

export default SignalsList;
