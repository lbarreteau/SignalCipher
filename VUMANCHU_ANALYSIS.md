# 🔬 Analyse du Code VuManChu Cipher B

## 📋 Vue d'ensemble

Ce document analyse le code Pine Script original de VuManChu Cipher B et fournit les spécifications exactes pour l'implémentation Python.

---

## 🎯 Composants Principaux Identifiés

### 1. **WaveTrend Oscillator** (Composant Principal)

#### Paramètres Par Défaut
```python
WT_CHANNEL_LENGTH = 9
WT_AVERAGE_LENGTH = 12
WT_MA_SOURCE = 'hlc3'  # (high + low + close) / 3
WT_MA_LENGTH = 3

# Niveaux Overbought/Oversold
OB_LEVEL_1 = 53
OB_LEVEL_2 = 60
OB_LEVEL_3 = 100
OS_LEVEL_1 = -53
OS_LEVEL_2 = -60
OS_LEVEL_3 = -75
```

#### Formule (traduite de Pine Script)
```python
def calculate_wavetrend(df, channel_len=9, average_len=12, ma_len=3):
    """
    Calcule WaveTrend Oscillator
    
    Pine Script original:
    esa = ema(tfsrc, chlen)
    de = ema(abs(tfsrc - esa), chlen)
    ci = (tfsrc - esa) / (0.015 * de)
    wt1 = ema(ci, avg)
    wt2 = sma(wt1, malen)
    """
    # Source = HLC3
    hlc3 = (df['high'] + df['low'] + df['close']) / 3
    
    # ESA = EMA of source
    esa = hlc3.ewm(span=channel_len, adjust=False).mean()
    
    # D = EMA of absolute difference
    d = abs(hlc3 - esa).ewm(span=channel_len, adjust=False).mean()
    
    # CI = Channel Index
    ci = (hlc3 - esa) / (0.015 * d)
    
    # WT1 = EMA of CI
    wt1 = ci.ewm(span=average_len, adjust=False).mean()
    
    # WT2 = SMA of WT1
    wt2 = wt1.rolling(window=ma_len).mean()
    
    # VWAP derivative
    wt_vwap = wt1 - wt2
    
    return wt1, wt2, wt_vwap
```

#### Signaux WaveTrend
```python
def detect_wt_signals(wt1, wt2):
    """
    Détecte les signaux de croisement WaveTrend
    """
    # Croisement
    wt_cross = (wt1.shift(1) <= wt2.shift(1)) & (wt1 > wt2)  # Cross up
    wt_cross |= (wt1.shift(1) >= wt2.shift(1)) & (wt1 < wt2)  # Cross down
    
    wt_cross_up = (wt1.shift(1) <= wt2.shift(1)) & (wt1 > wt2)
    wt_cross_down = (wt1.shift(1) >= wt2.shift(1)) & (wt1 < wt2)
    
    # Zones
    wt_oversold = wt2 <= -53
    wt_overbought = wt2 >= 53
    
    return {
        'cross': wt_cross,
        'cross_up': wt_cross_up,
        'cross_down': wt_cross_down,
        'oversold': wt_oversold,
        'overbought': wt_overbought
    }
```

---

### 2. **Money Flow Index (MFI) - RSI+MFI Combiné**

#### Paramètres Par Défaut
```python
MFI_PERIOD = 60
MFI_MULTIPLIER = 150
MFI_POS_Y = 2.5  # Position verticale pour affichage
```

#### Formule (traduite)
```python
def calculate_mfi_rsi_area(df, period=60, multiplier=150):
    """
    Calcule la zone MFI+RSI combinée
    
    Pine Script:
    f_rsimfi(_period, _multiplier, _tf) => 
        sma(((close - open) / (high - low)) * _multiplier, _period) - rsiMFIPosY
    """
    # Money Flow calculation
    money_flow = ((df['close'] - df['open']) / (df['high'] - df['low'])) * multiplier
    
    # SMA of money flow
    mfi_rsi = money_flow.rolling(window=period).mean() - MFI_POS_Y
    
    return mfi_rsi
```

