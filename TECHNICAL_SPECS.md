# Spécifications Techniques - SignalCipher

## 🔬 Détails Techniques des Sous-Indicateurs

### 1. Money Flow Index (MFI)

#### Formule Mathématique
```
Typical Price = (High + Low + Close) / 3
Raw Money Flow = Typical Price × Volume
Money Flow Ratio = (14-period Positive Money Flow) / (14-period Negative Money Flow)
MFI = 100 - (100 / (1 + Money Flow Ratio))
```

#### Paramètres
- **Période:** 14 (standard), 28 (long terme)
- **Oversold:** < 20
- **Overbought:** > 80
- **Zone neutre:** 40-60

#### Features ML pour Money Flow
```python
features = {
    'mfi_value': float,           # Valeur actuelle du MFI
    'mfi_slope': float,           # Dérivée (changement)
    'mfi_acceleration': float,    # Dérivée seconde
    'distance_to_oversold': float,# Distance à la zone 20
    'distance_to_overbought': float,
    'time_in_zone': int,          # Temps passé en oversold/overbought
    'volume_ratio': float,        # Volume actuel / Volume moyen
    'price_momentum': float,      # RSI du prix
    'divergence_detected': bool,  # Divergence prix/MFI
    'trend_alignment': float,     # Alignement avec MA50/200
    # Multi-timeframe
    'mfi_1h': float,
    'mfi_4h': float,
    'mfi_1d': float,
    'mfi_cross_count_24h': int,   # Nombre de croisements récents
}
```

#### Labels pour Classification
```python
def label_mfi_signal(data, lookforward=48):  # 48 heures forward
    """
    Label: 1 (BON) si dans les 48h suivantes:
    - Prix monte de > 3% (bull market) ou > 5% (bear market)
    - Et ne drop pas de > 2% avant
    
    Label: 0 (MAUVAIS) sinon
    """
    future_return = (data['close'].shift(-lookforward) - data['close']) / data['close']
    max_drawdown = data['close'].rolling(lookforward).min() / data['close'] - 1
    
    return (future_return > 0.03) & (max_drawdown > -0.02)
```

---

### 2. Wave Trend Oscillator

#### Formule Mathématique
```
HLC3 = (High + Low + Close) / 3
ESA = EMA(HLC3, n1)  # n1 = 10
D = EMA(|HLC3 - ESA|, n1)
CI = (HLC3 - ESA) / (0.015 × D)
WT1 = EMA(CI, n2)  # n2 = 21
WT2 = SMA(WT1, 4)
```

#### Paramètres Market Cipher
- **Channel Length (n1):** 9
- **Average Length (n2):** 12
- **Oversold:** < -60
- **Overbought:** > 60
- **Signal:** Croisement WT1 et WT2

#### Features ML pour Wave Trend
```python
features = {
    'wt1_value': float,
    'wt2_value': float,
    'wt_difference': float,       # WT1 - WT2
    'wt_cross_bullish': bool,     # WT1 croise WT2 vers le haut
    'wt_cross_bearish': bool,
    'wt1_slope': float,
    'wt1_acceleration': float,
    'distance_to_zero': float,
    'time_above_zero': int,
    'extreme_reading': bool,      # > 60 ou < -60
    'volatility': float,          # Std dev de WT1
    # Patterns
    'double_bottom': bool,
    'double_top': bool,
    'higher_lows': bool,          # Série de creux ascendants
    'lower_highs': bool,
}
```

---

### 3. Momentum Waves (RSI-based)

#### Composants
```python
# Multiple RSI avec lissage
rsi_14 = RSI(close, 14)
rsi_21 = RSI(close, 21)
rsi_28 = RSI(close, 28)

# Money Flow (volume-weighted)
mf = close * volume
mf_positive = mf where close > close.shift(1)
mf_negative = mf where close < close.shift(1)

# Momentum composite
momentum = weighted_average([rsi_14, rsi_21, rsi_28], [0.5, 0.3, 0.2])
momentum_color = 'green' if momentum > 50 else 'red'
```

#### Features ML
```python
features = {
    'momentum_value': float,
    'momentum_color_green': bool,
    'color_change': bool,         # Changement de couleur
    'rsi_14': float,
    'rsi_21': float,
    'rsi_28': float,
    'rsi_spread': float,          # Écart entre RSI multiples
    'rsi_alignment': float,       # Tous alignés dans même sens
    'strength': float,            # Distance à 50
    'persistence': int,           # Nb périodes même couleur
    'volume_confirmation': bool,  # Volume supporte momentum
}
```

