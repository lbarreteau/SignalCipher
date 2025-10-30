"""
Money Flow Index (MFI) Indicator.

MFI is a momentum indicator that uses both price and volume to measure
buying and selling pressure. It's similar to RSI but volume-weighted.

Key component of Market Cipher B for detecting money flow strength.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional

from utils.logger import get_indicator_logger
from utils.config import get_indicator_params

logger = get_indicator_logger()


def typical_price(df: pd.DataFrame) -> pd.Series:
    """
    Calculate typical price (HLC3).
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        
    Returns:
        Series with typical price values
    """
    return (df['high'] + df['low'] + df['close']) / 3


def raw_money_flow(df: pd.DataFrame) -> pd.Series:
    """
    Calculate raw money flow.
    
    Raw Money Flow = Typical Price * Volume
    
    Args:
        df: DataFrame with OHLCV data
        
    Returns:
        Series with raw money flow values
    """
    tp = typical_price(df)
    return tp * df['volume']


def money_flow_index(df: pd.DataFrame, period: int = 60) -> pd.Series:
    """
    Calculate Money Flow Index (MFI).
    
    MFI measures the strength of money flowing in and out of a security.
    Range: 0-100
    - MFI > 80: Overbought
    - MFI < 20: Oversold
    
    Formula:
    1. Calculate typical price: (high + low + close) / 3
    2. Calculate raw money flow: typical_price * volume
    3. Calculate positive and negative money flow over period
    4. Calculate money flow ratio: positive_flow / negative_flow
    5. Calculate MFI: 100 - (100 / (1 + money_ratio))
    
    Args:
        df: DataFrame with OHLCV data
        period: Lookback period (default 60 for Market Cipher B)
        
    Returns:
        Series with MFI values
    """
    try:
        tp = typical_price(df)
        rmf = raw_money_flow(df)
        
        # Determine positive and negative money flow
        positive_flow = pd.Series(0.0, index=df.index)
        negative_flow = pd.Series(0.0, index=df.index)
        
        # When typical price increases, it's positive money flow
        # When typical price decreases, it's negative money flow
        tp_diff = tp.diff()
        
        positive_flow = rmf.where(tp_diff > 0, 0)
        negative_flow = rmf.where(tp_diff < 0, 0)
        
        # Sum over the period
        positive_mf = positive_flow.rolling(window=period).sum()
        negative_mf = negative_flow.rolling(window=period).sum()
        
        # Calculate money flow ratio
        money_ratio = positive_mf / negative_mf
        
        # Calculate MFI
        mfi = 100 - (100 / (1 + money_ratio))
        
        # Handle division by zero
        mfi = mfi.fillna(50)  # Neutral value when no negative flow
        
        logger.debug(f"MFI calculated: range [{mfi.min():.2f}, {mfi.max():.2f}]")
        
        return mfi
        
    except Exception as e:
        logger.error(f"Error calculating MFI: {e}")
        raise


def detect_mfi_divergence(
    df: pd.DataFrame,
    mfi: pd.Series,
    lookback: int = 14
) -> Tuple[pd.Series, pd.Series]:
    """
    Detect bullish and bearish divergences in MFI.
    
    Bullish divergence: Price makes lower low, but MFI makes higher low
    Bearish divergence: Price makes higher high, but MFI makes lower high
    
    Args:
        df: DataFrame with price data
        mfi: MFI series
        lookback: Period to look back for divergence
        
    Returns:
        Tuple of (bullish_divergence, bearish_divergence) boolean Series
    """
    price = df['close']
    
    # Find local minima and maxima
    price_min = price.rolling(window=lookback, center=True).min() == price
    price_max = price.rolling(window=lookback, center=True).max() == price
    
    mfi_min = mfi.rolling(window=lookback, center=True).min() == mfi
    mfi_max = mfi.rolling(window=lookback, center=True).max() == mfi
    
    # Initialize divergence series
    bullish_div = pd.Series(False, index=df.index)
    bearish_div = pd.Series(False, index=df.index)
    
    # Detect divergences (simplified version)
    # In production, you'd want more sophisticated peak detection
    for i in range(lookback * 2, len(df)):
        # Bullish divergence
        if price_min.iloc[i]:
            # Look for previous low
            prev_lows = price_min.iloc[i-lookback*2:i]
            if prev_lows.any():
                prev_idx = prev_lows[::-1].idxmax()
                if price.iloc[i] < price.loc[prev_idx] and mfi.iloc[i] > mfi.loc[prev_idx]:
                    bullish_div.iloc[i] = True
        
        # Bearish divergence
        if price_max.iloc[i]:
            # Look for previous high
            prev_highs = price_max.iloc[i-lookback*2:i]
            if prev_highs.any():
                prev_idx = prev_highs[::-1].idxmax()
                if price.iloc[i] > price.loc[prev_idx] and mfi.iloc[i] < mfi.loc[prev_idx]:
                    bearish_div.iloc[i] = True
    
    logger.debug(f"MFI divergences: {bullish_div.sum()} bullish, {bearish_div.sum()} bearish")
    
    return bullish_div, bearish_div


def detect_mfi_signals(
    mfi: pd.Series,
    overbought: int = 80,
    oversold: int = 20
) -> Tuple[pd.Series, pd.Series]:
    """
    Detect buy/sell signals from MFI levels.
    
    Args:
        mfi: MFI series
        overbought: Overbought threshold (default 80)
        oversold: Oversold threshold (default 20)
        
    Returns:
        Tuple of (buy_signals, sell_signals) boolean Series
    """
    # Buy signal: MFI crosses above oversold level
    buy_signals = (mfi > oversold) & (mfi.shift(1) <= oversold)
    
    # Sell signal: MFI crosses below overbought level
    sell_signals = (mfi < overbought) & (mfi.shift(1) >= overbought)
    
    logger.debug(f"MFI signals: {buy_signals.sum()} buys, {sell_signals.sum()} sells")
    
    return buy_signals, sell_signals


def add_money_flow(
    df: pd.DataFrame,
    period: Optional[int] = None,
    overbought: Optional[int] = None,
    oversold: Optional[int] = None
) -> pd.DataFrame:
    """
    Add Money Flow Index indicator to DataFrame.
    
    Args:
        df: DataFrame with OHLCV data
        period: MFI period (uses config if None)
        overbought: Overbought level (uses config if None)
        oversold: Oversold level (uses config if None)
        
    Returns:
        DataFrame with added columns: mfi, mfi_buy, mfi_sell, mfi_bullish_div, mfi_bearish_div
    """
    # Get parameters from config if not provided
    if any(p is None for p in [period, overbought, oversold]):
        params = get_indicator_params('money_flow')
        period = period or params.get('period', 60)
        overbought = overbought or params.get('overbought_level', 80)
        oversold = oversold or params.get('oversold_level', 20)
    
    logger.info(f"Calculating Money Flow Index: period={period}")
    
    # Calculate MFI
    mfi = money_flow_index(df, period)
    
    # Add to DataFrame
    df = df.copy()
    df['mfi'] = mfi
    
    # Detect signals
    buy_signals, sell_signals = detect_mfi_signals(mfi, overbought, oversold)
    df['mfi_buy'] = buy_signals
    df['mfi_sell'] = sell_signals
    
    # Detect divergences
    bullish_div, bearish_div = detect_mfi_divergence(df, mfi)
    df['mfi_bullish_div'] = bullish_div
    df['mfi_bearish_div'] = bearish_div
    
    logger.info(
        f"✅ MFI added: {len(df)} candles, {buy_signals.sum()} buy signals, "
        f"{sell_signals.sum()} sell signals, {bullish_div.sum()} bullish divergences"
    )
    
    return df


if __name__ == '__main__':
    """Test Money Flow Index indicator."""
    print("=" * 70)
    print("💰 Testing Money Flow Index (MFI)")
    print("=" * 70)
    
    # Import here to avoid circular dependencies
    from data_collection.binance_client import BinanceClient
    
    # Fetch BTC data
    print("\n📈 Fetching BTC/USDT 1h data...")
    client = BinanceClient()
    df = client.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=200)
    
    print(f"✅ Fetched {len(df)} candles")
    print(f"   Date range: {df.index[0]} to {df.index[-1]}")
    
    # Calculate MFI
    print("\n🔬 Calculating Money Flow Index...")
    df = add_money_flow(df, period=60, overbought=80, oversold=20)
    
    # Display results
    print(f"\n✅ MFI calculated!")
    print(f"   MFI range: [{df['mfi'].min():.2f}, {df['mfi'].max():.2f}]")
    print(f"   Buy signals: {df['mfi_buy'].sum()}")
    print(f"   Sell signals: {df['mfi_sell'].sum()}")
    print(f"   Bullish divergences: {df['mfi_bullish_div'].sum()}")
    print(f"   Bearish divergences: {df['mfi_bearish_div'].sum()}")
    
    # Show latest values
    print("\n📊 Latest MFI values:")
    print(df[['close', 'volume', 'mfi', 'mfi_buy', 'mfi_sell']].tail(10))
    
    # Show recent signals
    buy_signals = df[df['mfi_buy']]
    sell_signals = df[df['mfi_sell']]
    
    if not buy_signals.empty:
        print("\n🟢 Recent BUY signals (MFI crossing above oversold):")
        print(buy_signals[['close', 'mfi']].tail(3))
    
    if not sell_signals.empty:
        print("\n🔴 Recent SELL signals (MFI crossing below overbought):")
        print(sell_signals[['close', 'mfi']].tail(3))
    
    # Show divergences
    bullish_divs = df[df['mfi_bullish_div']]
    bearish_divs = df[df['mfi_bearish_div']]
    
    if not bullish_divs.empty:
        print("\n🟢 Bullish divergences detected:")
        print(bullish_divs[['close', 'mfi']].tail(2))
    
    if not bearish_divs.empty:
        print("\n🔴 Bearish divergences detected:")
        print(bearish_divs[['close', 'mfi']].tail(2))
    
    # Check current status
    latest = df.iloc[-1]
    print(f"\n📈 Current Status:")
    print(f"   Price: ${latest['close']:,.2f}")
    print(f"   Volume: {latest['volume']:,.2f} BTC")
    print(f"   MFI: {latest['mfi']:.2f}")
    
    if latest['mfi'] > 80:
        print(f"   ⚠️  OVERBOUGHT territory (strong selling pressure)!")
    elif latest['mfi'] < 20:
        print(f"   ⚠️  OVERSOLD territory (strong buying pressure)!")
    elif latest['mfi'] > 70:
        print(f"   📈 High buying pressure")
    elif latest['mfi'] < 30:
        print(f"   📉 High selling pressure")
    else:
        print(f"   ℹ️  Neutral money flow")
    
    print("\n" + "=" * 70)
    print("🎉 Money Flow Index test completed successfully!")
    print("=" * 70)
