import React, { useState } from 'react';
import { 
  Box, 
  AppBar, 
  Toolbar, 
  Typography, 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  IconButton, 
  Divider, 
  Badge, 
  Avatar, 
  useTheme, 
  useMediaQuery,
  Chip,
  Container,
  Tooltip
} from '@mui/material';
import { 
  Dashboard as DashboardIcon, 
  ShowChart as ChartIcon, 
  Notifications as NotificationsIcon, 
  Storage as StorageIcon, 
  Settings as SettingsIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  Circle as CircleIcon
} from '@mui/icons-material';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const AppLayout: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  
  // التحقق من المسار النشط
  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };
  
  // قائمة الصفحات
  const menuItems = [
    { text: 'لوحة التحكم', icon: <DashboardIcon />, path: '/' },
    { text: 'التحليل الفني', icon: <ChartIcon />, path: '/technical-analysis' },
    { text: 'الإشارات', icon: <NotificationsIcon />, path: '/signals' },
    { text: 'البيانات', icon: <StorageIcon />, path: '/data' },
    { text: 'الإعدادات', icon: <SettingsIcon />, path: '/settings' }
  ];
  
  // فتح/إغلاق القائمة الجانبية في الأجهزة المحمولة
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  
  // التنقل بين الصفحات
  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      setMobileOpen(false);
    }
  };
  
  // محتوى القائمة الجانبية
  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          منصة التداول الذكية
        </Typography>
        {isMobile && (
          <IconButton onClick={handleDrawerToggle} size="small">
            <CloseIcon />
          </IconButton>
        )}
      </Box>
      
      <Divider />
      
      <List sx={{ flexGrow: 1 }}>
        {menuItems.map((item) => (
          <ListItem 
            key={item.text} 
            onClick={() => handleNavigation(item.path)}
            sx={{ 
              backgroundColor: isActive(item.path) ? 'rgba(25, 118, 210, 0.08)' : 'transparent',
              borderRight: isActive(item.path) ? `4px solid ${theme.palette.primary.main}` : 'none',
              '&:hover': {
                backgroundColor: 'rgba(25, 118, 210, 0.04)',
              }
            }}
          >
            <ListItemIcon sx={{ 
              color: isActive(item.path) ? theme.palette.primary.main : 'inherit',
              minWidth: 40
            }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText 
              primary={item.text} 
              primaryTypographyProps={{ 
                fontWeight: isActive(item.path) ? 'bold' : 'normal',
                color: isActive(item.path) ? theme.palette.primary.main : 'inherit'
              }}
            />
            {item.text === 'الإشارات' && (
              <Badge badgeContent={3} color="error" sx={{ mr: 1 }} />
            )}
          </ListItem>
        ))}
      </List>
      
      <Divider />
      
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Chip 
            icon={<CircleIcon sx={{ fontSize: '0.8rem', color: '#4caf50' }} />} 
            label="متصل" 
            size="small"
            variant="outlined"
            sx={{ 
              borderColor: '#4caf50',
              color: '#4caf50',
              '& .MuiChip-label': {
                px: 1
              }
            }}
          />
        </Box>
        
        <Typography variant="caption" color="text.secondary">
          v1.0.0
        </Typography>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* الشريط العلوي */}
      <AppBar 
        position="fixed" 
        sx={{ 
          zIndex: theme.zIndex.drawer + 1,
          boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
          backgroundColor: '#ffffff',
          color: 'text.primary'
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              flexGrow: 1, 
              display: { xs: 'none', sm: 'block' },
              fontWeight: 'bold',
              color: theme.palette.primary.main
            }}
          >
            منصة التداول الذكية | Pocket Option
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tooltip title="إشعارات جديدة">
              <IconButton color="inherit">
                <Badge badgeContent={4} color="error">
                  <NotificationsIcon />
                </Badge>
              </IconButton>
            </Tooltip>
            
            <Tooltip title="الملف الشخصي">
              <IconButton sx={{ p: 0, ml: 1 }}>
                <Avatar sx={{ bgcolor: theme.palette.primary.main }}>م</Avatar>
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>
      
      {/* القائمة الجانبية */}
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        {/* القائمة الجانبية للأجهزة المحمولة */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // تحسين الأداء على الأجهزة المحمولة
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              borderRadius: 0
            },
          }}
        >
          {drawer}
        </Drawer>
        
        {/* القائمة الجانبية للأجهزة المكتبية */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              borderRight: '1px solid rgba(0, 0, 0, 0.08)',
              boxShadow: 'none'
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      
      {/* المحتوى الرئيسي */}
      <Box
        component="main"
        sx={{ 
          flexGrow: 1, 
          width: { md: `calc(100% - ${drawerWidth}px)` },
          bgcolor: 'background.default',
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <Toolbar /> {/* مساحة للشريط العلوي */}
        
        <Container maxWidth="xl" sx={{ flexGrow: 1, py: 3 }}>
          <Outlet />
        </Container>
        
        {/* تذييل الصفحة */}
        <Box 
          component="footer" 
          sx={{ 
            py: 2, 
            textAlign: 'center',
            borderTop: '1px solid rgba(0, 0, 0, 0.08)',
            mt: 'auto'
          }}
        >
          <Typography variant="body2" color="text.secondary">
            منصة التداول الذكية © {new Date().getFullYear()}
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default AppLayout;