---

### 4. Divergence Detection

#### Types de Divergences

**Regular Bullish Divergence (RBD):**
```
Price: Lower Low
Indicator: Higher Low
→ Signal de retournement haussier
```

**Regular Bearish Divergence (RBD):**
```
Price: Higher High
Indicator: Lower High
→ Signal de retournement baissier
```

**Hidden Bullish Divergence (HBD):**
```
Price: Higher Low
Indicator: Lower Low
→ Signal de continuation haussière
```

**Hidden Bearish Divergence (HBD):**
```
Price: Lower High
Indicator: Higher High
→ Signal de continuation baissière
```

#### Algorithme de Détection
```python
def detect_divergence(price, indicator, lookback=20):
    """
    1. Identifier les pivots (peaks/troughs) sur prix et indicateur
    2. Comparer les 2-3 derniers pivots
    3. Vérifier l'alignement temporel (±2 périodes)
    4. Calculer la force de la divergence
    """
    price_pivots = find_pivots(price, order=5)
    ind_pivots = find_pivots(indicator, order=5)
    
    divergences = []
    for i in range(len(price_pivots)-1):
        price_diff = price_pivots[i+1] - price_pivots[i]
        ind_diff = ind_pivots[i+1] - ind_pivots[i]
        
        # Regular Bullish
        if price_diff < 0 and ind_diff > 0:
            divergences.append({
                'type': 'regular_bullish',
                'strength': abs(price_diff) * ind_diff,
                'timestamp': price_pivots.index[i+1]
            })
    
    return divergences
```

#### Features ML pour Divergences
```python
features = {
    'divergence_type': str,       # RBD, RBD, HBD, HBD
    'strength': float,            # Magnitude de la divergence
    'timespan': int,              # Nombre de périodes entre pivots
    'price_slope': float,
    'indicator_slope': float,
    'volume_trend': float,        # Volume durant divergence
    'prior_trend_strength': float,# Force de la tendance avant
    'pivot_quality': float,       # Clarté des pivots (0-1)
    'confluence': int,            # Nb d'indicateurs divergents
    'context': str,               # 'bottom', 'top', 'middle'
}
```

---

### 5. VWAP & Support/Resistance

#### VWAP Calculation
```python
typical_price = (high + low + close) / 3
vwap = cumsum(typical_price * volume) / cumsum(volume)

# Multiple timeframe VWAP
vwap_session = VWAP(reset='1D')
vwap_weekly = VWAP(reset='1W')
vwap_monthly = VWAP(reset='1M')
```

#### Support/Resistance Detection
```python
def detect_levels(data, window=50, touches_required=3):
    """
    Méthode des clusters:
    1. Identifier tous les pivots high/low
    2. Clustering (DBSCAN) des niveaux proches
    3. Compter nombre de touches
    4. Score = touches × volume moyen aux touches
    """
    levels = []
    pivots = find_all_pivots(data)
    
    clusters = DBSCAN(eps=0.005).fit(pivots.reshape(-1, 1))
    
    for cluster_id in set(clusters.labels_):
        cluster_points = pivots[clusters.labels_ == cluster_id]
        touches = len(cluster_points)
        
        if touches >= touches_required:
            levels.append({
                'price': cluster_points.mean(),
                'touches': touches,
                'strength': touches * volume_at_touches.mean()
            })
    
    return sorted(levels, key=lambda x: x['strength'], reverse=True)
```

---

## 🤖 Architecture des Modèles ML

### Model 1: Money Flow Classifier

**Type:** Binary Classification (Gradient Boosting)

```python
from lightgbm import LGBMClassifier

model = LGBMClassifier(
    objective='binary',
    metric='auc',
    num_leaves=31,
    learning_rate=0.05,
    n_estimators=500,
    class_weight='balanced',  # Pour données déséquilibrées
    early_stopping_rounds=50
)

# Features importance tracking
feature_importance = model.feature_importances_
```

**Pipeline:**
```python
1. Feature Engineering (20-30 features)
2. Scaling (StandardScaler)
3. SMOTE (si imbalance > 1:3)
4. Train LightGBM
5. Threshold optimization (maximize F1)
6. Calibration (Platt scaling)
```

---

### Model 2: Wave Trend Predictor

**Type:** Multi-class Classification (3 classes: BUY / HOLD / SELL)

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    objective='multi:softmax',
    num_class=3,
    max_depth=6,
    learning_rate=0.05,
    n_estimators=300,
    subsample=0.8,
    colsample_bytree=0.8
)

