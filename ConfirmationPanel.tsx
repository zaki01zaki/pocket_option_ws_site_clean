import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Stack,
  Chip, 
  Tooltip, 
  Switch, 
  FormControlLabel, 
  Button, 
  Divider,
  useTheme,
  IconButton,
  TextField
} from '@mui/material';
import { 
  Check as CheckIcon,
  Close as CloseIcon,
  Info as InfoIcon,
  Add as AddIcon
} from '@mui/icons-material';

// مكون لوحة التأكيدات
const ConfirmationPanel: React.FC = () => {
  const theme = useTheme();
  
  // حالة المكون
  const [loading, setLoading] = useState<boolean>(false);
  
  // بيانات وهمية للتأكيدات
  const [confirmations, setConfirmations] = useState<Array<{name: string, active: boolean, type: string}>>([
    { name: 'RSI تشبع شراء', active: true, type: 'technical' },
    { name: 'MACD تقاطع إيجابي', active: true, type: 'technical' },
    { name: 'المتوسط المتحرك 50/200', active: true, type: 'technical' },
    { name: 'بولينجر باندز اختراق', active: false, type: 'technical' },
    { name: 'ستوكاستيك تشبع بيع', active: true, type: 'technical' },
    { name: 'حجم التداول مرتفع', active: false, type: 'volume' },
    { name: 'نموذج شمعة انعكاسي', active: true, type: 'pattern' },
    { name: 'مستويات فيبوناتشي', active: false, type: 'pattern' },
    { name: 'مؤشر القوة النسبية', active: true, type: 'technical' },
    { name: 'تقاطع المتوسطات', active: true, type: 'technical' },
    { name: 'نموذج الرأس والكتفين', active: false, type: 'pattern' },
    { name: 'مستويات الدعم والمقاومة', active: true, type: 'price' }
  ]);
  
  // تبديل حالة التأكيد
  const toggleConfirmation = (index: number) => {
    const newConfirmations = [...confirmations];
    newConfirmations[index].active = !newConfirmations[index].active;
    setConfirmations(newConfirmations);
  };
  
  // حفظ التغييرات
  const saveChanges = () => {
    setLoading(true);
    
    // محاكاة حفظ التغييرات
    setTimeout(() => {
      setLoading(false);
      alert('تم حفظ التغييرات بنجاح');
    }, 1500);
  };
  
  // تفعيل جميع التأكيدات
  const enableAll = () => {
    const newConfirmations = confirmations.map(conf => ({ ...conf, active: true }));
    setConfirmations(newConfirmations);
  };
  
  // تعطيل جميع التأكيدات
  const disableAll = () => {
    const newConfirmations = confirmations.map(conf => ({ ...conf, active: false }));
    setConfirmations(newConfirmations);
  };
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* عنوان الصفحة */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          نظام التأكيدات المتعدد
        </Typography>
        
        <Box>
          <Button 
            variant="outlined" 
            color="primary" 
            onClick={enableAll}
            sx={{ mr: 1 }}
          >
            تفعيل الكل
          </Button>
          
          <Button 
            variant="outlined" 
            color="error" 
            onClick={disableAll}
            sx={{ mr: 1 }}
          >
            تعطيل الكل
          </Button>
          
          <Button 
            variant="contained" 
            color="primary" 
            onClick={saveChanges}
            disabled={loading}
          >
            حفظ التغييرات
          </Button>
        </Box>
      </Box>
      
      {/* شرح نظام التأكيدات */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
          <InfoIcon color="info" sx={{ mr: 2, mt: 0.5 }} />
          <Box>
            <Typography variant="h6" gutterBottom>
              نظام التأكيدات المتعدد
            </Typography>
            <Typography variant="body1">
              يستخدم نظام التأكيدات المتعدد لتحسين دقة الإشارات من خلال تحليل مجموعة متنوعة من المؤشرات الفنية والأنماط السعرية. كلما زاد عدد التأكيدات النشطة، زادت دقة الإشارة. يمكنك تفعيل أو تعطيل التأكيدات حسب استراتيجية التداول الخاصة بك.
            </Typography>
          </Box>
        </Box>
      </Paper>
      
      {/* تصنيف التأكيدات */}
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
        <Box sx={{ flex: 1 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              التأكيدات الفنية
            </Typography>
            
            <Divider sx={{ mb: 2 }} />
            
            <Box>
              {confirmations
                .filter(conf => conf.type === 'technical')
                .map((confirmation, index) => (
                  <Box key={index} sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {confirmation.active ? (
                        <CheckIcon sx={{ color: 'success.main', mr: 1 }} />
                      ) : (
                        <CloseIcon sx={{ color: 'text.disabled', mr: 1 }} />
                      )}
                      <Typography variant={confirmation.active ? 'subtitle1' : 'body1'} sx={{ color: confirmation.active ? 'text.primary' : 'text.secondary' }}>
                        {confirmation.name}
                      </Typography>
                    </Box>
                    
                    <Switch
                      checked={confirmation.active}
                      onChange={() => toggleConfirmation(confirmations.findIndex(c => c.name === confirmation.name))}
                      color="primary"
                    />
                  </Box>
                ))}
            </Box>
          </Paper>
        </Box>
        
        <Box sx={{ flex: 1 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              تأكيدات الأنماط والحجم
            </Typography>
            
            <Divider sx={{ mb: 2 }} />
            
            <Box>
              {confirmations
                .filter(conf => conf.type === 'pattern' || conf.type === 'volume' || conf.type === 'price')
                .map((confirmation, index) => (
                  <Box key={index} sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {confirmation.active ? (
                        <CheckIcon sx={{ color: 'success.main', mr: 1 }} />
                      ) : (
                        <CloseIcon sx={{ color: 'text.disabled', mr: 1 }} />
                      )}
                      <Typography variant={confirmation.active ? 'subtitle1' : 'body1'} sx={{ color: confirmation.active ? 'text.primary' : 'text.secondary' }}>
                        {confirmation.name}
                      </Typography>
                    </Box>
                    
                    <Switch
                      checked={confirmation.active}
                      onChange={() => toggleConfirmation(confirmations.findIndex(c => c.name === confirmation.name))}
                      color="primary"
                    />
                  </Box>
                ))}
            </Box>
          </Paper>
        </Box>
      </Box>
      
      {/* إضافة تأكيد جديد */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          إضافة تأكيد جديد
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2 }}>
          <Box sx={{ flex: { xs: '1', sm: '5' } }}>
            <TextField
              fullWidth
              label="اسم التأكيد"
              placeholder="مثال: تقاطع المتوسطات 20/50"
            />
          </Box>
          
          <Box sx={{ flex: { xs: '1', sm: '5' } }}>
            <TextField
              fullWidth
              select
              label="نوع التأكيد"
              SelectProps={{
                native: true,
              }}
            >
              <option value="technical">مؤشر فني</option>
              <option value="pattern">نمط سعري</option>
              <option value="volume">حجم التداول</option>
              <option value="price">مستويات السعر</option>
            </TextField>
          </Box>
          
          <Box sx={{ flex: { xs: '1', sm: '2' } }}>
            <Button 
              variant="contained" 
              color="primary" 
              startIcon={<AddIcon />}
              fullWidth
              sx={{ height: '100%' }}
            >
              إضافة
            </Button>
          </Box>
        </Box>
      </Paper>
      
      {/* ملخص التأكيدات */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          ملخص التأكيدات
        </Typography>
        
        <Divider sx={{ mb: 2 }} />
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {confirmations.map((confirmation, index) => (
            <Box key={index} sx={{ width: { xs: 'calc(50% - 8px)', sm: 'calc(33.33% - 8px)', md: 'calc(25% - 8px)', lg: 'calc(16.66% - 8px)' } }}>
              <Tooltip title={confirmation.active ? 'تأكيد نشط' : 'تأكيد غير نشط'}>
                <Chip
                  label={confirmation.name}
                  color={confirmation.active ? 'primary' : 'default'}
                  variant={confirmation.active ? 'filled' : 'outlined'}
                  sx={{ width: '100%' }}
                />
              </Tooltip>
            </Box>
          ))}
        </Box>
        
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="subtitle1">
            التأكيدات النشطة: {confirmations.filter(c => c.active).length} من أصل {confirmations.length}
          </Typography>
          
          <Button 
            variant="contained" 
            color="primary" 
            onClick={saveChanges}
            disabled={loading}
          >
            حفظ التغييرات
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default ConfirmationPanel;
