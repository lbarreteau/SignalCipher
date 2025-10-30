# GitHub Copilot Instructions for SignalCipher

## Project Overview

SignalCipher is a Python-based cryptocurrency trading analysis bot that provides automated trading signals. The bot analyzes market data using 5 technical indicators inspired by Market Cipher B and generates scored alerts to help traders make informed decisions.

### Core Purpose
- Analyze cryptocurrency market data in real-time
- Calculate technical indicators (MFI, StochRSI, VWAP, MACD, RSI)
- Generate weighted scores based on indicator values
- Send trading alerts when score thresholds are met

## Architecture

### System Components

1. **Data Collection Layer**
   - Fetch real-time price and volume data from crypto exchanges
   - Support for multiple data sources (Binance, Coinbase, etc.)
   - Historical data retrieval for backtesting

2. **Indicator Calculation Engine**
   - Money Flow Index (MFI)
   - Stochastic RSI (StochRSI)
   - Volume Weighted Average Price (VWAP)
   - MACD (Moving Average Convergence Divergence)
   - Relative Strength Index (RSI)

3. **Scoring System**
   - Weighted point allocation per indicator
   - Threshold-based signal generation
   - Configurable scoring rules

4. **Alert System**
   - Notification delivery (Discord, Telegram, email)
   - Alert history and logging
   - Rate limiting and filtering

### Technology Stack
- **Language**: Python 3.8+
- **Data Analysis**: pandas, numpy
- **Technical Indicators**: ta-lib or pandas-ta
- **API Clients**: ccxt (Cryptocurrency Exchange Trading)
- **Configuration**: YAML or JSON
- **Logging**: Python logging module
- **Testing**: pytest

## Development Workflows

### Setting Up the Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Project Structure

```
SignalCipher/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── collectors.py      # Data fetching from exchanges
│   │   └── models.py          # Data models
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── mfi.py             # Money Flow Index
│   │   ├── stochrsi.py        # Stochastic RSI
│   │   ├── vwap.py            # VWAP
│   │   ├── macd.py            # MACD
│   │   └── rsi.py             # RSI
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── engine.py          # Scoring calculation
│   │   └── rules.py           # Scoring rules configuration
│   ├── alerts/
│   │   ├── __init__.py
│   │   ├── notifiers.py       # Alert delivery
│   │   └── formatters.py      # Alert message formatting
│   └── main.py                # Entry point
├── tests/
│   ├── __init__.py
│   ├── test_indicators/
│   ├── test_scoring/
│   └── test_alerts/
├── config/
│   ├── config.yaml            # Main configuration
│   └── scoring_rules.yaml     # Scoring rules
├── docs/
│   └── SCORING_LOGIC.md       # Detailed scoring documentation
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Coding Conventions

### Python Style Guide
- Follow PEP 8 style guide
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Naming Conventions
- **Classes**: PascalCase (e.g., `DataCollector`, `ScoreEngine`)
- **Functions/Methods**: snake_case (e.g., `calculate_mfi`, `send_alert`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_SCORE`, `DEFAULT_PERIOD`)
- **Private members**: prefix with underscore (e.g., `_internal_method`)

### Code Documentation

```python
def calculate_mfi(high: pd.Series, low: pd.Series, close: pd.Series, 
                  volume: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Money Flow Index (MFI).
    
    The MFI is a momentum indicator that uses price and volume to identify
    overbought or oversold conditions.
    
    Args:
        high: Series of high prices
        low: Series of low prices
        close: Series of closing prices
        volume: Series of volume data
        period: Lookback period for calculation (default: 14)
    
    Returns:
        Series containing MFI values (0-100)
    
    Raises:
        ValueError: If period is less than 1 or series lengths don't match
    """
    # Implementation here
    pass
```

### Error Handling
- Use specific exceptions rather than generic `Exception`
- Log errors with appropriate severity levels
- Provide meaningful error messages
- Handle API rate limits and network errors gracefully

```python
import logging

logger = logging.getLogger(__name__)

try:
    data = fetch_market_data(symbol)
except RateLimitError as e:
    logger.warning(f"Rate limit hit for {symbol}: {e}")
    time.sleep(retry_delay)
except NetworkError as e:
    logger.error(f"Network error fetching {symbol}: {e}")
    raise
```

