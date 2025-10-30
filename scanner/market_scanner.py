"""
Market Scanner - Combines all indicators for comprehensive analysis.

Scans multiple cryptocurrencies across different timeframes using:
- WaveTrend Oscillator
- Money Flow Index (MFI)
- RSI & Stochastic RSI

Provides aggregated signals and scoring.
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from utils.logger import get_scanner_logger
from utils.config import get_config, get_top_symbols, get_active_timeframes
from data_collection.binance_client import BinanceClient
from indicators.wavetrend import add_wavetrend
from indicators.money_flow import add_money_flow
from indicators.rsi import add_rsi, add_stochastic_rsi

logger = get_scanner_logger()


class MarketScanner:
    """
    Scanner for analyzing multiple cryptocurrencies with all indicators.
    """
    
    def __init__(self):
        """Initialize market scanner."""
        self.config = get_config()
        self.client = BinanceClient()
        logger.info("✅ Market Scanner initialized")
    
    def scan_symbol(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 200
    ) -> pd.DataFrame:
        """
        Scan a single symbol with all indicators.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe to analyze
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with all indicators calculated
        """
        try:
            logger.info(f"🔍 Scanning {symbol} {timeframe}...")
            
            # Fetch data
            df = self.client.fetch_ohlcv(symbol, timeframe, limit)
            
            if df.empty:
                logger.warning(f"No data for {symbol}")
                return df
            
            # Add all indicators
            df = add_wavetrend(df)
            df = add_money_flow(df)
            df = add_rsi(df)
            df = add_stochastic_rsi(df)
            
            logger.info(f"✅ {symbol} scan completed")
            
            return df
            
        except Exception as e:
            logger.error(f"Error scanning {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_signal_score(self, row: pd.Series) -> Tuple[int, str]:
        """
        Calculate aggregated signal score from all indicators.
        
        Score ranges from -5 (strong sell) to +5 (strong buy):
        - WaveTrend: -2 to +2
        - MFI: -1 to +1
        - RSI: -1 to +1
        - StochRSI: -1 to +1
        
        Args:
            row: DataFrame row with indicator values
            
        Returns:
            Tuple of (score, signal_type)
        """
        score = 0
        
        # WaveTrend signals (weight: 2)
        if row.get('wt_buy', False):
            score += 2
        elif row.get('wt_sell', False):
            score -= 2
        elif row['wt1'] < -60:  # Oversold
            score += 1
        elif row['wt1'] > 60:  # Overbought
            score -= 1
        
        # MFI signals (weight: 1)
        if row.get('mfi_buy', False):
            score += 1
        elif row.get('mfi_sell', False):
            score -= 1
        elif row['mfi'] < 20:  # Oversold
            score += 0.5
        elif row['mfi'] > 80:  # Overbought
            score -= 0.5
        
        # RSI signals (weight: 1)
        if row.get('rsi_buy', False):
            score += 1
        elif row.get('rsi_sell', False):
            score -= 1
        elif row['rsi'] < 30:  # Oversold
            score += 0.5
        elif row['rsi'] > 70:  # Overbought
            score -= 0.5
        
        # StochRSI signals (weight: 1)
        if row.get('stoch_buy', False):
            score += 1
        elif row.get('stoch_sell', False):
            score -= 1
        elif row['stoch_k'] < 20:  # Oversold
            score += 0.5
        elif row['stoch_k'] > 80:  # Overbought
            score -= 0.5
        
        # Determine signal type
        if score >= 3:
            signal_type = "STRONG BUY"
        elif score >= 1.5:
            signal_type = "BUY"
        elif score <= -3:
            signal_type = "STRONG SELL"
        elif score <= -1.5:
            signal_type = "SELL"
        else:
            signal_type = "NEUTRAL"
        
        return score, signal_type
    
    def get_latest_signals(self, df: pd.DataFrame, symbol: str) -> Dict:
        """
        Extract latest signals from analyzed DataFrame.
        
        Args:
            df: DataFrame with indicators
            symbol: Symbol name
            
        Returns:
            Dictionary with signal information
        """
        if df.empty:
            return {}
        
        latest = df.iloc[-1]
        score, signal_type = self.calculate_signal_score(latest)
        
        return {
            'symbol': symbol,
            'timestamp': latest.name,
            'price': latest['close'],
            'signal_score': score,
            'signal_type': signal_type,
            'wt1': latest['wt1'],
            'wt2': latest['wt2'],
            'mfi': latest['mfi'],
            'rsi': latest['rsi'],
            'stoch_k': latest['stoch_k'],
            'stoch_d': latest['stoch_d'],
            'wt_buy': latest.get('wt_buy', False),
            'wt_sell': latest.get('wt_sell', False),
            'volume': latest['volume']
        }
    
    def scan_multiple_symbols(
        self,
        symbols: Optional[List[str]] = None,
        timeframe: str = '1h',
        limit: int = 200
    ) -> pd.DataFrame:
        """
        Scan multiple symbols and return aggregated results.
        
        Args:
            symbols: List of symbols (uses config default if None)
            timeframe: Timeframe to analyze
            limit: Number of candles per symbol
            
        Returns:
            DataFrame with results for all symbols
        """
        if symbols is None:
            symbols = get_top_symbols()
        
        logger.info(f"🔍 Scanning {len(symbols)} symbols on {timeframe} timeframe")
        
        results = []
        
        for symbol in symbols:
            try:
                # Scan symbol
                df = self.scan_symbol(symbol, timeframe, limit)
                
                if not df.empty:
                    # Get latest signals
                    signals = self.get_latest_signals(df, symbol)
                    results.append(signals)
                
            except Exception as e:
                logger.error(f"Failed to scan {symbol}: {e}")
                continue
        
        # Create results DataFrame
        if results:
            results_df = pd.DataFrame(results)
            results_df = results_df.sort_values('signal_score', ascending=False)
            logger.info(f"✅ Scan completed: {len(results_df)} symbols analyzed")
            return results_df
        else:
            logger.warning("No results from scan")
            return pd.DataFrame()
    
    def find_opportunities(
        self,
        min_score: float = 2.0,
        timeframe: str = '1h'
    ) -> pd.DataFrame:
        """
        Find trading opportunities based on signal scores.
        
        Args:
            min_score: Minimum absolute signal score
            timeframe: Timeframe to scan
            
        Returns:
            DataFrame with strong opportunities
        """
        logger.info(f"🎯 Finding opportunities with |score| >= {min_score}")
        
        # Scan all symbols
        results = self.scan_multiple_symbols(timeframe=timeframe)
        
        if results.empty:
            return results
        
        # Filter by score
        opportunities = results[abs(results['signal_score']) >= min_score]
        
        logger.info(f"✅ Found {len(opportunities)} opportunities")
        
        return opportunities


if __name__ == '__main__':
    """Test market scanner."""
    print("=" * 70)
    print("🔍 Market Scanner - Multi-Symbol Analysis")
    print("=" * 70)
    
    # Initialize scanner
    scanner = MarketScanner()
    
    # Test single symbol scan
    print("\n📊 Testing single symbol scan (BTC/USDT)...")
    df = scanner.scan_symbol('BTC/USDT', timeframe='1h', limit=200)
    
    if not df.empty:
        signals = scanner.get_latest_signals(df, 'BTC/USDT')
        
        print(f"\n✅ BTC/USDT Analysis:")
        print(f"   Price: ${signals['price']:,.2f}")
        print(f"   Signal Score: {signals['signal_score']:.1f}")
        print(f"   Signal Type: {signals['signal_type']}")
        print(f"   WaveTrend: wt1={signals['wt1']:.2f}, wt2={signals['wt2']:.2f}")
        print(f"   MFI: {signals['mfi']:.2f}")
        print(f"   RSI: {signals['rsi']:.2f}")
        print(f"   StochRSI: K={signals['stoch_k']:.2f}, D={signals['stoch_d']:.2f}")
    
    # Test multiple symbols scan
    print("\n\n🔍 Scanning top cryptocurrencies...")
    symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']
    results = scanner.scan_multiple_symbols(symbols=symbols, timeframe='1h')
    
    if not results.empty:
        print(f"\n✅ Scan Results ({len(results)} symbols):")
        print("\n" + "=" * 70)
        
        # Display results
        for _, row in results.iterrows():
            print(f"\n{row['symbol']}")
            print(f"  Price: ${row['price']:,.2f}")
            print(f"  Score: {row['signal_score']:.1f} ({row['signal_type']})")
            print(f"  WT1: {row['wt1']:>6.2f}  MFI: {row['mfi']:>5.2f}  RSI: {row['rsi']:>5.2f}  StochK: {row['stoch_k']:>5.2f}")
            
            if row['wt_buy']:
                print(f"  🟢 WaveTrend BUY signal!")
            elif row['wt_sell']:
                print(f"  🔴 WaveTrend SELL signal!")
        
        print("\n" + "=" * 70)
        
        # Find strong opportunities
        print("\n🎯 Strong Trading Opportunities (|score| >= 2.0):")
        opportunities = results[abs(results['signal_score']) >= 2.0]
        
        if not opportunities.empty:
            print(f"\nFound {len(opportunities)} strong signals:\n")
            
            for _, opp in opportunities.iterrows():
                emoji = "🟢" if opp['signal_score'] > 0 else "🔴"
                print(f"{emoji} {opp['symbol']:<12} Score: {opp['signal_score']:>5.1f}  {opp['signal_type']:<12}  ${opp['price']:>10,.2f}")
        else:
            print("  No strong opportunities at the moment")
    
    print("\n" + "=" * 70)
    print("🎉 Market Scanner test completed successfully!")
    print("=" * 70)
