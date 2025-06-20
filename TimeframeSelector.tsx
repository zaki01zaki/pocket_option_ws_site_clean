import React from 'react';
import { 
  Box, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem,
  SelectChangeEvent
} from '@mui/material';

interface TimeframeSelectorProps {
  selectedTimeframe: string;
  onTimeframeChange: (timeframe: string) => void;
}

const TimeframeSelector: React.FC<TimeframeSelectorProps> = ({ selectedTimeframe, onTimeframeChange }) => {
  
  const handleChange = (event: SelectChangeEvent) => {
    onTimeframeChange(event.target.value);
  };
  
  return (
    <Box sx={{ minWidth: 200 }}>
      <FormControl fullWidth>
        <InputLabel>الإطار الزمني</InputLabel>
        <Select
          value={selectedTimeframe}
          label="الإطار الزمني"
          onChange={handleChange}
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
  );
};

export default TimeframeSelector;
