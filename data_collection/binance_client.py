"""
Binance API client for data collection.

Fetches OHLCV data and market information from Binance.
"""

import ccxt
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import time

from utils.logger import get_data_logger
from utils.config import get_config

logger = get_data_logger()


class BinanceClient:
    """Binance API client for fetching cryptocurrency data."""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Binance client.
        
        Args:
            api_key: Binance API key (optional for public endpoints)
            api_secret: Binance API secret (optional for public endpoints)
        """
        self.config = get_config()
        
        # Get API keys from config if not provided
        if api_key is None or api_secret is None:
            keys = self.config.get_api_keys()
            api_key = api_key or keys.get('api_key')
            api_secret = api_secret or keys.get('api_secret')
        
        # Initialize CCXT Binance client
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,  # Respect rate limits
            'options': {
                'defaultType': 'spot',  # Use spot market
            }
        })
        
        logger.info("✅ Binance client initialized")
    
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 500,
        since: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
            timeframe: Timeframe (e.g., '1m', '5m', '15m', '1h', '4h', '1d')
            limit: Number of candles to fetch (max 1000)
            since: Timestamp in milliseconds (optional)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            logger.info(f"📊 Fetching {symbol} {timeframe} data (limit={limit})")
            
            # Fetch data from Binance
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit,
                since=since
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Convert to float
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            logger.info(f"✅ Fetched {len(df)} candles for {symbol} {timeframe}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error fetching {symbol} {timeframe}: {str(e)}")
            raise
    
    def fetch_historical_data(
        self,
        symbol: str,
        timeframe: str = '1h',
        days: int = 30
    ) -> pd.DataFrame:
        """
        Fetch historical data for a specified number of days.
        
        Args:
            symbol: Trading pair symbol
            timeframe: Timeframe
            days: Number of days to fetch
            
        Returns:
            DataFrame with historical OHLCV data
        """
        try:
            logger.info(f"📅 Fetching {days} days of {symbol} {timeframe} data")
            
            # Calculate since timestamp
            since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
            
            all_data = []
            current_since = since
            
            while True:
                # Fetch batch
                df = self.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    limit=1000,
                    since=current_since
                )
                
                if df.empty:
                    break
                
                all_data.append(df)
                
                # Check if we have enough data
                last_timestamp = df.index[-1]
                if last_timestamp >= datetime.now() - timedelta(hours=1):
                    break
                
                # Update since for next batch
                current_since = int(last_timestamp.timestamp() * 1000) + 1
                
                # Rate limiting
                time.sleep(0.5)
            
            # Combine all data
            if all_data:
                result = pd.concat(all_data)
                result = result[~result.index.duplicated(keep='first')]
                result = result.sort_index()
                
                logger.info(f"✅ Fetched {len(result)} total candles for {symbol}")
                return result
            else:
                logger.warning(f"⚠️  No data found for {symbol}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ Error fetching historical data: {str(e)}")
            raise
    
    def fetch_multiple_symbols(
        self,
        symbols: List[str],
        timeframe: str = '1h',
        limit: int = 500
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple symbols.
        
        Args:
            symbols: List of trading pair symbols
            timeframe: Timeframe
            limit: Number of candles per symbol
            
        Returns:
            Dictionary mapping symbols to DataFrames
        """
        results = {}
        
        logger.info(f"🔄 Fetching data for {len(symbols)} symbols")
        
        for symbol in symbols:
            try:
                df = self.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    limit=limit
                )
                results[symbol] = df
                
                # Rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                logger.error(f"❌ Failed to fetch {symbol}: {str(e)}")
                results[symbol] = pd.DataFrame()
        
        logger.info(f"✅ Completed fetching {len(results)} symbols")
        return results
    
    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Get current ticker information.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Ticker information dictionary
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            logger.debug(f"📈 Ticker for {symbol}: ${ticker['last']:.2f}")
            return ticker
        except Exception as e:
            logger.error(f"❌ Error fetching ticker for {symbol}: {str(e)}")
            raise
    
    def get_market_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get market information for a symbol.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Market information dictionary
        """
        try:
            markets = self.exchange.load_markets()
            if symbol in markets:
                return markets[symbol]
            else:
                logger.warning(f"⚠️  Symbol {symbol} not found")
                return {}
        except Exception as e:
            logger.error(f"❌ Error fetching market info: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test connection to Binance API.
        
        Returns:
            True if connection successful
        """
        try:
            logger.info("🔌 Testing Binance connection...")
            
            # Fetch server time
            time_response = self.exchange.fetch_time()
            server_time = datetime.fromtimestamp(time_response / 1000)
            
            logger.info(f"✅ Connected to Binance! Server time: {server_time}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection test failed: {str(e)}")
            return False


if __name__ == '__main__':
    """Test Binance client."""
    print("=" * 70)
    print("🔗 Testing Binance Client")
    print("=" * 70)
    
    # Initialize client (uses API keys from .env or works without for public data)
    client = BinanceClient()
    
    # Test connection
    if client.test_connection():
        print("\n✅ Connection test passed!\n")
        
        # Fetch BTC/USDT data
        print("📊 Fetching BTC/USDT 1h data...")
        df = client.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
        
        print(f"\n📈 Fetched {len(df)} candles")
        print(f"   Date range: {df.index[0]} to {df.index[-1]}")
        print(f"   Latest close: ${df['close'].iloc[-1]:,.2f}")
        print(f"   High: ${df['high'].max():,.2f}")
        print(f"   Low: ${df['low'].min():,.2f}")
        
        print("\n📊 Sample data:")
        print(df.tail())
        
        # Get current ticker
        print("\n📈 Current ticker info:")
        ticker = client.get_ticker('BTC/USDT')
        print(f"   Price: ${ticker['last']:,.2f}")
        print(f"   24h Change: {ticker['percentage']:.2f}%")
        print(f"   24h Volume: {ticker['baseVolume']:,.2f} BTC")
        
        print("\n" + "=" * 70)
        print("🎉 Binance client test completed successfully!")
        print("=" * 70)
    else:
        print("\n❌ Connection test failed!")
