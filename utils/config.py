"""
Configuration management for SignalCipher.

This module handles loading and accessing configuration from YAML files
and environment variables.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration manager for SignalCipher."""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self._config = None
        self._symbols = None
        self._timeframes = None
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load main configuration file.
        
        Returns:
            Dictionary containing configuration
        """
        if self._config is None:
            config_path = self.config_dir / "config.yaml"
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        return self._config
    
    def load_symbols(self) -> Dict[str, Any]:
        """
        Load symbols configuration.
        
        Returns:
            Dictionary containing symbols configuration
        """
        if self._symbols is None:
            symbols_path = self.config_dir / "symbols.yaml"
            with open(symbols_path, 'r') as f:
                self._symbols = yaml.safe_load(f)
        return self._symbols
    
    def load_timeframes(self) -> Dict[str, Any]:
        """
        Load timeframes configuration.
        
        Returns:
            Dictionary containing timeframes configuration
        """
        if self._timeframes is None:
            timeframes_path = self.config_dir / "timeframes.yaml"
            with open(timeframes_path, 'r') as f:
                self._timeframes = yaml.safe_load(f)
        return self._timeframes
    
    def get_top_symbols(self, count: Optional[int] = None) -> List[str]:
        """
        Get list of top cryptocurrency symbols to scan.
        
        Args:
            count: Number of symbols to return (None for all enabled)
            
        Returns:
            List of symbol strings (e.g., ['BTC/USDT', 'ETH/USDT'])
        """
        symbols_config = self.load_symbols()
        top_symbols = [
            s['symbol'] 
            for s in symbols_config['top_10'] 
            if s.get('enabled', True)
        ]
        
        if count:
            return top_symbols[:count]
        return top_symbols
    
    def get_active_timeframes(self) -> List[str]:
        """
        Get list of active timeframes.
        
        Returns:
            List of timeframe codes (e.g., ['1h', '4h', '1d'])
        """
        timeframes_config = self.load_timeframes()
        return [
            tf['code'] 
            for tf in timeframes_config['timeframes'] 
            if tf.get('enabled', False)
        ]
    
    def get_api_keys(self) -> Dict[str, str]:
        """
        Get API keys from environment variables.
        
        Returns:
            Dictionary with 'api_key' and 'secret'
            
        Raises:
            ValueError: If API keys are not set
        """
        api_key = os.getenv('BINANCE_API_KEY')
        secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not secret:
            raise ValueError(
                "Binance API keys not found in environment variables. "
                "Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file"
            )
        
        return {
            'api_key': api_key,
            'secret': secret
        }
    
    def get_indicator_params(self, indicator_name: str) -> Dict[str, Any]:
        """
        Get parameters for a specific indicator.
        
        Args:
            indicator_name: Name of the indicator (e.g., 'money_flow', 'wave_trend')
            
        Returns:
            Dictionary of indicator parameters
        """
        config = self.load_config()
        indicators = config.get('indicators', {})
        return indicators.get(indicator_name, {})
    
    def get_ml_params(self, model_name: str) -> Dict[str, Any]:
        """
        Get parameters for a specific ML model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary of model parameters
        """
        config = self.load_config()
        ml_models = config.get('ml_models', {})
        return ml_models.get(model_name, {})
    
    def get_scanner_params(self) -> Dict[str, Any]:
        """
        Get scanner configuration parameters.
        
        Returns:
            Dictionary of scanner parameters
        """
        config = self.load_config()
        return config.get('scanner', {})
    
    def get_database_url(self) -> str:
        """
        Get database URL from environment.
        
        Returns:
            Database URL string
        """
        return os.getenv('DATABASE_URL', 'sqlite:///signalcipher.db')
    
    def get_redis_url(self) -> str:
        """
        Get Redis URL from environment.
        
        Returns:
            Redis URL string
        """
        return os.getenv('REDIS_URL', 'redis://localhost:6379/0')


# Global config instance
config = Config()


# Convenience functions
def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config instance
    """
    return config


def get_top_symbols(count: Optional[int] = None) -> List[str]:
    """Get list of top symbols to scan."""
    return config.get_top_symbols(count)


def get_active_timeframes() -> List[str]:
    """Get list of active timeframes."""
    return config.get_active_timeframes()


def get_api_keys() -> Dict[str, str]:
    """Get Binance API keys."""
    return config.get_api_keys()


def get_indicator_params(indicator_name: str) -> Dict[str, Any]:
    """Get parameters for an indicator."""
    return config.get_indicator_params(indicator_name)


def get_ml_params(model_name: str) -> Dict[str, Any]:
    """Get parameters for an ML model."""
    return config.get_ml_params(model_name)


if __name__ == '__main__':
    """Test configuration loading."""
    print("=" * 70)
    print("🔧 SignalCipher Configuration Test")
    print("=" * 70)
    
    try:
        # Test main config
        main_config = config.load_config()
        print(f"\n✅ Main config loaded: {len(main_config)} sections")
        
        # Test symbols
        symbols = get_top_symbols()
        print(f"✅ Symbols loaded: {len(symbols)} active")
        print(f"   Top 3: {symbols[:3]}")
        
        # Test timeframes
        timeframes = get_active_timeframes()
        print(f"✅ Timeframes loaded: {timeframes}")
        
        # Test API keys
        try:
            keys = get_api_keys()
            print(f"✅ API keys found:")
            print(f"   Key: {keys['api_key'][:10]}...")
            print(f"   Secret: {keys['secret'][:10]}...")
        except ValueError as e:
            print(f"⚠️  API keys: {e}")
        
        # Test indicator params
        wt_params = get_indicator_params('wave_trend')
        print(f"✅ WaveTrend params: channel_len={wt_params.get('channel_length')}")
        
        mfi_params = get_indicator_params('money_flow')
        print(f"✅ MFI params: period={mfi_params.get('period')}")
        
        # Test scanner params
        scanner = config.get_scanner_params()
        print(f"✅ Scanner: interval={scanner.get('scan_interval')}s")
        
        print("\n" + "=" * 70)
        print("🎉 Configuration test completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error loading configuration: {e}")
        import traceback
        traceback.print_exc()
