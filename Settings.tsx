import React, { useState } from 'react';
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
  Switch,
  FormControlLabel,
  useTheme,
  IconButton,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tab,
  Tabs
} from '@mui/material';
import { 
  Settings as SettingsIcon, 
  Save as SaveIcon,
  Language as LanguageIcon,
  Palette as PaletteIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
  AccountCircle as AccountCircleIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  DarkMode as DarkModeIcon,
  LightMode as LightModeIcon
} from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

// مكون لعرض محتوى التبويب
function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

// مكون الإعدادات
const Settings: React.FC = () => {
  const theme = useTheme();
  
  // حالة المكون
  const [loading, setLoading] = useState<boolean>(false);
  const [tabValue, setTabValue] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  
  // إعدادات المستخدم
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [language, setLanguage] = useState<string>('ar');
  const [emailNotifications, setEmailNotifications] = useState<boolean>(true);
  const [telegramNotifications, setTelegramNotifications] = useState<boolean>(true);
  const [smsNotifications, setSmsNotifications] = useState<boolean>(false);
  const [autoRefresh, setAutoRefresh] = useState<boolean>(true);
  const [refreshInterval, setRefreshInterval] = useState<number>(5);
  const [apiKey, setApiKey] = useState<string>('po_api_key_123456789');
  
  // تغيير التبويب
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };
  
  // فتح مربع الحوار
  const handleOpenDialog = () => {
    setOpenDialog(true);
  };
  
  // إغلاق مربع الحوار
  const handleCloseDialog = () => {
    setOpenDialog(false);
  };
  
  // حفظ الإعدادات
  const saveSettings = () => {
    setLoading(true);
    
    // محاكاة حفظ الإعدادات
    setTimeout(() => {
      setLoading(false);
      alert('تم حفظ الإعدادات بنجاح');
    }, 1500);
  };
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          الإعدادات
        </Typography>
        
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<SaveIcon />}
          onClick={saveSettings}
          disabled={loading}
        >
          حفظ الإعدادات
        </Button>
      </Box>
      
      {/* تبويبات الإعدادات */}
      <Paper sx={{ width: '100%', mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab icon={<AccountCircleIcon />} label="الحساب" />
          <Tab icon={<PaletteIcon />} label="المظهر" />
          <Tab icon={<NotificationsIcon />} label="الإشعارات" />
          <Tab icon={<SecurityIcon />} label="الأمان" />
        </Tabs>
        
        {/* محتوى تبويب الحساب */}
        <TabPanel value={tabValue} index={0}>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                معلومات الحساب
              </Typography>
              
              <TextField
                fullWidth
                label="اسم المستخدم"
                defaultValue="trader123"
                sx={{ mb: 3 }}
              />
              
              <TextField
                fullWidth
                label="البريد الإلكتروني"
                defaultValue="user@example.com"
                sx={{ mb: 3 }}
              />
              
              <TextField
                fullWidth
                label="الاسم الكامل"
                defaultValue="محمد أحمد"
                sx={{ mb: 3 }}
              />
              
              <Button 
                variant="outlined" 
                color="primary"
                onClick={handleOpenDialog}
              >
                تغيير كلمة المرور
              </Button>
            </Box>
            
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                إعدادات الحساب
              </Typography>
              
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel id="timezone-select-label">المنطقة الزمنية</InputLabel>
                <Select
                  labelId="timezone-select-label"
                  id="timezone-select"
                  value="Asia/Riyadh"
                  label="المنطقة الزمنية"
                >
                  <MenuItem value="Asia/Riyadh">الرياض (GMT+3)</MenuItem>
                  <MenuItem value="Asia/Dubai">دبي (GMT+4)</MenuItem>
                  <MenuItem value="Europe/London">لندن (GMT+0)</MenuItem>
                  <MenuItem value="America/New_York">نيويورك (GMT-5)</MenuItem>
                  <MenuItem value="Asia/Tokyo">طوكيو (GMT+9)</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel id="language-select-label">اللغة</InputLabel>
                <Select
                  labelId="language-select-label"
                  id="language-select"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  label="اللغة"
                >
                  <MenuItem value="ar">العربية</MenuItem>
                  <MenuItem value="en">الإنجليزية</MenuItem>
                  <MenuItem value="fr">الفرنسية</MenuItem>
                  <MenuItem value="tr">التركية</MenuItem>
                </Select>
              </FormControl>
              
              <FormControlLabel
                control={
                  <Switch 
                    checked={autoRefresh} 
                    onChange={() => setAutoRefresh(!autoRefresh)} 
                    color="primary"
                  />
                }
                label="تحديث البيانات تلقائياً"
                sx={{ mb: 2, display: 'block' }}
              />
              
              {autoRefresh && (
                <TextField
                  fullWidth
                  label="فترة التحديث (دقائق)"
                  type="number"
                  value={refreshInterval}
                  onChange={(e) => setRefreshInterval(parseInt(e.target.value))}
                  InputProps={{ inputProps: { min: 1, max: 60 } }}
                />
              )}
            </Box>
          </Box>
        </TabPanel>
        
        {/* محتوى تبويب المظهر */}
        <TabPanel value={tabValue} index={1}>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                السمة والألوان
              </Typography>
              
              <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {darkMode ? <DarkModeIcon sx={{ mr: 1 }} /> : <LightModeIcon sx={{ mr: 1 }} />}
                  <Typography variant="body1">
                    {darkMode ? 'الوضع الداكن' : 'الوضع الفاتح'}
                  </Typography>
                </Box>
                
                <Switch 
                  checked={darkMode} 
                  onChange={() => setDarkMode(!darkMode)} 
                  color="primary"
                />
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                اللون الرئيسي
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 1, mb: 3, flexWrap: 'wrap' }}>
                {['#1976d2', '#2196f3', '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722', '#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5'].map((color) => (
                  <Box
                    key={color}
                    sx={{
                      width: 30,
                      height: 30,
                      bgcolor: color,
                      borderRadius: '50%',
                      cursor: 'pointer',
                      border: '2px solid',
                      borderColor: color === '#1976d2' ? 'primary.main' : 'transparent',
                    }}
                  />
                ))}
              </Box>
              
              <Typography variant="subtitle1" gutterBottom>
                اللون الثانوي
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 1, mb: 3, flexWrap: 'wrap' }}>
                {['#f50057', '#ff4081', '#e040fb', '#7c4dff', '#536dfe', '#448aff', '#40c4ff', '#18ffff', '#64ffda', '#69f0ae', '#b2ff59', '#eeff41', '#ffff00', '#ffd740', '#ffab40', '#ff6e40'].map((color) => (
                  <Box
                    key={color}
                    sx={{
                      width: 30,
                      height: 30,
                      bgcolor: color,
                      borderRadius: '50%',
                      cursor: 'pointer',
                      border: '2px solid',
                      borderColor: color === '#f50057' ? 'secondary.main' : 'transparent',
                    }}
                  />
                ))}
              </Box>
            </Box>
            
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                تخصيص الواجهة
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <SettingsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="عرض شريط التنقل الجانبي" 
                    secondary="إظهار أو إخفاء شريط التنقل الجانبي"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <SettingsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="عرض الرسوم البيانية المصغرة" 
                    secondary="إظهار الرسوم البيانية المصغرة في لوحة التحكم"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <SettingsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="تمكين الرسوم المتحركة" 
                    secondary="تفعيل الرسوم المتحركة في واجهة المستخدم"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <SettingsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="عرض الإحصائيات المفصلة" 
                    secondary="إظهار إحصائيات مفصلة في لوحة التحكم"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
              </List>
            </Box>
          </Box>
        </TabPanel>
        
        {/* محتوى تبويب الإشعارات */}
        <TabPanel value={tabValue} index={2}>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                قنوات الإشعارات
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <NotificationsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="إشعارات البريد الإلكتروني" 
                    secondary="إرسال الإشعارات عبر البريد الإلكتروني"
                  />
                  <ListItemSecondaryAction>
                    <Switch 
                      checked={emailNotifications} 
                      onChange={() => setEmailNotifications(!emailNotifications)} 
                      color="primary" 
                    />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <NotificationsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="إشعارات تيليجرام" 
                    secondary="إرسال الإشعارات عبر تيليجرام"
                  />
                  <ListItemSecondaryAction>
                    <Switch 
                      checked={telegramNotifications} 
                      onChange={() => setTelegramNotifications(!telegramNotifications)} 
                      color="primary" 
                    />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <NotificationsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="إشعارات الرسائل النصية" 
                    secondary="إرسال الإشعارات عبر الرسائل النصية"
                  />
                  <ListItemSecondaryAction>
                    <Switch 
                      checked={smsNotifications} 
                      onChange={() => setSmsNotifications(!smsNotifications)} 
                      color="primary" 
                    />
                  </ListItemSecondaryAction>
                </ListItem>
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                معلومات الاتصال
              </Typography>
              
              <TextField
                fullWidth
                label="البريد الإلكتروني للإشعارات"
                defaultValue="user@example.com"
                sx={{ mb: 3 }}
                disabled={!emailNotifications}
              />
              
              <TextField
                fullWidth
                label="معرف محادثة تيليجرام"
                defaultValue="123456789"
                sx={{ mb: 3 }}
                disabled={!telegramNotifications}
              />
              
              <TextField
                fullWidth
                label="رقم الهاتف للرسائل النصية"
                defaultValue="+966501234567"
                disabled={!smsNotifications}
              />
            </Box>
            
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                إعدادات الإشعارات
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <NotificationsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="إشعارات إشارات الشراء" 
                    secondary="إرسال إشعارات عند ظهور إشارات شراء"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <NotificationsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="إشعارات إشارات البيع" 
                    secondary="إرسال إشعارات عند ظهور إشارات بيع"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <NotificationsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="إشعارات تغير الاتجاه" 
                    secondary="إرسال إشعارات عند تغير اتجاه السوق"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <NotificationsIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="إشعارات الأخبار الاقتصادية" 
                    secondary="إرسال إشعارات عند نشر أخبار اقتصادية مهمة"
                  />
                  <ListItemSecondaryAction>
                    <Switch color="primary" />
                  </ListItemSecondaryAction>
                </ListItem>
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                الحد الأدنى لنسبة الثقة
              </Typography>
              
              <TextField
                fullWidth
                label="نسبة الثقة (%)"
                type="number"
                defaultValue={75}
                InputProps={{ inputProps: { min: 50, max: 100 } }}
                sx={{ mb: 3 }}
                helperText="سيتم إرسال إشعارات فقط للإشارات التي تتجاوز نسبة الثقة المحددة"
              />
              
              <FormControlLabel
                control={<Switch defaultChecked color="primary" />}
                label="كتم الإشعارات خلال ساعات الليل (12 ص - 6 ص)"
              />
            </Box>
          </Box>
        </TabPanel>
        
        {/* محتوى تبويب الأمان */}
        <TabPanel value={tabValue} index={3}>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                بيانات الاعتماد
              </Typography>
              
              <TextField
                fullWidth
                label="مفتاح API لمنصة Pocket Option"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                sx={{ mb: 3 }}
              />
              
              <Button 
                variant="outlined" 
                color="primary"
                sx={{ mb: 3 }}
              >
                إنشاء مفتاح API جديد
              </Button>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                المصادقة الثنائية
              </Typography>
              
              <FormControlLabel
                control={<Switch color="primary" />}
                label="تفعيل المصادقة الثنائية"
                sx={{ mb: 2, display: 'block' }}
              />
              
              <Button 
                variant="outlined" 
                color="primary"
                disabled
              >
                إعداد المصادقة الثنائية
              </Button>
            </Box>
            
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                سجل الدخول
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemText 
                    primary="آخر تسجيل دخول" 
                    secondary="2025-06-05 22:45:12"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemText 
                    primary="عنوان IP" 
                    secondary="192.168.1.1"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemText 
                    primary="المتصفح" 
                    secondary="Chrome 120.0.0.0"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemText 
                    primary="نظام التشغيل" 
                    secondary="Windows 11"
                  />
                </ListItem>
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                خيارات الأمان
              </Typography>
              
              <FormControlLabel
                control={<Switch defaultChecked color="primary" />}
                label="تسجيل الخروج تلقائياً بعد 30 دقيقة من عدم النشاط"
                sx={{ mb: 2, display: 'block' }}
              />
              
              <FormControlLabel
                control={<Switch defaultChecked color="primary" />}
                label="إرسال إشعار عند تسجيل الدخول من جهاز جديد"
                sx={{ mb: 2, display: 'block' }}
              />
              
              <Button 
                variant="outlined" 
                color="error"
              >
                تسجيل الخروج من جميع الأجهزة
              </Button>
            </Box>
          </Box>
        </TabPanel>
      </Paper>
      
      {/* زر حفظ الإعدادات */}
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button 
          variant="contained" 
          color="primary" 
          size="large"
          startIcon={<SaveIcon />}
          onClick={saveSettings}
          disabled={loading}
        >
          حفظ جميع الإعدادات
        </Button>
      </Box>
      
      {/* مربع حوار تغيير كلمة المرور */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>تغيير كلمة المرور</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="كلمة المرور الحالية"
            type="password"
            fullWidth
            variant="outlined"
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="كلمة المرور الجديدة"
            type="password"
            fullWidth
            variant="outlined"
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="تأكيد كلمة المرور الجديدة"
            type="password"
            fullWidth
            variant="outlined"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="primary">
            إلغاء
          </Button>
          <Button onClick={handleCloseDialog} color="primary" variant="contained">
            تغيير كلمة المرور
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Settings;
