"""
Feature Engineering for Machine Learning Models.

Extracts features from technical indicators for ML model training:
- WaveTrend features
- Money Flow features
- RSI/StochRSI features
- Price action features
- Volume features
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple
from datetime import datetime

from utils.logger import get_logger
from indicators.wavetrend import add_wavetrend
from indicators.money_flow import add_money_flow
from indicators.rsi import add_rsi, add_stochastic_rsi

logger = get_logger('features')


class FeatureEngineering:
    """Feature engineering for ML models."""
    
    def __init__(self):
        """Initialize feature engineering."""
        self.feature_columns = []
        logger.info("✅ Feature Engineering initialized")
    
    def add_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add price-based features.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with added price features
        """
        df = df.copy()
        
        # Price changes
        df['price_change'] = df['close'].pct_change()
        df['price_change_2'] = df['close'].pct_change(periods=2)
        df['price_change_5'] = df['close'].pct_change(periods=5)
        
        # High-Low range
        df['hl_range'] = (df['high'] - df['low']) / df['close']
        
        # Close position in range
        df['close_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
        df['close_position'] = df['close_position'].fillna(0.5)
        
        # Gap from previous close
        df['gap'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)
        
        # Body size (candle body)
        df['body_size'] = abs(df['close'] - df['open']) / df['close']
        
        # Upper/Lower shadows
        df['upper_shadow'] = (df['high'] - df[['open', 'close']].max(axis=1)) / df['close']
        df['lower_shadow'] = (df[['open', 'close']].min(axis=1) - df['low']) / df['close']
        
        logger.debug("Added price features")
        return df
    
    def add_volume_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add volume-based features.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with added volume features
        """
        df = df.copy()
        
        # Volume changes
        df['volume_change'] = df['volume'].pct_change()
        df['volume_ma_5'] = df['volume'].rolling(window=5).mean()
        df['volume_ma_20'] = df['volume'].rolling(window=20).mean()
        
        # Volume ratio to moving average
        df['volume_ratio_5'] = df['volume'] / df['volume_ma_5']
        df['volume_ratio_20'] = df['volume'] / df['volume_ma_20']
        
        # Volume-price correlation
        df['vp_ratio'] = df['volume'] * df['close']
        df['vp_ratio_change'] = df['vp_ratio'].pct_change()
        
        logger.debug("Added volume features")
        return df
    
    def add_moving_average_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add moving average features.
        
        Args:
            df: DataFrame with price data
            
        Returns:
            DataFrame with MA features
        """
        df = df.copy()
        
        # Simple Moving Averages
        df['sma_7'] = df['close'].rolling(window=7).mean()
        df['sma_25'] = df['close'].rolling(window=25).mean()
        df['sma_99'] = df['close'].rolling(window=99).mean()
        
        # Exponential Moving Averages
        df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # Distance from moving averages
        df['distance_sma_7'] = (df['close'] - df['sma_7']) / df['close']
        df['distance_sma_25'] = (df['close'] - df['sma_25']) / df['close']
        df['distance_ema_12'] = (df['close'] - df['ema_12']) / df['close']
        
        # MA crossovers
        df['ma_cross_7_25'] = (df['sma_7'] > df['sma_25']).astype(int)
        df['ma_cross_12_26'] = (df['ema_12'] > df['ema_26']).astype(int)
        
        logger.debug("Added moving average features")
        return df
    
    def add_wavetrend_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add WaveTrend-specific features.
        
        Args:
            df: DataFrame with WaveTrend indicators
            
        Returns:
            DataFrame with WaveTrend features
        """
        df = df.copy()
        
        # WaveTrend momentum
        df['wt1_momentum'] = df['wt1'].diff()
        df['wt2_momentum'] = df['wt2'].diff()
        
        # WaveTrend spread
        df['wt_spread'] = df['wt1'] - df['wt2']
        df['wt_spread_change'] = df['wt_spread'].diff()
        
        # WaveTrend zones
        df['wt_oversold'] = (df['wt1'] < -60).astype(int)
        df['wt_overbought'] = (df['wt1'] > 60).astype(int)
        df['wt_extreme_oversold'] = (df['wt1'] < -80).astype(int)
        df['wt_extreme_overbought'] = (df['wt1'] > 80).astype(int)
        
        # WaveTrend crossover signals
        df['wt_cross_up'] = ((df['wt1'] > df['wt2']) & (df['wt1'].shift(1) <= df['wt2'].shift(1))).astype(int)
        df['wt_cross_down'] = ((df['wt1'] < df['wt2']) & (df['wt1'].shift(1) >= df['wt2'].shift(1))).astype(int)
        
        logger.debug("Added WaveTrend features")
        return df
    
    def add_mfi_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add Money Flow Index features.
        
        Args:
            df: DataFrame with MFI indicator
            
        Returns:
            DataFrame with MFI features
        """
        df = df.copy()
        
        # MFI momentum
        df['mfi_momentum'] = df['mfi'].diff()
        df['mfi_acceleration'] = df['mfi_momentum'].diff()
        
        # MFI zones
        df['mfi_oversold'] = (df['mfi'] < 20).astype(int)
        df['mfi_overbought'] = (df['mfi'] > 80).astype(int)
        
        # MFI moving average
        df['mfi_ma_5'] = df['mfi'].rolling(window=5).mean()
        df['mfi_distance'] = df['mfi'] - df['mfi_ma_5']
        
        logger.debug("Added MFI features")
        return df
    
    def add_rsi_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add RSI and StochRSI features.
        
        Args:
            df: DataFrame with RSI indicators
            
        Returns:
            DataFrame with RSI features
        """
        df = df.copy()
        
        # RSI momentum
        df['rsi_momentum'] = df['rsi'].diff()
        
        # RSI zones
        df['rsi_oversold'] = (df['rsi'] < 30).astype(int)
        df['rsi_overbought'] = (df['rsi'] > 70).astype(int)
        
        # StochRSI features
        df['stoch_spread'] = df['stoch_k'] - df['stoch_d']
        df['stoch_cross_up'] = ((df['stoch_k'] > df['stoch_d']) & (df['stoch_k'].shift(1) <= df['stoch_d'].shift(1))).astype(int)
        df['stoch_cross_down'] = ((df['stoch_k'] < df['stoch_d']) & (df['stoch_k'].shift(1) >= df['stoch_d'].shift(1))).astype(int)
        
        logger.debug("Added RSI features")
        return df
    
    def create_target_variable(
        self,
        df: pd.DataFrame,
        lookahead: int = 12,
        threshold: float = 0.02
    ) -> pd.DataFrame:
        """
        Create target variable for ML models.
        
        Target: 1 if price increases by threshold% in next lookahead periods, else 0
        
        Args:
            df: DataFrame with price data
            lookahead: Number of periods to look ahead
            threshold: Minimum price change threshold (0.02 = 2%)
            
        Returns:
            DataFrame with target variable
        """
        df = df.copy()
        
        # Calculate future price change
        df['future_price'] = df['close'].shift(-lookahead)
        df['future_return'] = (df['future_price'] - df['close']) / df['close']
        
        # Binary target: 1 if price increases by threshold, 0 otherwise
        df['target'] = (df['future_return'] > threshold).astype(int)
        
        # Multi-class target (optional)
        df['target_multi'] = 0  # Neutral
        df.loc[df['future_return'] > threshold, 'target_multi'] = 1  # Buy
        df.loc[df['future_return'] < -threshold, 'target_multi'] = -1  # Sell
        
        logger.debug(f"Created target variable (lookahead={lookahead}, threshold={threshold})")
        return df
    
    def engineer_all_features(
        self,
        df: pd.DataFrame,
        include_indicators: bool = True
    ) -> pd.DataFrame:
        """
        Apply all feature engineering steps.
        
        Args:
            df: DataFrame with OHLCV data
            include_indicators: Whether to calculate indicators (if not already present)
            
        Returns:
            DataFrame with all features
        """
        logger.info("🔬 Engineering features...")
        
        # Add indicators if needed
        if include_indicators and 'wt1' not in df.columns:
            df = add_wavetrend(df)
            df = add_money_flow(df)
            df = add_rsi(df)
            df = add_stochastic_rsi(df)
        
        # Add all feature categories
        df = self.add_price_features(df)
        df = self.add_volume_features(df)
        df = self.add_moving_average_features(df)
        
        if 'wt1' in df.columns:
            df = self.add_wavetrend_features(df)
        
        if 'mfi' in df.columns:
            df = self.add_mfi_features(df)
        
        if 'rsi' in df.columns:
            df = self.add_rsi_features(df)
        
        # Create target variable
        df = self.create_target_variable(df)
        
        # Store feature column names
        self.feature_columns = self.get_feature_columns(df)
        
        logger.info(f"✅ Feature engineering completed: {len(self.feature_columns)} features")
        
        return df
    
    def get_feature_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of feature column names (excluding OHLCV and target).
        
        Args:
            df: DataFrame with features
            
        Returns:
            List of feature column names
        """
        exclude_cols = ['open', 'high', 'low', 'close', 'volume', 
                       'target', 'target_multi', 'future_price', 'future_return',
                       'wt_buy', 'wt_sell', 'mfi_buy', 'mfi_sell',
                       'rsi_buy', 'rsi_sell', 'stoch_buy', 'stoch_sell',
                       'mfi_bullish_div', 'mfi_bearish_div']
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        return feature_cols
    
    def prepare_ml_data(
        self,
        df: pd.DataFrame,
        drop_na: bool = True
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for ML model training.
        
        Args:
            df: DataFrame with features and target
            drop_na: Whether to drop rows with NaN values
            
        Returns:
            Tuple of (features DataFrame, target Series)
        """
        if drop_na:
            df = df.dropna()
        
        X = df[self.feature_columns]
        y = df['target']
        
        logger.info(f"📊 ML data prepared: {len(X)} samples, {len(self.feature_columns)} features")
        
        return X, y


if __name__ == '__main__':
    """Test feature engineering."""
    print("=" * 70)
    print("🔬 Testing Feature Engineering")
    print("=" * 70)
    
    from data_collection.binance_client import BinanceClient
    
    # Fetch data
    print("\n📈 Fetching BTC/USDT data...")
    client = BinanceClient()
    df = client.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=500)
    
    print(f"✅ Fetched {len(df)} candles")
    
    # Initialize feature engineering
    fe = FeatureEngineering()
    
    # Engineer features
    print("\n🔬 Engineering features...")
    df_features = fe.engineer_all_features(df, include_indicators=True)
    
    print(f"\n✅ Feature engineering completed!")
    print(f"   Total columns: {len(df_features.columns)}")
    print(f"   Feature columns: {len(fe.feature_columns)}")
    
    # Show feature categories
    print("\n📊 Feature Categories:")
    price_features = [col for col in fe.feature_columns if 'price' in col or 'body' in col or 'shadow' in col]
    volume_features = [col for col in fe.feature_columns if 'volume' in col or 'vp_' in col]
    wt_features = [col for col in fe.feature_columns if 'wt' in col]
    mfi_features = [col for col in fe.feature_columns if 'mfi' in col]
    rsi_features = [col for col in fe.feature_columns if 'rsi' in col or 'stoch' in col]
    ma_features = [col for col in fe.feature_columns if 'ma' in col or 'ema' in col or 'sma' in col]
    
    print(f"   Price features: {len(price_features)}")
    print(f"   Volume features: {len(volume_features)}")
    print(f"   WaveTrend features: {len(wt_features)}")
    print(f"   MFI features: {len(mfi_features)}")
    print(f"   RSI features: {len(rsi_features)}")
    print(f"   Moving Average features: {len(ma_features)}")
    
    # Prepare ML data
    print("\n📊 Preparing ML data...")
    X, y = fe.prepare_ml_data(df_features, drop_na=True)
    
    print(f"\n✅ ML data prepared:")
    print(f"   Samples: {len(X)}")
    print(f"   Features: {X.shape[1]}")
    print(f"   Target distribution:")
    print(f"     Buy signals (1): {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
    print(f"     No signal (0): {(y==0).sum()} ({(y==0).sum()/len(y)*100:.1f}%)")
    
    # Show sample features
    print("\n📊 Sample features (latest 5 rows):")
    print(X.tail())
    
    print("\n📊 Target values (latest 10):")
    print(y.tail(10).values)
    
    # Feature importance preview
    print("\n📊 Feature statistics:")
    print(X.describe().T[['mean', 'std', 'min', 'max']].head(10))
    
    print("\n" + "=" * 70)
    print("🎉 Feature Engineering test completed successfully!")
    print("=" * 70)