**Note:** Cette formule est une version simplifiée qui combine RSI et MFI en un seul indicateur.

---

### 3. **RSI (Relative Strength Index)**

#### Paramètres Par Défaut
```python
RSI_LENGTH = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 60
```

#### Implémentation Standard
```python
def calculate_rsi(df, period=14):
    """
    RSI standard
    """
    delta = df['close'].diff()
    
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi
```

---

### 4. **Stochastic RSI**

#### Paramètres Par Défaut
```python
STOCH_LENGTH = 14
STOCH_RSI_LENGTH = 14
STOCH_K_SMOOTH = 3
STOCH_D_SMOOTH = 3
STOCH_USE_LOG = True
```

#### Formule
```python
def calculate_stochastic_rsi(df, stoch_len=14, rsi_len=14, k_smooth=3, d_smooth=3, use_log=True):
    """
    Stochastic RSI
    
    Pine Script:
    src = _log ? log(_src) : _src
    rsi = rsi(src, _rsilen)
    kk = sma(stoch(rsi, rsi, rsi, _stochlen), _smoothk)
    d1 = sma(kk, _smoothd)
    """
    # Source
    src = np.log(df['close']) if use_log else df['close']
    
    # Calculate RSI
    rsi = calculate_rsi(pd.DataFrame({'close': src}), period=rsi_len)
    
    # Stochastic of RSI
    lowest_rsi = rsi.rolling(window=stoch_len).min()
    highest_rsi = rsi.rolling(window=stoch_len).max()
    
    stoch = 100 * (rsi - lowest_rsi) / (highest_rsi - lowest_rsi)
    
    # Smooth
    k = stoch.rolling(window=k_smooth).mean()
    d = k.rolling(window=d_smooth).mean()
    
    return k, d
```

---

### 5. **Divergence Detection (Fonction Clé)**

#### Fonction de Détection des Fractals
```python
def find_fractals(series):
    """
    Détecte les pivots (fractals) dans une série
    
    Pine Script:
    f_top_fractal(src) => src[4] < src[2] and src[3] < src[2] and src[2] > src[1] and src[2] > src[0]
    f_bot_fractal(src) => src[4] > src[2] and src[3] > src[2] and src[2] < src[1] and src[2] < src[0]
    """
    top_fractals = []
    bot_fractals = []
    
    for i in range(4, len(series)):
        # Top fractal (peak)
        if (series[i-4] < series[i-2] and 
            series[i-3] < series[i-2] and 
            series[i-2] > series[i-1] and 
            series[i-2] > series[i]):
            top_fractals.append(i-2)
        
        # Bottom fractal (trough)
        if (series[i-4] > series[i-2] and 
            series[i-3] > series[i-2] and 
            series[i-2] < series[i-1] and 
            series[i-2] < series[i]):
            bot_fractals.append(i-2)
    
    return top_fractals, bot_fractals
```