## Indicator Implementation Guidelines

### Money Flow Index (MFI)
- Period: 14 (default)
- Range: 0-100
- Overbought: > 80
- Oversold: < 20

**Scoring Rules:**
- MFI < 20: +25 points (extreme oversold)
- MFI 20-30: +15 points (oversold)
- MFI > 80: -25 points (extreme overbought)
- MFI 70-80: -15 points (overbought)

### Stochastic RSI (StochRSI)
- Period: 14 (default)
- Smooth K: 3, Smooth D: 3
- Range: 0-100

**Scoring Rules:**
- K crosses above D below 20: +20 points (bullish signal)
- Both K and D < 20: +10 points (oversold)
- K crosses below D above 80: -20 points (bearish signal)
- Both K and D > 80: -10 points (overbought)

### VWAP (Volume Weighted Average Price)
- Calculate daily VWAP
- Compare current price to VWAP

**Scoring Rules:**
- Close > VWAP: +10 points (bullish momentum, price above average)
- Close < VWAP: -10 points (bearish momentum, price below average)

### MACD
- Fast: 12, Slow: 26, Signal: 9 (default)
- Monitor histogram crossovers

**Scoring Rules:**
- Histogram crosses from negative to positive: +15 points (bullish)
- Histogram crosses from positive to negative: -15 points (bearish)

### RSI (Relative Strength Index)
- Period: 14 (default)
- Range: 0-100

**Scoring Rules:**
- RSI < 30: +5 points (oversold)
- RSI > 70: -5 points (overbought)

## Scoring System

### Score Calculation
Total score is the sum of all indicator scores. Range: -85 to +85

**Maximum Positive Score**: +85
- MFI: +25 (extreme oversold)
- StochRSI: +20 (K crosses above D below 20) + +10 (both < 20) = +30
- VWAP: +10 (close > VWAP)
- MACD: +15 (histogram crosses positive)
- RSI: +5 (RSI < 30)

**Maximum Negative Score**: -85
- MFI: -25 (extreme overbought)
- StochRSI: -20 (K crosses below D above 80) + -10 (both > 80) = -30
- VWAP: -10 (close < VWAP)
- MACD: -15 (histogram crosses negative)
- RSI: -5 (RSI > 70)

### Signal Thresholds
- **STRONG BUY**: Score > 75
- **WEAK BUY**: Score > 50
- **NEUTRAL**: Score between -50 and 50
- **WEAK SELL**: Score < -50
- **STRONG SELL**: Score < -75

### Implementation Example

```python
class ScoreEngine:
    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules
    
    def calculate_score(self, indicators: Dict[str, float]) -> int:
        """Calculate total score from indicator values."""
        score = 0
        score += self._score_mfi(indicators['mfi'])
        score += self._score_stochrsi(indicators['stochrsi_k'], indicators['stochrsi_d'])
        score += self._score_vwap(indicators['price'], indicators['vwap'])
        score += self._score_macd(indicators['macd_histogram'], indicators['prev_macd_histogram'])
        score += self._score_rsi(indicators['rsi'])
        return score
    
    def get_signal(self, score: int) -> str:
        """Convert score to trading signal."""
        if score > 75:
            return "STRONG_BUY"
        elif score > 50:
            return "WEAK_BUY"
        elif score < -75:
            return "STRONG_SELL"
        elif score < -50:
            return "WEAK_SELL"
        else:
            return "NEUTRAL"
```

## Testing Practices

### Unit Tests
- Test each indicator calculation independently
- Verify scoring logic with known inputs
- Mock external API calls

```python
def test_calculate_mfi_oversold():
    """Test MFI calculation returns expected value in oversold condition."""
    # Arrange
    high = pd.Series([100, 105, 102])
    low = pd.Series([95, 98, 96])
    close = pd.Series([98, 103, 100])
    volume = pd.Series([1000, 1500, 1200])
    
    # Act
    mfi = calculate_mfi(high, low, close, volume, period=2)
    
    # Assert
    assert 0 <= mfi.iloc[-1] <= 100
```

### Integration Tests
- Test full pipeline from data fetch to alert generation
- Use historical data for reproducibility
- Verify alert formatting and delivery

