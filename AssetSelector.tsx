import React from 'react';
import { 
  Box, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem,
  SelectChangeEvent
} from '@mui/material';

interface AssetSelectorProps {
  selectedAsset: string;
  onAssetChange: (asset: string) => void;
}

const AssetSelector: React.FC<AssetSelectorProps> = ({ selectedAsset, onAssetChange }) => {
  
  const handleChange = (event: SelectChangeEvent) => {
    onAssetChange(event.target.value);
  };
  
  return (
    <Box sx={{ minWidth: 200 }}>
      <FormControl fullWidth>
        <InputLabel>الأصل</InputLabel>
        <Select
          value={selectedAsset}
          label="الأصل"
          onChange={handleChange}
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
    </Box>
  );
};

export default AssetSelector;
