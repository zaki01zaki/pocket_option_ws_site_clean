import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Button, 
  Divider, 
  Stack,
  SelectChangeEvent
} from '@mui/material';
import { 
  DataCollection as DataCollectionIcon,
  Sync as SyncIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

// مكون جمع البيانات
const DataCollection: React.FC = () => {
  // حالة المكون
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<string>('EURUSD');
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('5m');
  const [collectionStatus, setCollectionStatus] = useState<'idle' | 'collecting' | 'success' | 'error'>('idle');
  const [lastCollection, setLastCollection] = useState<Date | null>(null);
  
  // تغيير الأصل المحدد
  const handleAssetChange = (event: SelectChangeEvent) => {
    setSelectedAsset(event.target.value);
  };
  
  // تغيير الإطار الزمني المحدد
  const handleTimeframeChange = (event: SelectChangeEvent) => {
    setSelectedTimeframe(event.target.value);
  };
  
  // بدء جمع البيانات
  const startDataCollection = () => {
    setLoading(true);
    setCollectionStatus('collecting');
    
    // محاكاة جمع البيانات
    setTimeout(() => {
      setLoading(false);
      setCollectionStatus('success');
      setLastCollection(new Date());
      
      // إعادة الحالة إلى idle بعد 3 ثوان
      setTimeout(() => {
        setCollectionStatus('idle');
      }, 3000);
    }, 2000);
  };
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Typography variant="h4" component="h1" sx={{ mb: 3, fontWeight: 'bold' }}>
        جمع البيانات الحية
      </Typography>
      
      {/* إعدادات جمع البيانات */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SettingsIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">إعدادات جمع البيانات</Typography>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 3 }}>
          <FormControl fullWidth>
            <InputLabel>الأصل</InputLabel>
            <Select
              value={selectedAsset}
              label="الأصل"
              onChange={handleAssetChange}
            >
              <MenuItem value="EURUSD">EUR/USD</MenuItem>
              <MenuItem value="GBPUSD">GBP/USD</MenuItem>
              <MenuItem value="USDJPY">USD/JPY</MenuItem>
              <MenuItem value="AUDUSD">AUD/USD</MenuItem>
              <MenuItem value="USDCAD">USD/CAD</MenuItem>
              <MenuItem value="NZDUSD">NZD/USD</MenuItem>
              <MenuItem value="USDCHF">USD/CHF</MenuItem>
              <MenuItem value="EURGBP">EUR/GBP</MenuItem>
              <MenuItem value="EURJPY">EUR/JPY</MenuItem>
              <MenuItem value="GBPJPY">GBP/JPY</MenuItem>
              <MenuItem value="BTCUSD">BTC/USD</MenuItem>
              <MenuItem value="ETHUSD">ETH/USD</MenuItem>
              <MenuItem value="GOLD">GOLD</MenuItem>
              <MenuItem value="SILVER">SILVER</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl fullWidth>
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
        </Box>
        
        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<SyncIcon />}
            onClick={startDataCollection}
            disabled={loading}
          >
            {loading ? 'جاري جمع البيانات...' : 'بدء جمع البيانات'}
          </Button>
        </Box>
      </Paper>
      
      {/* حالة جمع البيانات */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <DataCollectionIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">حالة جمع البيانات</Typography>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            الحالة الحالية:
          </Typography>
          
          <Typography variant="body1" fontWeight="bold" color={
            collectionStatus === 'collecting' ? 'primary.main' :
            collectionStatus === 'success' ? 'success.main' :
            collectionStatus === 'error' ? 'error.main' :
            'text.primary'
          }>
            {collectionStatus === 'collecting' ? 'جاري جمع البيانات...' :
             collectionStatus === 'success' ? 'تم جمع البيانات بنجاح' :
             collectionStatus === 'error' ? 'حدث خطأ أثناء جمع البيانات' :
             'جاهز لجمع البيانات'}
          </Typography>
        </Box>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            آخر تحديث للبيانات:
          </Typography>
          
          <Typography variant="body1">
            {lastCollection ? lastCollection.toLocaleString('ar-SA') : 'لم يتم جمع البيانات بعد'}
          </Typography>
        </Box>
        
        <Box>
          <Typography variant="subtitle1" gutterBottom>
            الأصول المتاحة:
          </Typography>
          
          <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
            <Paper sx={{ px: 2, py: 1, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              EUR/USD
            </Paper>
            <Paper sx={{ px: 2, py: 1, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              GBP/USD
            </Paper>
            <Paper sx={{ px: 2, py: 1, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              USD/JPY
            </Paper>
            <Paper sx={{ px: 2, py: 1, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              BTC/USD
            </Paper>
            <Paper sx={{ px: 2, py: 1, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              ETH/USD
            </Paper>
            <Paper sx={{ px: 2, py: 1, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              GOLD
            </Paper>
          </Stack>
        </Box>
      </Paper>
      
      {/* جدول زمني لجمع البيانات */}
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SettingsIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">الجدول الزمني لجمع البيانات</Typography>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ mb: 3 }}>
          <Typography variant="body1" paragraph>
            يتم جمع البيانات تلقائياً وفقاً للجدول الزمني التالي:
          </Typography>
          
          <Box component="ul" sx={{ pl: 2 }}>
            <Box component="li" sx={{ mb: 1 }}>
              <Typography variant="body1">
                <strong>الإطار الزمني 1 دقيقة:</strong> كل 30 ثانية
              </Typography>
            </Box>
            <Box component="li" sx={{ mb: 1 }}>
              <Typography variant="body1">
                <strong>الإطار الزمني 5 دقائق:</strong> كل 1 دقيقة
              </Typography>
            </Box>
            <Box component="li" sx={{ mb: 1 }}>
              <Typography variant="body1">
                <strong>الإطار الزمني 15 دقيقة:</strong> كل 3 دقائق
              </Typography>
            </Box>
            <Box component="li" sx={{ mb: 1 }}>
              <Typography variant="body1">
                <strong>الإطار الزمني 30 دقيقة:</strong> كل 5 دقائق
              </Typography>
            </Box>
            <Box component="li" sx={{ mb: 1 }}>
              <Typography variant="body1">
                <strong>الإطار الزمني 1 ساعة:</strong> كل 10 دقائق
              </Typography>
            </Box>
            <Box component="li" sx={{ mb: 1 }}>
              <Typography variant="body1">
                <strong>الإطار الزمني 4 ساعات:</strong> كل 30 دقيقة
              </Typography>
            </Box>
            <Box component="li">
              <Typography variant="body1">
                <strong>الإطار الزمني اليومي:</strong> كل ساعة
              </Typography>
            </Box>
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="outlined"
            color="primary"
            startIcon={<SettingsIcon />}
          >
            تعديل الجدول الزمني
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default DataCollection;
