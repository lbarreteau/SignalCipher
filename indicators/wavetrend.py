"""
WaveTrend Oscillator (LazyBear's Indicator).

This is the main indicator in Market Cipher B / VuManChu Cipher B.
It's a momentum oscillator that combines price, volume, and moving averages
to detect potential trend reversals.

Based on TradingView's WaveTrend by LazyBear.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional

from utils.logger import get_indicator_logger
from utils.config import get_indicator_params

logger = get_indicator_logger()


def hlc3(df: pd.DataFrame) -> pd.Series:
    """
    Calculate HLC3 (typical price).
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        
    Returns:
        Series with HLC3 values
    """
    return (df['high'] + df['low'] + df['close']) / 3


def ema(series: pd.Series, period: int) -> pd.Series:
    """
    Calculate Exponential Moving Average.
    
    Args:
        series: Input series
        period: EMA period
        
    Returns:
        Series with EMA values
    """
    return series.ewm(span=period, adjust=False).mean()


def wavetrend(
    df: pd.DataFrame,
    channel_len: int = 9,
    avg_len: int = 12,
    overbought: int = 60,
    oversold: int = -60,
    overbought2: int = 53,
    oversold2: int = -53
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate WaveTrend Oscillator.
    
    This is the core of Market Cipher B indicator.
    
    Formula (from VuManChu Cipher B analysis):
    1. Calculate typical price: hlc3 = (high + low + close) / 3
    2. Calculate ESA (Exponential Simple Average): esa = EMA(hlc3, channel_len)
    3. Calculate distance: d = EMA(abs(hlc3 - esa), channel_len)
    4. Calculate channel index: ci = (hlc3 - esa) / (0.015 * d)
    5. Calculate wt1: tci = EMA(ci, avg_len)
    6. Calculate wt2: signal line = SMA(wt1, 4)
    
    Args:
        df: DataFrame with OHLCV data
        channel_len: Channel length (default 9)
        avg_len: Average length (default 12)
        overbought: Overbought level (default 60)
        oversold: Oversold level (default -60)
        overbought2: Secondary overbought level (default 53)
        oversold2: Secondary oversold level (default -53)
        
    Returns:
        Tuple of (wt1, wt2, vwap) Series
    """
    try:
        # Step 1: Calculate typical price (hlc3)
        ap = hlc3(df)
        
        # Step 2: Calculate ESA (Exponential Simple Average)
        esa = ema(ap, channel_len)
        
        # Step 3: Calculate distance (d)
        d = ema(abs(ap - esa), channel_len)
        
        # Step 4: Calculate Channel Index (ci)
        # ci = (hlc3 - esa) / (0.015 * d)
        ci = (ap - esa) / (0.015 * d)
        
        # Step 5: Calculate wt1 (TCI - Trend Channel Index)
        wt1 = ema(ci, avg_len)
        
        # Step 6: Calculate wt2 (signal line)
        # Using SMA of 4 periods on wt1
        wt2 = wt1.rolling(window=4).mean()
        
        logger.debug(f"WaveTrend calculated: wt1 range [{wt1.min():.2f}, {wt1.max():.2f}]")
        
        return wt1, wt2, ap
        
    except Exception as e:
        logger.error(f"Error calculating WaveTrend: {e}")
        raise


def detect_wavetrend_signals(
    wt1: pd.Series,
    wt2: pd.Series,
    overbought: int = 60,
    oversold: int = -60
) -> Tuple[pd.Series, pd.Series]:
    """
    Detect buy/sell signals from WaveTrend crossovers.
    
    Buy signal: wt1 crosses above wt2 in oversold region
    Sell signal: wt1 crosses below wt2 in overbought region
    
    Args:
        wt1: WaveTrend line 1
        wt2: WaveTrend line 2
        overbought: Overbought threshold
        oversold: Oversold threshold
        
    Returns:
        Tuple of (buy_signals, sell_signals) boolean Series
    """
    # Detect crossovers
    cross_up = (wt1 > wt2) & (wt1.shift(1) <= wt2.shift(1))
    cross_down = (wt1 < wt2) & (wt1.shift(1) >= wt2.shift(1))
    
    # Buy signals: cross up in oversold region
    buy_signals = cross_up & (wt1 < oversold)
    
    # Sell signals: cross down in overbought region
    sell_signals = cross_down & (wt1 > overbought)
    
    logger.debug(f"WaveTrend signals: {buy_signals.sum()} buys, {sell_signals.sum()} sells")
    
    return buy_signals, sell_signals


