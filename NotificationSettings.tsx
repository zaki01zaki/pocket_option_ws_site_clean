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
  Notifications as NotificationsIcon,
  Email as EmailIcon,
  Sms as SmsIcon,
  Save as SaveIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

// مكون إعدادات الإشعارات
const NotificationSettings: React.FC = () => {
  // حالة الإعدادات
  const [settings, setSettings] = useState({
    // إعدادات عامة
    notificationsEnabled: true,
    minConfidence: 70,
    
    // قنوات الإشعارات
    telegramEnabled: true,
    telegramChatId: '',
    telegramToken: '',
    
    emailEnabled: false,
    emailAddress: '',
    emailSubjectPrefix: '[منصة التداول]',
    
    smsEnabled: false,
    phoneNumber: '',
    
    // أنواع الإشعارات
    notifyOnBuySignal: true,
    notifyOnSellSignal: true,
    notifyOnSignalExpiry: false,
    notifyOnSystemEvents: true,
    
    // الأصول
    assetsToNotify: 'all', // all, selected
    selectedAssets: ['EURUSD', 'GBPUSD', 'BTCUSD'],
    
    // الأطر الزمنية
    timeframesToNotify: 'all', // all, selected
    selectedTimeframes: ['5m', '15m', '1h']
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
  
  // تغيير قائمة الأصول المحددة
  const handleAssetsChange = (event: SelectChangeEvent<string[]>) => {
    const { target: { value } } = event;
    handleSettingChange('selectedAssets', typeof value === 'string' ? value.split(',') : value);
  };
  
  // تغيير قائمة الأطر الزمنية المحددة
  const handleTimeframesChange = (event: SelectChangeEvent<string[]>) => {
    const { target: { value } } = event;
    handleSettingChange('selectedTimeframes', typeof value === 'string' ? value.split(',') : value);
  };
  
  // تغيير نوع الأصول للإشعار
  const handleAssetsToNotifyChange = (event: SelectChangeEvent) => {
    handleSettingChange('assetsToNotify', event.target.value);
  };
  
  // تغيير نوع الأطر الزمنية للإشعار
  const handleTimeframesToNotifyChange = (event: SelectChangeEvent) => {
    handleSettingChange('timeframesToNotify', event.target.value);
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
        إعدادات الإشعارات
      </Typography>
      
      {/* حالة الحفظ */}
      {saveStatus === 'success' && (
        <Alert severity="success" sx={{ mb: 3 }}>
          تم حفظ إعدادات الإشعارات بنجاح
        </Alert>
      )}
      
      {saveStatus === 'error' && (
        <Alert severity="error" sx={{ mb: 3 }}>
          حدث خطأ أثناء حفظ إعدادات الإشعارات
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
          <FormControlLabel
            control={
              <Switch
                checked={settings.notificationsEnabled}
                onChange={(e) => handleSettingChange('notificationsEnabled', e.target.checked)}
                color="primary"
              />
            }
            label="تفعيل الإشعارات"
          />
          
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            عند تعطيل الإشعارات، لن يتم إرسال أي إشعارات عبر أي قناة
          </Typography>
        </Box>
        
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            الحد الأدنى لنسبة الثقة للإشعارات: {settings.minConfidence}%
          </Typography>
          
          <Box sx={{ px: 1 }}>
            <Slider
              value={settings.minConfidence}
              onChange={(e, value) => handleSettingChange('minConfidence', value)}
              min={50}
              max={95}
              step={5}
              marks={[
                { value: 50, label: '50%' },
                { value: 70, label: '70%' },
                { value: 95, label: '95%' }
              ]}
              disabled={!settings.notificationsEnabled}
            />
          </Box>
          
          <Typography variant="caption" color="text.secondary">
            سيتم إرسال إشعارات فقط للإشارات التي تتجاوز نسبة الثقة المحددة
          </Typography>
        </Box>
      </Paper>
      
      {/* قنوات الإشعارات */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <NotificationsIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">قنوات الإشعارات</Typography>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        {/* إعدادات تيليجرام */}
        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="subtitle1">إشعارات تيليجرام</Typography>
            
            <FormControlLabel
              control={
                <Switch
                  checked={settings.telegramEnabled}
                  onChange={(e) => handleSettingChange('telegramEnabled', e.target.checked)}
                  color="primary"
                  disabled={!settings.notificationsEnabled}
                />
              }
              label="تفعيل"
            />
          </Box>
          
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
            <TextField
              label="معرف الدردشة (Chat ID)"
              variant="outlined"
              fullWidth
              value={settings.telegramChatId}
              onChange={(e) => handleSettingChange('telegramChatId', e.target.value)}
              disabled={!settings.notificationsEnabled || !settings.telegramEnabled}
            />
            
            <TextField
              label="رمز الوصول (Token)"
              variant="outlined"
              fullWidth
              value={settings.telegramToken}
              onChange={(e) => handleSettingChange('telegramToken', e.target.value)}
              disabled={!settings.notificationsEnabled || !settings.telegramEnabled}
            />
          </Box>
          
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            للحصول على معرف الدردشة ورمز الوصول، يرجى التواصل مع BotFather على تيليجرام
          </Typography>
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        {/* إعدادات البريد الإلكتروني */}
        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="subtitle1">إشعارات البريد الإلكتروني</Typography>
            
            <FormControlLabel
              control={
                <Switch
                  checked={settings.emailEnabled}
                  onChange={(e) => handleSettingChange('emailEnabled', e.target.checked)}
                  color="primary"
                  disabled={!settings.notificationsEnabled}
                />
              }
              label="تفعيل"
            />
          </Box>
          
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
            <TextField
              label="عنوان البريد الإلكتروني"
              variant="outlined"
              fullWidth
              value={settings.emailAddress}
              onChange={(e) => handleSettingChange('emailAddress', e.target.value)}
              disabled={!settings.notificationsEnabled || !settings.emailEnabled}
            />
            
            <TextField
              label="بادئة عنوان الرسالة"
              variant="outlined"
              fullWidth
              value={settings.emailSubjectPrefix}
              onChange={(e) => handleSettingChange('emailSubjectPrefix', e.target.value)}
              disabled={!settings.notificationsEnabled || !settings.emailEnabled}
            />
          </Box>
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        {/* إعدادات الرسائل النصية */}
        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="subtitle1">إشعارات الرسائل النصية (SMS)</Typography>
            
            <FormControlLabel
              control={
                <Switch
                  checked={settings.smsEnabled}
                  onChange={(e) => handleSettingChange('smsEnabled', e.target.checked)}
                  color="primary"
                  disabled={!settings.notificationsEnabled}
                />
              }
              label="تفعيل"
            />
          </Box>
          
          <TextField
            label="رقم الهاتف"
            variant="outlined"
            fullWidth
            value={settings.phoneNumber}
            onChange={(e) => handleSettingChange('phoneNumber', e.target.value)}
            disabled={!settings.notificationsEnabled || !settings.smsEnabled}
            placeholder="+1234567890"
            helperText="يرجى إدخال رقم الهاتف بالصيغة الدولية مع رمز البلد"
          />
        </Box>
      </Paper>
      
      {/* أنواع الإشعارات */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <NotificationsIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">أنواع الإشعارات</Typography>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.notifyOnBuySignal}
                onChange={(e) => handleSettingChange('notifyOnBuySignal', e.target.checked)}
                color="success"
                disabled={!settings.notificationsEnabled}
              />
            }
            label="إشعار عند ظهور إشارة شراء"
          />
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.notifyOnSellSignal}
                onChange={(e) => handleSettingChange('notifyOnSellSignal', e.target.checked)}
                color="error"
                disabled={!settings.notificationsEnabled}
              />
            }
            label="إشعار عند ظهور إشارة بيع"
          />
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.notifyOnSignalExpiry}
                onChange={(e) => handleSettingChange('notifyOnSignalExpiry', e.target.checked)}
                color="warning"
                disabled={!settings.notificationsEnabled}
              />
            }
            label="إشعار عند انتهاء صلاحية الإشارة"
          />
          
          <FormControlLabel
            control={
              <Switch
                checked={settings.notifyOnSystemEvents}
                onChange={(e) => handleSettingChange('notifyOnSystemEvents', e.target.checked)}
                color="info"
                disabled={!settings.notificationsEnabled}
              />
            }
            label="إشعار عند أحداث النظام (تحديثات، صيانة، إلخ)"
          />
        </Box>
      </Paper>
      
      {/* الأصول والأطر الزمنية */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SettingsIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">الأصول والأطر الزمنية</Typography>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        {/* الأصول */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            الأصول
          </Typography>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>الأصول للإشعار</InputLabel>
            <Select
              value={settings.assetsToNotify}
              label="الأصول للإشعار"
              onChange={handleAssetsToNotifyChange}
              disabled={!settings.notificationsEnabled}
            >
              <MenuItem value="all">جميع الأصول</MenuItem>
              <MenuItem value="selected">أصول محددة فقط</MenuItem>
            </Select>
          </FormControl>
          
          {settings.assetsToNotify === 'selected' && (
            <FormControl fullWidth>
              <InputLabel>الأصول المحددة</InputLabel>
              <Select
                multiple
                value={settings.selectedAssets}
                label="الأصول المحددة"
                onChange={handleAssetsChange}
                disabled={!settings.notificationsEnabled}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
              >
                <MenuItem value="EURUSD">EUR/USD</MenuItem>
                <MenuItem value="GBPUSD">GBP/USD</MenuItem>
                <MenuItem value="USDJPY">USD/JPY</MenuItem>
                <MenuItem value="AUDUSD">AUD/USD</MenuItem>
                <MenuItem value="USDCAD">USD/CAD</MenuItem>
                <MenuItem value="BTCUSD">BTC/USD</MenuItem>
                <MenuItem value="ETHUSD">ETH/USD</MenuItem>
                <MenuItem value="GOLD">GOLD</MenuItem>
              </Select>
            </FormControl>
          )}
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        {/* الأطر الزمنية */}
        <Box>
          <Typography variant="subtitle1" gutterBottom>
            الأطر الزمنية
          </Typography>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>الأطر الزمنية للإشعار</InputLabel>
            <Select
              value={settings.timeframesToNotify}
              label="الأطر الزمنية للإشعار"
              onChange={handleTimeframesToNotifyChange}
              disabled={!settings.notificationsEnabled}
            >
              <MenuItem value="all">جميع الأطر الزمنية</MenuItem>
              <MenuItem value="selected">أطر زمنية محددة فقط</MenuItem>
            </Select>
          </FormControl>
          
          {settings.timeframesToNotify === 'selected' && (
            <FormControl fullWidth>
              <InputLabel>الأطر الزمنية المحددة</InputLabel>
              <Select
                multiple
                value={settings.selectedTimeframes}
                label="الأطر الزمنية المحددة"
                onChange={handleTimeframesChange}
                disabled={!settings.notificationsEnabled}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
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
          )}
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
              notificationsEnabled: true,
              minConfidence: 70,
              
              telegramEnabled: true,
              telegramChatId: '',
              telegramToken: '',
              
              emailEnabled: false,
              emailAddress: '',
              emailSubjectPrefix: '[منصة التداول]',
              
              smsEnabled: false,
              phoneNumber: '',
              
              notifyOnBuySignal: true,
              notifyOnSellSignal: true,
              notifyOnSignalExpiry: false,
              notifyOnSystemEvents: true,
              
              assetsToNotify: 'all',
              selectedAssets: ['EURUSD', 'GBPUSD', 'BTCUSD'],
              
              timeframesToNotify: 'all',
              selectedTimeframes: ['5m', '15m', '1h']
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
          disabled={saveStatus === 'saving' || !settings.notificationsEnabled}
        >
          {saveStatus === 'saving' ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
        </Button>
      </Stack>
    </Box>
  );
};

export default NotificationSettings;