# Labels
# 0 = SELL (baisse > 2%)
# 1 = HOLD (entre -2% et +2%)
# 2 = BUY (hausse > 2%)
```

---

### Model 3: LSTM for Sequence Prediction

**Type:** Sequence-to-One (Deep Learning)

```python
import tensorflow as tf
from tensorflow.keras import layers

model = tf.keras.Sequential([
    layers.LSTM(128, return_sequences=True, input_shape=(sequence_length, n_features)),
    layers.Dropout(0.2),
    layers.LSTM(64, return_sequences=False),
    layers.Dropout(0.2),
    layers.Dense(32, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 classes
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy', tf.keras.metrics.AUC()]
)
```

**Input:** Séquence de 60 périodes (features temporelles)  
**Output:** Probabilités [P(SELL), P(HOLD), P(BUY)]

---

### Model 4: Signal Aggregator (Meta-Model)

**Type:** Ensemble Voting + Stacking

```python
from sklearn.ensemble import StackingClassifier, VotingClassifier

# Level 1: Base models
base_models = [
    ('mfi', money_flow_classifier),
    ('wave', wave_trend_predictor),
    ('momentum', momentum_analyzer),
    ('divergence', pattern_recognizer),
]

# Level 2: Meta-learner
meta_model = LogisticRegression(class_weight='balanced')

stacked = StackingClassifier(
    estimators=base_models,
    final_estimator=meta_model,
    cv=5
)
```

**Logique de décision:**
```python
def generate_signal(predictions, confidence_threshold=0.7):
    """
    Signal final basé sur:
    1. Vote majoritaire des modèles
    2. Confidence minimale requise
    3. Confluence multi-timeframes
    """
    vote = predictions.mean(axis=0)
    confidence = predictions.std(axis=0)
    
    if vote['BUY'] > confidence_threshold and confidence < 0.2:
        return 'STRONG_BUY'
    elif vote['BUY'] > 0.5:
        return 'BUY'
    elif vote['SELL'] > confidence_threshold and confidence < 0.2:
        return 'STRONG_SELL'
    elif vote['SELL'] > 0.5:
        return 'SELL'
    else:
        return 'HOLD'
```

---

## 📊 Data Pipeline

### Data Collection
```python
class DataFetcher:
    def fetch_ohlcv(self, symbol, timeframe, since, limit=1000):
        """
        Binance API call avec retry logic
        """
        # Rate limiting: 1200 req/min
        # Batch size: 1000 candles max
        pass
    
    def fetch_multiple_timeframes(self, symbol, timeframes):
        """
        Parallélisation avec ThreadPoolExecutor
        """
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.fetch_ohlcv, symbol, tf, since)
                for tf in timeframes
            ]
        return [f.result() for f in futures]
```

### Data Processing
```python
class DataProcessor:
    def calculate_indicators(self, df):
        """
        Ajoute tous les indicateurs au DataFrame
        """
        df['mfi'] = self.calculate_mfi(df)
        df['wt1'], df['wt2'] = self.calculate_wave_trend(df)
        df['momentum'] = self.calculate_momentum(df)
        df['vwap'] = self.calculate_vwap(df)
        
        # Divergences (nécessite historique)
        df['divergence'] = self.detect_divergences(df)
        
        return df
    
    def add_ml_features(self, df):
        """
        Feature engineering pour ML
        """
        # Dérivées
        df['mfi_slope'] = df['mfi'].diff()
        df['mfi_accel'] = df['mfi_slope'].diff()
        
        # Moyennes mobiles
        df['ma_50'] = df['close'].rolling(50).mean()
        df['ma_200'] = df['close'].rolling(200).mean()
        
        # Volatilité
        df['volatility'] = df['close'].pct_change().rolling(20).std()
        
        return df
```

---

## 🔄 Real-Time Scanner Architecture

### Scanner Flow
```
┌─────────────────┐
│  Main Scheduler │  (Every 5 minutes)
└────────┬────────┘
         │
         ├──► Fetch Top 10 Cryptos
         │
         ├──► For each crypto:
         │    ├─► Fetch all timeframes (parallel)
         │    ├─► Calculate indicators
         │    ├─► Run ML models
         │    └─► Generate signals
         │
         ├──► Aggregate results
         │
         ├──► Filter by confidence
         │
         └──► Send notifications