#### Détection des Divergences
```python
def find_divergences(indicator, price_high, price_low, ob_level, os_level, use_limits=True):
    """
    Trouve les divergences régulières et cachées
    
    Pine Script logic:
    bearSignal = fractalTop and high[2] > highPrice and src[2] < highPrev
    bullSignal = fractalBot and low[2] < lowPrice and src[2] > lowPrev
    bearDivHidden = fractalTop and high[2] < highPrice and src[2] > highPrev
    bullDivHidden = fractalBot and low[2] > lowPrice and src[2] < lowPrev
    """
    top_fractals, bot_fractals = find_fractals(indicator)
    
    divergences = {
        'regular_bearish': [],
        'regular_bullish': [],
        'hidden_bearish': [],
        'hidden_bullish': []
    }
    
    # Regular Bearish Divergence
    for i in range(1, len(top_fractals)):
        curr_idx = top_fractals[i]
        prev_idx = top_fractals[i-1]
        
        if use_limits and indicator[curr_idx] < ob_level:
            continue
        
        # Price makes higher high, indicator makes lower high
        if (price_high[curr_idx] > price_high[prev_idx] and 
            indicator[curr_idx] < indicator[prev_idx]):
            divergences['regular_bearish'].append(curr_idx)
    
    # Regular Bullish Divergence
    for i in range(1, len(bot_fractals)):
        curr_idx = bot_fractals[i]
        prev_idx = bot_fractals[i-1]
        
        if use_limits and indicator[curr_idx] > os_level:
            continue
        
        # Price makes lower low, indicator makes higher low
        if (price_low[curr_idx] < price_low[prev_idx] and 
            indicator[curr_idx] > indicator[prev_idx]):
            divergences['regular_bullish'].append(curr_idx)
    
    # Hidden Bearish Divergence
    for i in range(1, len(top_fractals)):
        curr_idx = top_fractals[i]
        prev_idx = top_fractals[i-1]
        
        # Price makes lower high, indicator makes higher high
        if (price_high[curr_idx] < price_high[prev_idx] and 
            indicator[curr_idx] > indicator[prev_idx]):
            divergences['hidden_bearish'].append(curr_idx)
    
    # Hidden Bullish Divergence
    for i in range(1, len(bot_fractals)):
        curr_idx = bot_fractals[i]
        prev_idx = bot_fractals[i-1]
        
        # Price makes higher low, indicator makes lower low
        if (price_low[curr_idx] > price_low[prev_idx] and 
            indicator[curr_idx] < indicator[prev_idx]):
            divergences['hidden_bullish'].append(curr_idx)
    
    return divergences
```

---

### 6. **Signaux Principaux**

#### Buy Signal (Green Circle)
```python
def detect_buy_signal(wt1, wt2):
    """
    Pine Script:
    buySignal = wtCross and wtCrossUp and wtOversold
    """
    wt_cross_up = (wt1.shift(1) <= wt2.shift(1)) & (wt1 > wt2)
    wt_oversold = wt2 <= -53
    
    buy_signal = wt_cross_up & wt_oversold
    
    return buy_signal
```

#### Sell Signal (Red Circle)
```python
def detect_sell_signal(wt1, wt2):
    """
    Pine Script:
    sellSignal = wtCross and wtCrossDown and wtOverbought
    """
    wt_cross_down = (wt1.shift(1) >= wt2.shift(1)) & (wt1 < wt2)
    wt_overbought = wt2 >= 53
    
    sell_signal = wt_cross_down & wt_overbought
    
    return sell_signal
```

#### Gold Buy Signal (Golden Circle)
```python
def detect_gold_buy(wt2, rsi, wt_bull_div, os_level_3=-75):
    """
    Pine Script:
    wtGoldBuy = ((wtShowDiv and wtBullDiv) or (rsiShowDiv and rsiBullDiv)) and
               wtLow_prev <= osLevel3 and
               wt2 > osLevel3 and
               wtLow_prev - wt2 <= -5 and
               lastRsi < 30
    """
    # Conditions:
    # 1. Bullish divergence détectée
    # 2. Previous WT low <= -75
    # 3. Current WT2 > -75
    # 4. Momentum fort (différence > 5)
    # 5. RSI < 30
    
    gold_buy = (
        wt_bull_div &
        (wt2 > os_level_3) &
        (rsi < 30)
    )
    
    return gold_buy
```

---

## 🎨 Niveaux et Zones Clés

### Niveaux WaveTrend
```python
WT_LEVELS = {
    'overbought': {
        'level_1': 53,   # Premier niveau de résistance
        'level_2': 60,   # Forte résistance
        'level_3': 100,  # Résistance extrême
    },
    'oversold': {
        'level_1': -53,  # Premier niveau de support
        'level_2': -60,  # Fort support
        'level_3': -75,  # Support extrême (Gold buy zone)
    }
}
```

### Niveaux MFI/RSI
```python
MFI_LEVELS = {
    'positive': 0,    # Au-dessus = Money flow entrant
    'negative': 0,    # En-dessous = Money flow sortant
}

RSI_LEVELS = {
    'oversold': 30,
    'neutral': 50,
    'overbought': 60,
}
```

