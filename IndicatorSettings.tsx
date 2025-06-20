import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Switch, 
  FormControlLabel, 
  TextField, 
  Button, 
  Divider, 
  Chip,
  Stack,
  Slider,
  Alert,
  SelectChangeEvent
} from '@mui/material';
import { 
  Settings as SettingsIcon,
  TrendingUp as TrendingUpIcon,
  Save as SaveIcon
} from '@mui/icons-material';

// مكون إعدادات المؤشرات الفنية
const IndicatorSettings: React.FC = () => {
  // حالة الإعدادات
  const [settings, setSettings] = useState({
    // إعدادات مؤشر القوة النسبية RSI
    rsiEnabled: true,
    rsiPeriod: 14,
    rsiOverbought: 70,
    rsiOversold: 30,
    rsiWeight: 20,
    
    // إعدادات مؤشر MACD
    macdEnabled: true,
    macdFastPeriod: 12,
    macdSlowPeriod: 26,
    macdSignalPeriod: 9,
    macdWeight: 20,
    
    // إعدادات المتوسطات المتحركة
    maEnabled: true,
    maFastPeriod: 9,
    maSlowPeriod: 21,
    maType: 'ema', // ema, sma, wma
    maWeight: 20,
    
    // إعدادات بولينجر باندز
    bbEnabled: true,
    bbPeriod: 20,
    bbDeviation: 2,
    bbWeight: 20,
    
    // إعدادات ستوكاستيك
    stochEnabled: true,
    stochKPeriod: 14,
    stochDPeriod: 3,
    stochSlowing: 3,
    stochOverbought: 80,
    stochOversold: 20,
    stochWeight: 20,
    
    // إعدادات عامة
    confirmationThreshold: 60
  });
  
  // حالة الحفظ
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');
  
  // تغيير الإعدادات
  const handleSettingChange = (setting: string, value: any) => {
    setSettings({
      ...settings,
      [setting]: value
    });
    setSaveStatus('idle');
  };
  
  // تغيير نوع المتوسط المتحرك
  const handleMATypeChange = (event: SelectChangeEvent) => {
    handleSettingChange('maType', event.target.value);
  };
  
  // حفظ الإعدادات
  const saveSettings = () => {
    setSaveStatus('saving');
    
    // محاكاة حفظ الإعدادات
    setTimeout(() => {
      setSaveStatus('success');
      
      // إعادة الحالة إلى idle بعد 3 ثوان
      setTimeout(() => {
        setSaveStatus('idle');
      }, 3000);
    }, 1500);
  };
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Typography variant="h4" component="h1" sx={{ mb: 3, fontWeight: 'bold' }}>
        إعدادات المؤشرات الفنية
      </Typography>
      
      {/* حالة الحفظ */}
      {saveStatus === 'success' && (
        <Alert severity="success" sx={{ mb: 3 }}>
          تم حفظ الإعدادات بنجاح
        </Alert>
      )}
      
      {saveStatus === 'error' && (
        <Alert severity="error" sx={{ mb: 3 }}>
          حدث خطأ أثناء حفظ الإعدادات
        </Alert>
      )}
      
      {/* إعدادات عامة */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SettingsIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">إعدادات عامة</Typography>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            حد التأكيد: {settings.confirmationThreshold}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={settings.confirmationThreshold}
              onChange={(e, value) => handleSettingChange('confirmationThreshold', value)}
              min={50}
              max={90}
              step={5}
              marks={[
                { value: 50, label: '50%' },
                { value: 70, label: '70%' },
                { value: 90, label: '90%' }
              ]}
            />
          </Box>
          
          <Typography variant="caption" color="text.secondary">
            يحدد هذا الإعداد الحد الأدنى للتأكيد المطلوب لإنشاء إشارة تداول
          </Typography>
        </Box>
      </Paper>
      
      {/* إعدادات مؤشر القوة النسبية RSI */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TrendingUpIcon sx={{ mr: 1 }} color="primary" />
            <Typography variant="h6">مؤشر القوة النسبية (RSI)</Typography>
          </Box>
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.rsiEnabled}
                onChange={(e) => handleSettingChange('rsiEnabled', e.target.checked)}
                color="primary"
              />
            }
            label="تفعيل"
          />
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="الفترة"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.rsiPeriod}
            onChange={(e) => handleSettingChange('rsiPeriod', parseInt(e.target.value))}
            disabled={!settings.rsiEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <TextField
            label="مستوى التشبع الشرائي"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.rsiOverbought}
            onChange={(e) => handleSettingChange('rsiOverbought', parseInt(e.target.value))}
            disabled={!settings.rsiEnabled}
            InputProps={{ inputProps: { min: 50, max: 90 } }}
          />
          
          <TextField
            label="مستوى التشبع البيعي"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.rsiOversold}
            onChange={(e) => handleSettingChange('rsiOversold', parseInt(e.target.value))}
            disabled={!settings.rsiEnabled}
            InputProps={{ inputProps: { min: 10, max: 50 } }}
          />
        </Box>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            الوزن: {settings.rsiWeight}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={settings.rsiWeight}
              onChange={(e, value) => handleSettingChange('rsiWeight', value)}
              min={0}
              max={40}
              step={5}
              marks={[
                { value: 0, label: '0%' },
                { value: 20, label: '20%' },
                { value: 40, label: '40%' }
              ]}
              disabled={!settings.rsiEnabled}
            />
          </Box>
        </Box>
      </Paper>
      
      {/* إعدادات مؤشر MACD */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TrendingUpIcon sx={{ mr: 1 }} color="primary" />
            <Typography variant="h6">مؤشر MACD</Typography>
          </Box>
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.macdEnabled}
                onChange={(e) => handleSettingChange('macdEnabled', e.target.checked)}
                color="primary"
              />
            }
            label="تفعيل"
          />
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="الفترة السريعة"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.macdFastPeriod}
            onChange={(e) => handleSettingChange('macdFastPeriod', parseInt(e.target.value))}
            disabled={!settings.macdEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <TextField
            label="الفترة البطيئة"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.macdSlowPeriod}
            onChange={(e) => handleSettingChange('macdSlowPeriod', parseInt(e.target.value))}
            disabled={!settings.macdEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <TextField
            label="فترة الإشارة"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.macdSignalPeriod}
            onChange={(e) => handleSettingChange('macdSignalPeriod', parseInt(e.target.value))}
            disabled={!settings.macdEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
        </Box>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            الوزن: {settings.macdWeight}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={settings.macdWeight}
              onChange={(e, value) => handleSettingChange('macdWeight', value)}
              min={0}
              max={40}
              step={5}
              marks={[
                { value: 0, label: '0%' },
                { value: 20, label: '20%' },
                { value: 40, label: '40%' }
              ]}
              disabled={!settings.macdEnabled}
            />
          </Box>
        </Box>
      </Paper>
      
      {/* إعدادات المتوسطات المتحركة */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TrendingUpIcon sx={{ mr: 1 }} color="primary" />
            <Typography variant="h6">المتوسطات المتحركة</Typography>
          </Box>
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.maEnabled}
                onChange={(e) => handleSettingChange('maEnabled', e.target.checked)}
                color="primary"
              />
            }
            label="تفعيل"
          />
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="الفترة السريعة"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.maFastPeriod}
            onChange={(e) => handleSettingChange('maFastPeriod', parseInt(e.target.value))}
            disabled={!settings.maEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <TextField
            label="الفترة البطيئة"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.maSlowPeriod}
            onChange={(e) => handleSettingChange('maSlowPeriod', parseInt(e.target.value))}
            disabled={!settings.maEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <FormControl fullWidth>
            <InputLabel>نوع المتوسط</InputLabel>
            <Select
              value={settings.maType}
              label="نوع المتوسط"
              onChange={handleMATypeChange}
              disabled={!settings.maEnabled}
            >
              <MenuItem value="sma">المتوسط المتحرك البسيط (SMA)</MenuItem>
              <MenuItem value="ema">المتوسط المتحرك الأسي (EMA)</MenuItem>
              <MenuItem value="wma">المتوسط المتحرك الموزون (WMA)</MenuItem>
            </Select>
          </FormControl>
        </Box>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            الوزن: {settings.maWeight}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={settings.maWeight}
              onChange={(e, value) => handleSettingChange('maWeight', value)}
              min={0}
              max={40}
              step={5}
              marks={[
                { value: 0, label: '0%' },
                { value: 20, label: '20%' },
                { value: 40, label: '40%' }
              ]}
              disabled={!settings.maEnabled}
            />
          </Box>
        </Box>
      </Paper>
      
      {/* إعدادات بولينجر باندز */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TrendingUpIcon sx={{ mr: 1 }} color="primary" />
            <Typography variant="h6">بولينجر باندز</Typography>
          </Box>
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.bbEnabled}
                onChange={(e) => handleSettingChange('bbEnabled', e.target.checked)}
                color="primary"
              />
            }
            label="تفعيل"
          />
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="الفترة"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.bbPeriod}
            onChange={(e) => handleSettingChange('bbPeriod', parseInt(e.target.value))}
            disabled={!settings.bbEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <TextField
            label="الانحراف المعياري"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.bbDeviation}
            onChange={(e) => handleSettingChange('bbDeviation', parseFloat(e.target.value))}
            disabled={!settings.bbEnabled}
            InputProps={{ inputProps: { min: 1, max: 4, step: 0.1 } }}
          />
        </Box>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            الوزن: {settings.bbWeight}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={settings.bbWeight}
              onChange={(e, value) => handleSettingChange('bbWeight', value)}
              min={0}
              max={40}
              step={5}
              marks={[
                { value: 0, label: '0%' },
                { value: 20, label: '20%' },
                { value: 40, label: '40%' }
              ]}
              disabled={!settings.bbEnabled}
            />
          </Box>
        </Box>
      </Paper>
      
      {/* إعدادات ستوكاستيك */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TrendingUpIcon sx={{ mr: 1 }} color="primary" />
            <Typography variant="h6">ستوكاستيك</Typography>
          </Box>
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.stochEnabled}
                onChange={(e) => handleSettingChange('stochEnabled', e.target.checked)}
                color="primary"
              />
            }
            label="تفعيل"
          />
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="فترة K"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.stochKPeriod}
            onChange={(e) => handleSettingChange('stochKPeriod', parseInt(e.target.value))}
            disabled={!settings.stochEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <TextField
            label="فترة D"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.stochDPeriod}
            onChange={(e) => handleSettingChange('stochDPeriod', parseInt(e.target.value))}
            disabled={!settings.stochEnabled}
            InputProps={{ inputProps: { min: 2, max: 50 } }}
          />
          
          <TextField
            label="التباطؤ"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.stochSlowing}
            onChange={(e) => handleSettingChange('stochSlowing', parseInt(e.target.value))}
            disabled={!settings.stochEnabled}
            InputProps={{ inputProps: { min: 1, max: 10 } }}
          />
        </Box>
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="مستوى التشبع الشرائي"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.stochOverbought}
            onChange={(e) => handleSettingChange('stochOverbought', parseInt(e.target.value))}
            disabled={!settings.stochEnabled}
            InputProps={{ inputProps: { min: 50, max: 90 } }}
          />
          
          <TextField
            label="مستوى التشبع البيعي"
            type="number"
            variant="outlined"
            fullWidth
            value={settings.stochOversold}
            onChange={(e) => handleSettingChange('stochOversold', parseInt(e.target.value))}
            disabled={!settings.stochEnabled}
            InputProps={{ inputProps: { min: 10, max: 50 } }}
          />
        </Box>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            الوزن: {settings.stochWeight}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={settings.stochWeight}
              onChange={(e, value) => handleSettingChange('stochWeight', value)}
              min={0}
              max={40}
              step={5}
              marks={[
                { value: 0, label: '0%' },
                { value: 20, label: '20%' },
                { value: 40, label: '40%' }
              ]}
              disabled={!settings.stochEnabled}
            />
          </Box>
        </Box>
      </Paper>
      
      {/* أزرار التحكم */}
      <Stack direction="row" spacing={2} justifyContent="flex-end">
        <Button
          variant="outlined"
          color="secondary"
          onClick={() => {
            // إعادة تعيين الإعدادات إلى القيم الافتراضية
            setSettings({
              rsiEnabled: true,
              rsiPeriod: 14,
              rsiOverbought: 70,
              rsiOversold: 30,
              rsiWeight: 20,
              
              macdEnabled: true,
              macdFastPeriod: 12,
              macdSlowPeriod: 26,
              macdSignalPeriod: 9,
              macdWeight: 20,
              
              maEnabled: true,
              maFastPeriod: 9,
              maSlowPeriod: 21,
              maType: 'ema',
              maWeight: 20,
              
              bbEnabled: true,
              bbPeriod: 20,
              bbDeviation: 2,
              bbWeight: 20,
              
              stochEnabled: true,
              stochKPeriod: 14,
              stochDPeriod: 3,
              stochSlowing: 3,
              stochOverbought: 80,
              stochOversold: 20,
              stochWeight: 20,
              
              confirmationThreshold: 60
            });
            setSaveStatus('idle');
          }}
        >
          إعادة تعيين
        </Button>
        
        <Button
          variant="contained"
          color="primary"
          startIcon={<SaveIcon />}
          onClick={saveSettings}
          disabled={saveStatus === 'saving'}
        >
          {saveStatus === 'saving' ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
        </Button>
      </Stack>
    </Box>
  );
};

export default IndicatorSettings;
