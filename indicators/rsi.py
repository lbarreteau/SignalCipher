"""
RSI (Relative Strength Index) Indicator.

RSI is a momentum oscillator that measures the speed and magnitude
of recent price changes to evaluate overbought or oversold conditions.

Part of Market Cipher B indicator suite.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional

from utils.logger import get_indicator_logger
from utils.config import get_indicator_params

logger = get_indicator_logger()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    RSI = 100 - (100 / (1 + RS))
    where RS = Average Gain / Average Loss
    
    Range: 0-100
    - RSI > 70: Overbought
    - RSI < 30: Oversold
    
    Args:
        series: Price series (usually close prices)
        period: RSI period (default 14)
        
    Returns:
        Series with RSI values
    """
    try:
        # Calculate price changes
        delta = series.diff()
        
        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Calculate average gain and loss using EMA (Wilder's smoothing)
        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi_values = 100 - (100 / (1 + rs))
        
        # Handle division by zero
        rsi_values = rsi_values.fillna(50)
        
        logger.debug(f"RSI calculated: range [{rsi_values.min():.2f}, {rsi_values.max():.2f}]")
        
        return rsi_values
        
    except Exception as e:
        logger.error(f"Error calculating RSI: {e}")
        raise


def stochastic_rsi(
    series: pd.Series,
    rsi_period: int = 14,
    stoch_period: int = 14,
    k_smooth: int = 3,
    d_smooth: int = 3
) -> Tuple[pd.Series, pd.Series]:
    """
    Calculate Stochastic RSI (StochRSI).
    
    StochRSI applies the Stochastic oscillator formula to RSI values
    instead of price, making it more sensitive to RSI movements.
    
    Formula:
    1. Calculate RSI
    2. StochRSI = (RSI - RSI_Low) / (RSI_High - RSI_Low)
    3. %K = SMA(StochRSI, k_smooth)
    4. %D = SMA(%K, d_smooth)
    
    Args:
        series: Price series
        rsi_period: Period for RSI calculation
        stoch_period: Period for Stochastic calculation
        k_smooth: Smoothing period for %K
        d_smooth: Smoothing period for %D
        
    Returns:
        Tuple of (%K, %D) Series
    """
    try:
        # Calculate RSI
        rsi_values = rsi(series, rsi_period)
        
        # Calculate Stochastic of RSI
        rsi_low = rsi_values.rolling(window=stoch_period).min()
        rsi_high = rsi_values.rolling(window=stoch_period).max()
        
        stoch_rsi = (rsi_values - rsi_low) / (rsi_high - rsi_low)
        stoch_rsi = stoch_rsi.fillna(0.5)  # Neutral value
        
        # Scale to 0-100
        stoch_rsi = stoch_rsi * 100
        
        # Calculate %K (smoothed StochRSI)
        k = stoch_rsi.rolling(window=k_smooth).mean()
        
        # Calculate %D (signal line - smoothed %K)
        d = k.rolling(window=d_smooth).mean()
        
        logger.debug(f"StochRSI calculated: K range [{k.min():.2f}, {k.max():.2f}]")
        
        return k, d
        
    except Exception as e:
        logger.error(f"Error calculating StochRSI: {e}")
        raise


def detect_rsi_signals(
    rsi_values: pd.Series,
    overbought: int = 70,
    oversold: int = 30
) -> Tuple[pd.Series, pd.Series]:
    """
    Detect buy/sell signals from RSI levels.
    
    Args:
        rsi_values: RSI series
        overbought: Overbought threshold (default 70)
        oversold: Oversold threshold (default 30)
        
    Returns:
        Tuple of (buy_signals, sell_signals) boolean Series
    """
    # Buy signal: RSI crosses above oversold level
    buy_signals = (rsi_values > oversold) & (rsi_values.shift(1) <= oversold)
    
    # Sell signal: RSI crosses below overbought level
    sell_signals = (rsi_values < overbought) & (rsi_values.shift(1) >= overbought)
    
    logger.debug(f"RSI signals: {buy_signals.sum()} buys, {sell_signals.sum()} sells")
    
    return buy_signals, sell_signals


def detect_stochrsi_signals(
    k: pd.Series,
    d: pd.Series,
    overbought: int = 80,
    oversold: int = 20
) -> Tuple[pd.Series, pd.Series]:
    """
    Detect buy/sell signals from StochRSI crossovers.
    
    Buy signal: %K crosses above %D in oversold region
    Sell signal: %K crosses below %D in overbought region
    
    Args:
        k: StochRSI %K series
        d: StochRSI %D series
        overbought: Overbought threshold (default 80)
        oversold: Oversold threshold (default 20)
        
    Returns:
        Tuple of (buy_signals, sell_signals) boolean Series
    """
    # Detect crossovers
    cross_up = (k > d) & (k.shift(1) <= d.shift(1))
    cross_down = (k < d) & (k.shift(1) >= d.shift(1))
    
    # Buy signals: cross up in oversold region
    buy_signals = cross_up & (k < oversold)
    
    # Sell signals: cross down in overbought region
    sell_signals = cross_down & (k > overbought)
    
    logger.debug(f"StochRSI signals: {buy_signals.sum()} buys, {sell_signals.sum()} sells")
    
    return buy_signals, sell_signals


def add_rsi(
    df: pd.DataFrame,
    period: Optional[int] = None,
    overbought: Optional[int] = None,
    oversold: Optional[int] = None
) -> pd.DataFrame:
    """
    Add RSI indicator to DataFrame.
    
    Args:
        df: DataFrame with OHLCV data
        period: RSI period (uses config if None)
        overbought: Overbought level (uses config if None)
        oversold: Oversold level (uses config if None)
        
    Returns:
        DataFrame with added columns: rsi, rsi_buy, rsi_sell
    """
    # Get parameters from config if not provided
    if any(p is None for p in [period, overbought, oversold]):
        params = get_indicator_params('rsi')
        period = period or params.get('length', 14)
        overbought = overbought or params.get('overbought_level', 70)
        oversold = oversold or params.get('oversold_level', 30)
    
    logger.info(f"Calculating RSI: period={period}")
    
    # Calculate RSI
    rsi_values = rsi(df['close'], period)
    
    # Add to DataFrame
    df = df.copy()
    df['rsi'] = rsi_values
    
    # Detect signals
    buy_signals, sell_signals = detect_rsi_signals(rsi_values, overbought, oversold)
    df['rsi_buy'] = buy_signals
    df['rsi_sell'] = sell_signals
    
    logger.info(
        f"✅ RSI added: {len(df)} candles, {buy_signals.sum()} buy signals, "
        f"{sell_signals.sum()} sell signals"
    )
    
    return df


def add_stochastic_rsi(
    df: pd.DataFrame,
    rsi_period: Optional[int] = None,
    stoch_period: Optional[int] = None,
    k_smooth: Optional[int] = None,
    d_smooth: Optional[int] = None
) -> pd.DataFrame:
    """
    Add Stochastic RSI indicator to DataFrame.
    
    Args:
        df: DataFrame with OHLCV data
        rsi_period: RSI period (uses config if None)
        stoch_period: Stochastic period (uses config if None)
        k_smooth: %K smoothing (uses config if None)
        d_smooth: %D smoothing (uses config if None)
        
    Returns:
        DataFrame with added columns: stoch_k, stoch_d, stoch_buy, stoch_sell
    """
    # Get parameters from config if not provided
    if any(p is None for p in [rsi_period, stoch_period, k_smooth, d_smooth]):
        params = get_indicator_params('stochastic_rsi')
        rsi_period = rsi_period or params.get('rsi_length', 14)
        stoch_period = stoch_period or params.get('stoch_length', 14)
        k_smooth = k_smooth or params.get('k_smooth', 3)
        d_smooth = d_smooth or params.get('d_smooth', 3)
    
    logger.info(f"Calculating Stochastic RSI: rsi_period={rsi_period}, stoch_period={stoch_period}")
    
    # Calculate StochRSI
    k, d = stochastic_rsi(df['close'], rsi_period, stoch_period, k_smooth, d_smooth)
    
    # Add to DataFrame
    df = df.copy()
    df['stoch_k'] = k
    df['stoch_d'] = d
    
    # Detect signals
    buy_signals, sell_signals = detect_stochrsi_signals(k, d)
    df['stoch_buy'] = buy_signals
    df['stoch_sell'] = sell_signals
    
    logger.info(
        f"✅ StochRSI added: {len(df)} candles, {buy_signals.sum()} buy signals, "
        f"{sell_signals.sum()} sell signals"
    )
    
    return df


if __name__ == '__main__':
    """Test RSI and Stochastic RSI indicators."""
    print("=" * 70)
    print("📊 Testing RSI & Stochastic RSI")
    print("=" * 70)
    
    # Import here to avoid circular dependencies
    from data_collection.binance_client import BinanceClient
    
    # Fetch BTC data
    print("\n📈 Fetching BTC/USDT 1h data...")
    client = BinanceClient()
    df = client.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=200)
    
    print(f"✅ Fetched {len(df)} candles")
    print(f"   Date range: {df.index[0]} to {df.index[-1]}")
    
    # Calculate RSI
    print("\n🔬 Calculating RSI...")
    df = add_rsi(df, period=14, overbought=70, oversold=30)
    
    # Calculate Stochastic RSI
    print("\n🔬 Calculating Stochastic RSI...")
    df = add_stochastic_rsi(df, rsi_period=14, stoch_period=14, k_smooth=3, d_smooth=3)
    
    # Display results
    print(f"\n✅ Indicators calculated!")
    print(f"   RSI range: [{df['rsi'].min():.2f}, {df['rsi'].max():.2f}]")
    print(f"   RSI buy signals: {df['rsi_buy'].sum()}")
    print(f"   RSI sell signals: {df['rsi_sell'].sum()}")
    print(f"   StochRSI %K range: [{df['stoch_k'].min():.2f}, {df['stoch_k'].max():.2f}]")
    print(f"   StochRSI buy signals: {df['stoch_buy'].sum()}")
    print(f"   StochRSI sell signals: {df['stoch_sell'].sum()}")
    
    # Show latest values
    print("\n📊 Latest RSI values:")
    print(df[['close', 'rsi', 'stoch_k', 'stoch_d']].tail(10))
    
    # Show recent RSI signals
    rsi_buys = df[df['rsi_buy']]
    rsi_sells = df[df['rsi_sell']]
    
    if not rsi_buys.empty:
        print("\n🟢 Recent RSI BUY signals:")
        print(rsi_buys[['close', 'rsi']].tail(3))
    
    if not rsi_sells.empty:
        print("\n🔴 Recent RSI SELL signals:")
        print(rsi_sells[['close', 'rsi']].tail(3))
    
    # Show recent StochRSI signals
    stoch_buys = df[df['stoch_buy']]
    stoch_sells = df[df['stoch_sell']]
    
    if not stoch_buys.empty:
        print("\n🟢 Recent StochRSI BUY signals:")
        print(stoch_buys[['close', 'stoch_k', 'stoch_d']].tail(3))
    
    if not stoch_sells.empty:
        print("\n🔴 Recent StochRSI SELL signals:")
        print(stoch_sells[['close', 'stoch_k', 'stoch_d']].tail(3))
    
    # Check current status
    latest = df.iloc[-1]
    print(f"\n📈 Current Status:")
    print(f"   Price: ${latest['close']:,.2f}")
    print(f"   RSI: {latest['rsi']:.2f}", end="")
    
    if latest['rsi'] > 70:
        print(f" - ⚠️  OVERBOUGHT")
    elif latest['rsi'] < 30:
        print(f" - ⚠️  OVERSOLD")
    else:
        print(f" - ℹ️  Neutral")
    
    print(f"   StochRSI %K: {latest['stoch_k']:.2f}", end="")
    
    if latest['stoch_k'] > 80:
        print(f" - ⚠️  OVERBOUGHT")
    elif latest['stoch_k'] < 20:
        print(f" - ⚠️  OVERSOLD")
    else:
        print(f" - ℹ️  Neutral")
    
    print(f"   StochRSI %D: {latest['stoch_d']:.2f}")
    
    print("\n" + "=" * 70)
    print("🎉 RSI & StochRSI test completed successfully!")
    print("=" * 70)