---

## 🔄 Sommi Patterns (Avancé)

### Sommi Flag (Drapeau)
```python
def detect_sommi_flag(wt1, wt2, rsi_mfi, wt_vwap_htf):
    """
    Bearish Flag:
    - MFI+RSI < 0 (money flow sortant)
    - WT2 > 0 et croise vers le bas
    - VWAP higher timeframe < 0
    
    Bullish Flag: Inverse
    """
    wt_cross_down = (wt1.shift(1) >= wt2.shift(1)) & (wt1 < wt2)
    wt_cross_up = (wt1.shift(1) <= wt2.shift(1)) & (wt1 > wt2)
    
    bearish_flag = (
        (rsi_mfi < 0) &
        (wt2 > 0) &
        wt_cross_down &
        (wt_vwap_htf < 0)
    )
    
    bullish_flag = (
        (rsi_mfi > 0) &
        (wt2 < 0) &
        wt_cross_up &
        (wt_vwap_htf > 0)
    )
    
    return bearish_flag, bullish_flag
```

### Sommi Diamond (Diamant)
```python
def detect_sommi_diamond(wt1, wt2, htf_candle_direction):
    """
    Bearish Diamond:
    - WT2 >= 0
    - WT croise vers le bas
    - Heiken Ashi HTF candle est rouge
    
    Bullish Diamond:
    - WT2 <= 0
    - WT croise vers le haut
    - Heiken Ashi HTF candle est verte
    """
    wt_cross_down = (wt1.shift(1) >= wt2.shift(1)) & (wt1 < wt2)
    wt_cross_up = (wt1.shift(1) <= wt2.shift(1)) & (wt1 > wt2)
    
    bearish_diamond = (
        (wt2 >= 0) &
        wt_cross_down &
        (htf_candle_direction == 'bearish')
    )
    
    bullish_diamond = (
        (wt2 <= 0) &
        wt_cross_up &
        (htf_candle_direction == 'bullish')
    )
    
    return bearish_diamond, bullish_diamond
```

---

## 📊 Ordre d'Implémentation Recommandé

### Phase 1: Core Indicators (Semaine 1-2)
1. ✅ **WaveTrend Oscillator** - Le plus important
2. ✅ **Money Flow (MFI+RSI area)** - Deuxième priorité
3. ✅ **RSI** - Standard mais essentiel
4. ✅ **Stochastic RSI** - Pour confluence

### Phase 2: Divergence Detection (Semaine 3)
5. ✅ **Fractal Detection** - Base des divergences
6. ✅ **Divergence Logic** - Regular + Hidden pour WT, RSI, Stoch

### Phase 3: Signals (Semaine 4)
7. ✅ **Buy/Sell Signals** - Basé sur WT
8. ✅ **Gold Buy Signal** - Signal spécial
9. ✅ **Divergence Signals** - Confluence avec divergences

### Phase 4: Advanced Patterns (Semaine 5 - Optionnel)
10. ⭐ **Sommi Flag** - Pattern avancé
11. ⭐ **Sommi Diamond** - Pattern avancé avec HTF

---

## 🎯 Différences Clés Pine Script vs Python

### 1. **Indexing**
```python
# Pine Script: src[2] = 2 barres en arrière
# Python: series.shift(2) ou series.iloc[-3]

# Pine: src[2] < src[1]
# Python: series.shift(2) < series.shift(1)
```

### 2. **EMA vs SMA**
```python
# Pine: ema(src, length)
# Python: src.ewm(span=length, adjust=False).mean()

# Pine: sma(src, length)
# Python: src.rolling(window=length).mean()
```

### 3. **Cross Detection**
```python
# Pine: cross(a, b) = true when crossing
# Python: Need to check shift(1) vs current

def cross_up(a, b):
    return (a.shift(1) <= b.shift(1)) & (a > b)

def cross_down(a, b):
    return (a.shift(1) >= b.shift(1)) & (a < b)
```

