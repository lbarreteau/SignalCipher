"""
Real-time Signal Generator.

Combines all indicators and ML model to generate trading signals in real-time.
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime

from utils.logger import get_logger
from utils.config import get_config, get_top_symbols
from data_collection.binance_client import BinanceClient
from scanner.market_scanner import MarketScanner
from ml_models.money_flow_classifier import MoneyFlowClassifier
from ml_models.feature_engineering import FeatureEngineering

logger = get_logger('signals')


class SignalGenerator:
    """
    Real-time signal generator combining indicators and ML models.
    """
    
    def __init__(self, use_ml: bool = True):
        """
        Initialize signal generator.
        
        Args:
            use_ml: Whether to use ML model for predictions
        """
        self.config = get_config()
        self.client = BinanceClient()
        self.scanner = MarketScanner()
        self.use_ml = use_ml
        
        # Load ML model if available
        self.ml_model = None
        if use_ml:
            try:
                self.ml_model = MoneyFlowClassifier()
                self.ml_model.load('models/money_flow_classifier.pkl')
                logger.info("✅ ML model loaded")
            except Exception as e:
                logger.warning(f"Could not load ML model: {e}")
                self.use_ml = False
        
        self.fe = FeatureEngineering()
        
        logger.info("✅ Signal Generator initialized")
    
    def generate_signal(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 200
    ) -> Dict:
        """
        Generate comprehensive signal for a symbol.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe
            limit: Number of candles to fetch
            
        Returns:
            Dictionary with signal information
        """
        try:
            # Scan symbol with all indicators
            df = self.scanner.scan_symbol(symbol, timeframe, limit)
            
            if df.empty:
                return {'error': f'No data for {symbol}'}
            
            # Get latest indicator signals
            latest = df.iloc[-1]
            signals = self.scanner.get_latest_signals(df, symbol)
            
            # Add ML prediction if available
            ml_signal = None
            ml_probability = None
            
            if self.use_ml and self.ml_model:
                try:
                    # Engineer features for ML
                    df_features = self.fe.engineer_all_features(df, include_indicators=False)
                    
                    # Get latest features
                    X_latest = df_features[self.fe.feature_columns].iloc[-1:].fillna(0)
                    
                    # Predict
                    ml_signal = int(self.ml_model.predict(X_latest)[0])
                    ml_probability = float(self.ml_model.predict_proba(X_latest)[0])
                    
                except Exception as e:
                    logger.warning(f"ML prediction failed for {symbol}: {e}")
            
            # Calculate final signal
            final_score = signals['signal_score']
            
            if ml_signal == 1 and ml_probability > 0.6:
                final_score += 1.0  # Boost score with ML confirmation
            
            # Determine final signal type
            if final_score >= 3:
                final_signal = "STRONG BUY"
            elif final_score >= 1.5:
                final_signal = "BUY"
            elif final_score <= -3:
                final_signal = "STRONG SELL"
            elif final_score <= -1.5:
                final_signal = "SELL"
            else:
                final_signal = "NEUTRAL"
            
            # Build signal dictionary
            signal_data = {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'price': signals['price'],
                'timeframe': timeframe,
                
                # Indicator signals
                'indicator_score': signals['signal_score'],
                'indicator_signal': signals['signal_type'],
                
                # Individual indicators
                'wavetrend': {
                    'wt1': signals['wt1'],
                    'wt2': signals['wt2'],
                    'buy_signal': bool(signals['wt_buy']),
                    'sell_signal': bool(signals['wt_sell'])
                },
                'mfi': {
                    'value': signals['mfi'],
                    'oversold': signals['mfi'] < 20,
                    'overbought': signals['mfi'] > 80
                },
                'rsi': {
                    'value': signals['rsi'],
                    'oversold': signals['rsi'] < 30,
                    'overbought': signals['rsi'] > 70
                },
                'stoch_rsi': {
                    'k': signals['stoch_k'],
                    'd': signals['stoch_d'],
                    'oversold': signals['stoch_k'] < 20,
                    'overbought': signals['stoch_k'] > 80
                },
                
                # ML prediction
                'ml_prediction': {
                    'signal': ml_signal,
                    'probability': ml_probability,
                    'enabled': self.use_ml
                } if self.use_ml else None,
                
                # Final signal
                'final_score': final_score,
                'final_signal': final_signal,
                'confidence': self._calculate_confidence(signals, ml_signal, ml_probability)
            }
            
            logger.info(f"✅ Signal generated for {symbol}: {final_signal} (score: {final_score:.1f})")
            
            return signal_data
            
        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {e}")
            return {'error': str(e)}
    
    def _calculate_confidence(
        self,
        signals: Dict,
        ml_signal: Optional[int],
        ml_probability: Optional[float]
    ) -> float:
        """
        Calculate confidence level for the signal.
        
        Args:
            signals: Indicator signals
            ml_signal: ML prediction
            ml_probability: ML probability
            
        Returns:
            Confidence score (0-1)
        """
        confidence = 0.5  # Base confidence
        
        # Boost confidence if multiple indicators agree
        oversold_count = sum([
            signals['wt1'] < -60,
            signals['mfi'] < 20,
            signals['rsi'] < 30,
            signals['stoch_k'] < 20
        ])
        
        overbought_count = sum([
            signals['wt1'] > 60,
            signals['mfi'] > 80,
            signals['rsi'] > 70,
            signals['stoch_k'] > 80
        ])
        
        # More agreeing indicators = higher confidence
        max_agreement = max(oversold_count, overbought_count)
        confidence += (max_agreement / 4) * 0.3  # Up to 0.3 boost
        
        # ML confirmation adds confidence
        if ml_signal is not None and ml_probability is not None:
            if ml_probability > 0.7:
                confidence += 0.2
            elif ml_probability > 0.5:
                confidence += 0.1
        
        return min(confidence, 1.0)
    
    def scan_all_symbols(
        self,
        symbols: Optional[List[str]] = None,
        timeframe: str = '1h'
    ) -> pd.DataFrame:
        """
        Generate signals for multiple symbols.
        
        Args:
            symbols: List of symbols (uses config default if None)
            timeframe: Timeframe to analyze
            
        Returns:
            DataFrame with signals for all symbols
        """
        if symbols is None:
            symbols = get_top_symbols()
        
        logger.info(f"🔍 Generating signals for {len(symbols)} symbols...")
        
        results = []
        
        for symbol in symbols:
            signal = self.generate_signal(symbol, timeframe)
            
            if 'error' not in signal:
                results.append(signal)
        
        if results:
            # Convert to DataFrame
            df_results = pd.DataFrame([{
                'symbol': s['symbol'],
                'price': s['price'],
                'final_signal': s['final_signal'],
                'final_score': s['final_score'],
                'confidence': s['confidence'],
                'wt1': s['wavetrend']['wt1'],
                'mfi': s['mfi']['value'],
                'rsi': s['rsi']['value'],
                'ml_prob': s['ml_prediction']['probability'] if s['ml_prediction'] else None
            } for s in results])
            
            df_results = df_results.sort_values('final_score', ascending=False)
            
            logger.info(f"✅ Signals generated for {len(results)} symbols")
            
            return df_results
        else:
            logger.warning("No signals generated")
            return pd.DataFrame()


if __name__ == '__main__':
    """Test signal generator."""
    print("=" * 70)
    print("🎯 Real-time Signal Generator")
    print("=" * 70)
    
    # Initialize signal generator
    print("\n🚀 Initializing Signal Generator...")
    generator = SignalGenerator(use_ml=True)
    
    # Generate signal for BTC
    print("\n📊 Generating signal for BTC/USDT...")
    btc_signal = generator.generate_signal('BTC/USDT', timeframe='1h')
    
    if 'error' not in btc_signal:
        print(f"\n✅ BTC/USDT Signal Generated:")
        print(f"   Price: ${btc_signal['price']:,.2f}")
        print(f"   Final Signal: {btc_signal['final_signal']}")
        print(f"   Final Score: {btc_signal['final_score']:.1f}")
        print(f"   Confidence: {btc_signal['confidence']:.1%}")
        print(f"\n   Indicators:")
        print(f"     WaveTrend wt1: {btc_signal['wavetrend']['wt1']:.2f}")
        print(f"     MFI: {btc_signal['mfi']['value']:.2f}")
        print(f"     RSI: {btc_signal['rsi']['value']:.2f}")
        print(f"     StochRSI K: {btc_signal['stoch_rsi']['k']:.2f}")
        
        if btc_signal['ml_prediction']:
            print(f"\n   ML Prediction:")
            print(f"     Signal: {'BUY' if btc_signal['ml_prediction']['signal'] == 1 else 'HOLD'}")
            print(f"     Probability: {btc_signal['ml_prediction']['probability']:.1%}")
    
    # Scan multiple symbols
    print("\n\n🔍 Scanning top cryptocurrencies...")
    symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']
    results = generator.scan_all_symbols(symbols=symbols, timeframe='1h')
    
    if not results.empty:
        print(f"\n✅ Scan Results:")
        print("\n" + "=" * 70)
        
        for _, row in results.iterrows():
            emoji = "🟢" if row['final_score'] > 0 else "🔴" if row['final_score'] < 0 else "⚪"
            print(f"\n{emoji} {row['symbol']:<12}")
            print(f"   Price: ${row['price']:>10,.2f}")
            print(f"   Signal: {row['final_signal']:<15} Score: {row['final_score']:>5.1f}")
            print(f"   Confidence: {row['confidence']:>5.1%}")
            print(f"   WT1: {row['wt1']:>7.2f}  MFI: {row['mfi']:>6.2f}  RSI: {row['rsi']:>6.2f}", end="")
            if row['ml_prob'] is not None:
                print(f"  ML: {row['ml_prob']:>5.1%}")
            else:
                print()
        
        # Highlight strong signals
        print("\n" + "=" * 70)
        print("\n🎯 Trading Opportunities:")
        
        strong_signals = results[abs(results['final_score']) >= 2.0]
        
        if not strong_signals.empty:
            for _, opp in strong_signals.iterrows():
                emoji = "🟢🟢" if opp['final_score'] >= 3 else "🟢" if opp['final_score'] > 0 else "🔴"
                print(f"{emoji} {opp['symbol']:<12} {opp['final_signal']:<15} Score: {opp['final_score']:>5.1f}  Confidence: {opp['confidence']:>5.1%}")
        else:
            print("   No strong signals at the moment")
    
    print("\n" + "=" * 70)
    print("🎉 Signal Generator test completed successfully!")
    print("=" * 70)
