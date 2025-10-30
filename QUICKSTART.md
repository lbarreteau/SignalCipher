# ⚡ QuickStart - SignalCipher

> Pour ceux qui veulent commencer IMMÉDIATEMENT

## 🎯 Ce que ce projet fait

Reproduit **Market Cipher B** (indicateur TradingView à $1400) + ajoute de l'**IA** pour détecter automatiquement les meilleurs signaux de trading sur les **Top 10 cryptos**.

---

## 🚀 Démarrage Ultra-Rapide (15 minutes)

### 1. Clone & Setup (5 min)
```bash
cd /workspaces/SignalCipher

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Installation (peut prendre 5 min)
pip install --upgrade pip
pip install pandas numpy ccxt python-binance pyyaml python-dotenv
```

### 2. Configuration API Binance (5 min)

**A. Créer compte Binance:**
- Aller sur https://www.binance.com
- S'inscrire (gratuit)

**B. Générer API Key:**
- Menu > API Management
- Create API Key
- ⚠️ **IMPORTANT:** Cocher uniquement "Enable Reading" (pas de trading)
- Copier API Key et Secret

**C. Configurer .env:**
```bash
nano .env

# Coller:
BINANCE_API_KEY=ta_cle_api_ici
BINANCE_API_SECRET=ton_secret_ici
```

### 3. Premier Test (5 min)

**Créer test.py:**
```python
import ccxt
from dotenv import load_dotenv
import os

# Charger .env
load_dotenv()

# Test connexion Binance
exchange = ccxt.binance({
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_API_SECRET'),
})

# Récupérer prix BTC
ticker = exchange.fetch_ticker('BTC/USDT')
print(f"✅ Connexion OK!")
print(f"💰 Prix BTC: ${ticker['last']:,.2f}")

# Récupérer 100 dernières bougies 1h
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=100)
print(f"📊 Données récupérées: {len(ohlcv)} bougies")
```

**Exécuter:**
```bash
python test.py
```

**Résultat attendu:**
```
✅ Connexion OK!
💰 Prix BTC: $67,850.00
📊 Données récupérées: 100 bougies
```

---

## 📖 Fichiers à Lire (ordre de priorité)

### ⭐ OBLIGATOIRE (30 min)
1. **VISUAL_SUMMARY.md** - Diagrammes du projet (5 min)
2. **VUMANCHU_ANALYSIS.md** - Code TradingView traduit (15 min)
3. **TODO.md** Phase 1 - Premières tâches (10 min)

### 📚 Recommandé (1h)
4. **GETTING_STARTED.md** - Guide complet (30 min)
5. **TECHNICAL_SPECS.md** - Détails techniques (30 min)