def add_wavetrend(
    df: pd.DataFrame,
    channel_len: Optional[int] = None,
    avg_len: Optional[int] = None,
    overbought: Optional[int] = None,
    oversold: Optional[int] = None
) -> pd.DataFrame:
    """
    Add WaveTrend indicator to DataFrame.
    
    Args:
        df: DataFrame with OHLCV data
        channel_len: Channel length (uses config if None)
        avg_len: Average length (uses config if None)
        overbought: Overbought level (uses config if None)
        oversold: Oversold level (uses config if None)
        
    Returns:
        DataFrame with added columns: wt1, wt2, wt_buy, wt_sell
    """
    # Get parameters from config if not provided
    if any(p is None for p in [channel_len, avg_len, overbought, oversold]):
        params = get_indicator_params('wave_trend')
        channel_len = channel_len or params.get('channel_length', 9)
        avg_len = avg_len or params.get('average_length', 12)
        overbought = overbought or params.get('overbought_level', 60)
        oversold = oversold or params.get('oversold_level', -60)
    
    logger.info(f"Calculating WaveTrend: channel_len={channel_len}, avg_len={avg_len}")
    
    # Calculate WaveTrend
    wt1, wt2, _ = wavetrend(df, channel_len, avg_len, overbought, oversold)
    
    # Add to DataFrame
    df = df.copy()
    df['wt1'] = wt1
    df['wt2'] = wt2
    
    # Detect signals
    buy_signals, sell_signals = detect_wavetrend_signals(wt1, wt2, overbought, oversold)
    df['wt_buy'] = buy_signals
    df['wt_sell'] = sell_signals
    
    logger.info(f"✅ WaveTrend added: {len(df)} candles, {buy_signals.sum()} buy signals, {sell_signals.sum()} sell signals")
    
    return df


if __name__ == '__main__':
    """Test WaveTrend indicator."""
    print("=" * 70)
    print("📊 Testing WaveTrend Oscillator")
    print("=" * 70)
    
    # Import here to avoid circular dependencies
    from data_collection.binance_client import BinanceClient
    
    # Fetch BTC data
    print("\n📈 Fetching BTC/USDT 1h data...")
    client = BinanceClient()
    df = client.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=200)
    
    print(f"✅ Fetched {len(df)} candles")
    print(f"   Date range: {df.index[0]} to {df.index[-1]}")
    
    # Calculate WaveTrend
    print("\n🔬 Calculating WaveTrend indicator...")
    df = add_wavetrend(df, channel_len=9, avg_len=12, overbought=60, oversold=-60)
    
    # Display results
    print(f"\n✅ WaveTrend calculated!")
    print(f"   wt1 range: [{df['wt1'].min():.2f}, {df['wt1'].max():.2f}]")
    print(f"   wt2 range: [{df['wt2'].min():.2f}, {df['wt2'].max():.2f}]")
    print(f"   Buy signals: {df['wt_buy'].sum()}")
    print(f"   Sell signals: {df['wt_sell'].sum()}")
    
    # Show latest values
    print("\n📊 Latest WaveTrend values:")
    print(df[['close', 'wt1', 'wt2', 'wt_buy', 'wt_sell']].tail(10))
    
    # Show recent signals
    buy_signals = df[df['wt_buy']]
    sell_signals = df[df['wt_sell']]
    
    if not buy_signals.empty:
        print("\n🟢 Recent BUY signals:")
        print(buy_signals[['close', 'wt1', 'wt2']].tail(3))
    
    if not sell_signals.empty:
        print("\n🔴 Recent SELL signals:")
        print(sell_signals[['close', 'wt1', 'wt2']].tail(3))
    
    # Check current status
    latest = df.iloc[-1]
    print(f"\n📈 Current Status:")
    print(f"   Price: ${latest['close']:,.2f}")
    print(f"   wt1: {latest['wt1']:.2f}")
    print(f"   wt2: {latest['wt2']:.2f}")
    
    if latest['wt1'] < -60:
        print(f"   ⚠️  OVERSOLD territory!")
    elif latest['wt1'] > 60:
        print(f"   ⚠️  OVERBOUGHT territory!")
    else:
        print(f"   ℹ️  Neutral zone")
    
    print("\n" + "=" * 70)
    print("🎉 WaveTrend test completed successfully!")
    print("=" * 70)