### 4. **ValueWhen**
```python
# Pine: valuewhen(condition, source, occurrence)
# Python: Need custom function

def valuewhen(condition, source, occurrence=0):
    """
    Returns value of source when condition was true
    occurrence times ago
    """
    valid_values = source[condition]
    if len(valid_values) > occurrence:
        return valid_values.iloc[-(occurrence + 1)]
    return np.nan
```

---

## 📝 Structure Recommandée Python

```python
# indicators/vumanchu_cipher_b.py

class VuManchuCipherB:
    """
    Implémentation complète de VuManChu Cipher B
    """
    
    def __init__(self, 
                 wt_channel_len=9,
                 wt_average_len=12,
                 wt_ma_len=3,
                 mfi_period=60,
                 rsi_len=14,
                 stoch_len=14):
        self.wt_channel_len = wt_channel_len
        self.wt_average_len = wt_average_len
        self.wt_ma_len = wt_ma_len
        self.mfi_period = mfi_period
        self.rsi_len = rsi_len
        self.stoch_len = stoch_len
    
    def calculate_all(self, df):
        """
        Calcule tous les indicateurs sur un DataFrame OHLCV
        """
        result = df.copy()
        
        # 1. WaveTrend
        result['wt1'], result['wt2'], result['wt_vwap'] = self.calculate_wavetrend(df)
        
        # 2. MFI+RSI
        result['mfi_rsi'] = self.calculate_mfi_rsi(df)
        
        # 3. RSI
        result['rsi'] = self.calculate_rsi(df)
        
        # 4. Stochastic RSI
        result['stoch_k'], result['stoch_d'] = self.calculate_stoch_rsi(df)
        
        # 5. Divergences
        divergences = self.find_all_divergences(result)
        result = pd.concat([result, divergences], axis=1)
        
        # 6. Signals
        signals = self.generate_signals(result)
        result = pd.concat([result, signals], axis=1)
        
        return result
    
    def calculate_wavetrend(self, df):
        """WaveTrend calculation"""
        # Implementation...
        pass
    
    def calculate_mfi_rsi(self, df):
        """MFI+RSI area calculation"""
        # Implementation...
        pass
    
    # ... autres méthodes
```

---

## ⚠️ Points d'Attention

### 1. **Lookback Period**
Le code utilise `src[4]` pour les fractals, donc besoin de minimum 5 périodes de données.

### 2. **Multi-Timeframe**
VuManChu utilise `security()` pour accéder à des timeframes supérieurs. En Python, il faut:
- Télécharger données HTF séparément
- Resampler les données
- Aligner les timestamps

### 3. **Performance**
- Éviter les boucles Python natives
- Utiliser vectorisation pandas/numpy
- Cacher les calculs intermédiaires

### 4. **NaN Handling**
Les premiers éléments seront NaN (warmup period):
- EMA avec span=12 → 12 premiers NaN
- SMA avec window=3 → 3 premiers NaN
- Fractals → 5 premiers NaN

---

## 📦 Dépendances Python Nécessaires

```python
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator
# ou implémenter custom si besoin de précision exacte
```

---

## 🎯 Prochaines Étapes

### Immédiat
1. ✅ Créer `indicators/wavetrend.py` avec implémentation exacte
2. ✅ Créer `indicators/mfi_rsi.py` avec formule combinée
3. ✅ Tester sur données BTC pour validation visuelle vs TradingView

### Court Terme
4. ✅ Implémenter détection fractals
5. ✅ Implémenter détection divergences
6. ✅ Générer tous les signaux

### Validation
7. ✅ Comparer visuellement avec TradingView
8. ✅ Vérifier que signaux matchent
9. ✅ Ajuster paramètres si écarts

---

**Ce document sera la référence pour une implémentation fidèle à 100% du VuManChu Cipher B original.**

**Créé le:** 30 Octobre 2025  
**Source:** VuManChu Cipher B v4 (TradingView)  
**Status:** 📋 Référence pour implémentation