### 📋 Référence
- **PROJECT_PLAN.md** - Roadmap complète
- **README.md** - Documentation générale
- **config/*.yaml** - Paramètres

---

## 💻 Première Feature à Coder

### Option A: Utilitaires (Recommandé)

**Créer utils/config.py:**
```python
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    """Charge config.yaml"""
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_symbols():
    """Charge symbols.yaml"""
    with open('config/symbols.yaml', 'r') as f:
        data = yaml.safe_load(f)
        return [s['symbol'] for s in data['top_10'] if s['enabled']]

def get_api_keys():
    """Retourne clés API Binance"""
    return {
        'api_key': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_API_SECRET')
    }

# Test
if __name__ == '__main__':
    config = load_config()
    print(f"✅ Config chargée: {len(config)} sections")
    
    symbols = load_symbols()
    print(f"📊 Symboles actifs: {symbols}")
    
    keys = get_api_keys()
    print(f"🔑 API Key: {keys['api_key'][:10]}...")
```

**Tester:**
```bash
python utils/config.py
```

### Option B: Premier Indicateur (WaveTrend)

**Créer indicators/wavetrend.py:**
```python
import pandas as pd
import numpy as np

def calculate_wavetrend(df, channel_len=9, average_len=12, ma_len=3):
    """
    Calcule WaveTrend Oscillator (Market Cipher B)
    
    Args:
        df: DataFrame avec colonnes ['high', 'low', 'close']
        channel_len: Longueur du canal (défaut: 9)
        average_len: Longueur moyenne (défaut: 12)
        ma_len: Longueur MA (défaut: 3)
    
    Returns:
        wt1, wt2, wt_vwap
    """
    # HLC3 source
    hlc3 = (df['high'] + df['low'] + df['close']) / 3
    
    # ESA = EMA of HLC3
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

# Test avec données réelles
if __name__ == '__main__':
    import ccxt
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    # Récupérer données BTC
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=200)
    
    # Convertir en DataFrame
    df = pd.DataFrame(
        ohlcv,
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # Calculer WaveTrend
    wt1, wt2, wt_vwap = calculate_wavetrend(df)
    
    # Afficher dernières valeurs
    print("📊 WaveTrend calculé!")
    print(f"\nDernières valeurs:")
    print(f"WT1: {wt1.iloc[-1]:.2f}")
    print(f"WT2: {wt2.iloc[-1]:.2f}")
    print(f"VWAP: {wt_vwap.iloc[-1]:.2f}")
    
    # Déterminer signal
    if wt2.iloc[-1] < -53:
        print("\n🟢 SIGNAL: OVERSOLD (zone d'achat potentielle)")
    elif wt2.iloc[-1] > 53:
        print("\n🔴 SIGNAL: OVERBOUGHT (zone de vente potentielle)")
    else:
        print("\n🟡 SIGNAL: NEUTRE")
```

**Tester:**
```bash
python indicators/wavetrend.py
```

---

## 📊 Visualiser les Résultats

**Créer notebook simple:**
```bash
pip install matplotlib jupyter
jupyter notebook
```

**Dans notebook:**
```python
import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from indicators.wavetrend import calculate_wavetrend

# Données
exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=200)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Calculer
wt1, wt2, wt_vwap = calculate_wavetrend(df)

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Prix
ax1.plot(df['timestamp'], df['close'], label='BTC Price', color='blue')
ax1.set_ylabel('Price ($)')
ax1.legend()
ax1.grid(alpha=0.3)

# WaveTrend
ax2.plot(df['timestamp'], wt1, label='WT1', color='cyan', linewidth=2)
ax2.plot(df['timestamp'], wt2, label='WT2', color='purple', linewidth=2)
ax2.axhline(y=53, color='r', linestyle='--', alpha=0.5, label='Overbought')
ax2.axhline(y=-53, color='g', linestyle='--', alpha=0.5, label='Oversold')
ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax2.fill_between(df['timestamp'], wt1, wt2, alpha=0.2)
ax2.set_ylabel('WaveTrend')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 🎯 Prochaines Étapes

### Jour 1-2: Setup ✅
- [x] Environnement Python
- [x] API Binance configurée
- [x] Premier test réussi

### Jour 3-5: Utilitaires
- [ ] `utils/config.py` - Chargement config
- [ ] `utils/logger.py` - Système de logs
- [ ] Tests unitaires

### Jour 6-10: Data Collection
- [ ] `data_collection/binance_client.py` - Client API
- [ ] `data_collection/data_fetcher.py` - Téléchargement données
- [ ] Collecter 1 an BTC/ETH/BNB

### Jour 11-20: Premier Indicateur
- [ ] `indicators/wavetrend.py` - WaveTrend complet
- [ ] Tests avec données réelles
- [ ] Visualisation notebook
- [ ] Validation vs TradingView

### Jour 21-30: Suite des Indicateurs
- [ ] `indicators/mfi_rsi.py` - Money Flow
- [ ] `indicators/divergences.py` - Détection divergences
- [ ] Tous les signaux Market Cipher B

---

## 🤔 Questions Fréquentes

### Q: Combien ça coûte ?
**R:** Gratuit ! Juste besoin d'un compte Binance (gratuit) pour les données.

### Q: Quel niveau Python requis ?
**R:** Intermédiaire. Connaître pandas, numpy. Le reste s'apprend.

### Q: Combien de temps pour finir ?
**R:** ~14 semaines à temps partiel (plan complet), ou 1 mois intensif pour version basique.

### Q: Peut-on trader automatiquement avec ?
**R:** Oui mais PAS recommandé au début. D'abord backtester, paper trading, puis éventuellement live.

### Q: Market Cipher B est payant ($1400), c'est légal de le reproduire ?
**R:** OUI. On ne copie pas le code, on reproduit les calculs (qui sont publics). C'est éducatif et open-source.

---

## 🆘 Problèmes Courants

### Erreur: "No module named 'ccxt'"
```bash
pip install ccxt
```

### Erreur: "API Key invalid"
- Vérifier que API Key est bien dans .env
- Vérifier pas d'espaces avant/après
- Régénérer API Key si nécessaire

### Erreur: "Rate limit exceeded"
- Binance limite 1200 req/min
- Ajouter `time.sleep(0.1)` entre requêtes
- Utiliser cache

### WaveTrend ne matche pas TradingView
- Vérifier données identiques (même timeframe)
- Vérifier période de warmup (50+ candles)
- Comparer valeurs intermédiaires (ESA, D, CI)

---

## 📚 Ressources Rapides

### Commandes Utiles
```bash
# Activer venv
source venv/bin/activate

# Installer une lib
pip install nom_lib

# Lancer Python
python

# Lancer script
python mon_script.py

# Jupyter notebook
jupyter notebook
```

### Liens
- **Binance API Docs:** https://binance-docs.github.io/apidocs/
- **CCXT Docs:** https://docs.ccxt.com/
- **Pandas Cheatsheet:** https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf

---

## ✅ Checklist Démarrage

- [ ] Python 3.10+ installé
- [ ] Projet cloné/téléchargé
- [ ] Venv créé et activé
- [ ] Dépendances de base installées (pandas, numpy, ccxt)
- [ ] Compte Binance créé
- [ ] API Key générée (Read Only)
- [ ] .env configuré avec clés
- [ ] Test connexion réussi
- [ ] Documentation lue (au moins VISUAL_SUMMARY.md)
- [ ] Premier code écrit (utils/config.py OU indicators/wavetrend.py)

---

## 🎉 C'est Parti !

Tu es prêt à créer un système de trading algorithmique de niveau pro !

**Next:** Lis **TODO.md** pour la liste complète des tâches.

---

**Temps total pour être opérationnel:** ~30 minutes  
**Temps pour premier indicateur fonctionnel:** ~2 heures  
**Temps pour système complet:** ~14 semaines

**Bon code ! 🚀**