### Backtesting
- Validate indicator calculations against known good implementations
- Test scoring system on historical data
- Measure signal accuracy and timing

## Configuration Management

### config.yaml Example

```yaml
exchange:
  name: "binance"
  api_key: "${EXCHANGE_API_KEY}"
  api_secret: "${EXCHANGE_API_SECRET}"

symbols:
  - "BTC/USDT"
  - "ETH/USDT"
  - "SOL/USDT"

indicators:
  mfi:
    period: 14
  stochrsi:
    period: 14
    smooth_k: 3
    smooth_d: 3
  rsi:
    period: 14
  macd:
    fast: 12
    slow: 26
    signal: 9

alerts:
  channels:
    - type: "discord"
      webhook_url: "${DISCORD_WEBHOOK}"
    - type: "telegram"
      bot_token: "${TELEGRAM_BOT_TOKEN}"
      chat_id: "${TELEGRAM_CHAT_ID}"
  
  rate_limit:
    max_per_hour: 10
    cooldown_minutes: 5

logging:
  level: "INFO"
  file: "logs/signalcipher.log"
```

## Integration Points

### External APIs
- **ccxt**: Unified cryptocurrency exchange API
  - Handle rate limits (typically 1200 requests/minute for Binance)
  - Implement retry logic with exponential backoff
  - Cache data when appropriate

### Notification Services
- **Discord**: Use webhooks for alerts
- **Telegram**: Bot API for message delivery
- **Email**: SMTP for email notifications

### Data Persistence
- Consider using SQLite or PostgreSQL for:
  - Alert history
  - Score history
  - Performance metrics
  - Configuration snapshots

## Security Best Practices

1. **API Keys**: Store in environment variables, never commit to git
2. **Secrets Management**: Use `.env` files (added to `.gitignore`)
3. **Input Validation**: Validate all external data
4. **Rate Limiting**: Respect exchange API limits
5. **Error Handling**: Don't expose sensitive information in error messages

## Performance Considerations

1. **Data Caching**: Cache market data for short periods (e.g., 1 minute)
2. **Batch Processing**: Process multiple symbols efficiently
3. **Async Operations**: Use asyncio for concurrent API calls
4. **Memory Management**: Clean up old data regularly

## Common Pitfalls to Avoid

1. **Look-Ahead Bias**: Don't use future data in indicator calculations
2. **Overfitting**: Keep scoring rules simple and interpretable
3. **False Signals**: Implement cooldown periods between alerts
4. **Data Quality**: Validate and clean incoming market data
5. **Time Zones**: Always use UTC for consistency

## Additional Resources

- **Technical Analysis Library**: [pandas-ta documentation](https://github.com/twopirllc/pandas-ta)
- **CCXT Documentation**: [ccxt.readthedocs.io](https://ccxt.readthedocs.io/)
- **Market Cipher**: Research original indicator methodology
- **Trading View**: Reference for indicator calculations

## When Adding New Features

1. Update this documentation with new conventions
2. Add tests before implementation (TDD)
3. Update configuration schema if needed
4. Document scoring rules in SCORING_LOGIC.md
5. Update README with usage examples
6. Consider backward compatibility

## AI Agent Guidelines

When working on this codebase:

1. **Understand Context**: Review SCORING_LOGIC.md before modifying scoring rules
2. **Maintain Consistency**: Follow existing patterns for new indicators
3. **Test Thoroughly**: All indicator changes must include unit tests
4. **Document Changes**: Update relevant documentation
5. **Validate Calculations**: Cross-reference indicator formulas with standard definitions
6. **Consider Impact**: Changes to scoring can affect all signals
7. **Security First**: Never commit credentials or secrets
8. **Performance**: Profile code changes that affect real-time processing

## Questions to Ask Before Implementing

- Does this change affect the scoring system?
- Are there existing tests that need updating?
- Is this indicator calculation standard or custom?
- What's the expected range of output values?
- How will this integrate with the alert system?
- Are there configuration options needed?
- What are the performance implications?

## Getting Help

- Review existing issues and PRs
- Check SCORING_LOGIC.md for scoring rules
- Consult pandas-ta or ta-lib documentation for standard indicators
- Test with small datasets before running on production data