```

### Pseudocode
```python
class CryptoScanner:
    def __init__(self):
        self.symbols = ['BTC/USDT', 'ETH/USDT', ...]  # Top 10
        self.timeframes = ['1h', '4h', '1d']
        self.models = load_all_models()
    
    async def scan_all(self):
        """Scan complet multi-crypto multi-timeframe"""
        results = []
        
        for symbol in self.symbols:
            symbol_result = await self.scan_symbol(symbol)
            results.append(symbol_result)
        
        # Tri par score de confiance
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Envoi des alertes pour top 3
        await self.send_alerts(results[:3])
        
        return results
    
    async def scan_symbol(self, symbol):
        """Analyse complète d'un symbole"""
        # Données multi-timeframe
        data = await self.fetch_data(symbol, self.timeframes)
        
        # Calcul indicateurs
        for tf in self.timeframes:
            data[tf] = self.calculate_indicators(data[tf])
        
        # Prédictions ML
        predictions = {}
        for model_name, model in self.models.items():
            features = self.extract_features(data)
            predictions[model_name] = model.predict_proba(features)
        
        # Agrégation
        signal = self.aggregate_signals(predictions, data)
        
        return {
            'symbol': symbol,
            'signal': signal['direction'],  # BUY/SELL/HOLD
            'confidence': signal['confidence'],
            'timeframe_alignment': signal['tf_alignment'],
            'key_levels': self.identify_levels(data),
            'timestamp': datetime.now()
        }
```

---

## 🧪 Backtesting Framework

### Backtest Engine
```python
class Backtester:
    def __init__(self, initial_capital=10000):
        self.capital = initial_capital
        self.position = None
        self.trades = []
        self.equity_curve = []
    
    def run(self, data, signals):
        """
        Walk-forward backtest
        """
        for i, (timestamp, row) in enumerate(data.iterrows()):
            current_signal = signals.loc[timestamp]
            
            # Gestion position
            if current_signal == 'BUY' and self.position is None:
                self.enter_long(row['close'], timestamp)
            
            elif current_signal == 'SELL' and self.position is not None:
                self.exit_long(row['close'], timestamp)
            
            # Track equity
            current_equity = self.calculate_equity(row['close'])
            self.equity_curve.append(current_equity)
        
        return self.calculate_metrics()
    
    def calculate_metrics(self):
        """Métriques de performance"""
        returns = pd.Series(self.equity_curve).pct_change()
        
        return {
            'total_return': (self.equity_curve[-1] / self.capital - 1) * 100,
            'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252),
            'max_drawdown': self.calculate_max_drawdown(),
            'win_rate': len([t for t in self.trades if t['pnl'] > 0]) / len(self.trades),
            'profit_factor': self.calculate_profit_factor(),
            'num_trades': len(self.trades),
        }
```

---

## 📈 Performance Optimization

### Caching Strategy
```python
import redis

class CacheManager:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.ttl = 300  # 5 minutes
    
    def cache_ohlcv(self, symbol, timeframe, data):
        key = f"ohlcv:{symbol}:{timeframe}"
        self.redis.setex(key, self.ttl, pickle.dumps(data))
    
    def get_cached_ohlcv(self, symbol, timeframe):
        key = f"ohlcv:{symbol}:{timeframe}"
        cached = self.redis.get(key)
        return pickle.loads(cached) if cached else None
```

### Parallel Processing
```python
from concurrent.futures import ProcessPoolExecutor

def parallel_indicator_calculation(data_chunks):
    """
    Calcul parallèle des indicateurs
    """
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        results = executor.map(calculate_all_indicators, data_chunks)
    
    return pd.concat(results)
```

---

## 🔐 Security & Configuration

### Environment Variables
```bash
# .env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_secret

DATABASE_URL=postgresql://user:pass@localhost/signalcipher
REDIS_URL=redis://localhost:6379

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Config Files
```yaml
# config/config.yaml
scanner:
  scan_interval: 300  # seconds
  symbols_count: 10
  timeframes:
    - 1h
    - 4h
    - 1d
  
ml_models:
  confidence_threshold: 0.70
  retrain_frequency: 7  # days
  
notifications:
  min_confidence: 0.75
  platforms:
    - telegram
    - discord

risk_management:
  max_position_size: 0.1  # 10% du capital
  stop_loss_pct: 0.02     # 2%
  take_profit_pct: 0.05   # 5%
```

---

## 📝 Logging & Monitoring

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup
logger = logging.getLogger('SignalCipher')
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    'logs/signalcipher.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Usage
logger.info(f"Scanning {symbol} on {timeframe}")
logger.warning(f"Low confidence signal: {confidence}")
logger.error(f"API error: {error}")
```

---

**Prochaines étapes:** Implémentation phase par phase selon le PROJECT_PLAN.md

