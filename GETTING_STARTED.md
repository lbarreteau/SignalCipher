# 📖 Guide de Démarrage - SignalCipher

## 🎯 Vue d'ensemble du Projet

**SignalCipher** est un système complet qui reproduit l'indicateur Market Cipher B et utilise l'intelligence artificielle pour apprendre automatiquement à identifier les meilleurs signaux de trading.

### Objectifs Principaux

1. ✅ **Reproduction fidèle de Market Cipher B**
   - Money Flow Index (MFI)
   - Wave Trend Oscillator
   - Momentum Waves (Multi-RSI)
   - Détection de Divergences
   - VWAP & Support/Resistance

2. 🤖 **Intelligence Artificielle**
   - Un modèle ML pour chaque sous-indicateur
   - Apprend à distinguer bons vs mauvais signaux
   - Meta-modèle pour agréger tous les signaux

3. 📊 **Scanner Multi-Crypto**
   - Top 10 cryptomonnaies en temps réel
   - Analyse sur plusieurs timeframes (1h, 4h, 1d, etc.)
   - Notifications automatiques des opportunités

---

## 📁 Documents Créés

### 1. **PROJECT_PLAN.md** 📋
Le plan complet du projet avec:
- Architecture détaillée du projet
- Description de chaque sous-indicateur
- Stratégie d'apprentissage par IA
- Roadmap de développement (14 semaines)
- Stack technologique
- KPIs et métriques de succès

### 2. **TECHNICAL_SPECS.md** 🔬
Spécifications techniques détaillées:
- Formules mathématiques de chaque indicateur
- Features ML pour chaque modèle
- Algorithmes de détection (divergences, niveaux, etc.)
- Architecture des modèles d'IA
- Pipeline de données
- Scanner en temps réel
- Framework de backtesting

### 3. **README.md** 📖
Documentation principale:
- Installation et usage
- Exemples de commandes
- Structure du projet
- Description des modèles ML
- Format des signaux générés

### 4. **Configuration Files** ⚙️

#### `.env.example`
Template des variables d'environnement:
- Clés API Binance
- Configuration database
- Tokens Telegram/Discord
- Paramètres ML et scanner

#### `config/config.yaml`
Configuration complète:
- Paramètres des indicateurs
- Hyperparamètres ML
- Settings du scanner
- Risk management
- Backtesting
- Logging

#### `config/symbols.yaml`
Liste des cryptos à scanner:
- Top 10 cryptos par défaut
- Altcoins optionnels
- Watchlists thématiques
- Filtres (volume, market cap)

#### `config/timeframes.yaml`
Configuration des timeframes:
- Définition de chaque timeframe
- Catégories (scalping, swing, etc.)
- Règles de confluence
- Presets de trading

### 5. **requirements.txt** 📦
Toutes les dépendances Python:
- Data collection (ccxt, python-binance)
- Technical analysis (ta-lib, pandas-ta)
- Machine Learning (scikit-learn, XGBoost, LightGBM)
- Visualization (matplotlib, plotly, streamlit)
- Backtesting, notifications, etc.

### 6. **TODO.md** ✅
Liste de tâches complète:
- Phase par phase
- Checklists détaillées
- Priorités
- Notes sur les bloquants potentiels

### 7. **CONTRIBUTING.md** 🤝
Guide de contribution:
- Code of conduct
- Standards de code
- Workflow Git
- Process de PR
- Templates pour issues/PRs

### 8. **setup_project.py** 🏗️
Script d'initialisation automatique:
- Crée toute la structure de dossiers
- Initialise les fichiers __init__.py
- Crée .env depuis template
- Affiche les prochaines étapes

---

## 🚀 Comment Démarrer

### Étape 1: Initialisation du Projet

```bash
# Exécuter le script de setup
python setup_project.py
```

Ce script va:
- ✅ Créer tous les dossiers nécessaires
- ✅ Créer les fichiers __init__.py
- ✅ Créer le fichier .env depuis template
- ✅ Créer/mettre à jour .gitignore

### Étape 2: Environnement Virtuel

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer (Linux/Mac)
source venv/bin/activate

# Activer (Windows)
venv\Scripts\activate
```

### Étape 3: Installation des Dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

**Note:** L'installation de ta-lib peut nécessiter des dépendances système:
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# Mac (avec Homebrew)
brew install ta-lib

# Si problème, utiliser uniquement pandas-ta (alternatif)
```

### Étape 4: Configuration

```bash
# Éditer le fichier .env
nano .env  # ou ton éditeur préféré
```

Configurer au minimum:
```bash
BINANCE_API_KEY=ta_cle_api_ici
BINANCE_API_SECRET=ton_secret_ici
```

Pour obtenir les clés API Binance:
1. Créer un compte sur Binance.com
2. Aller dans Profil > API Management
3. Créer une nouvelle API Key
4. ⚠️ **Activer uniquement "Enable Reading"** (pas de trading pour commencer)

### Étape 5: Première Collecte de Données

```bash
# Test de connexion API (à créer)
python -c "import ccxt; print(ccxt.binance().fetch_ticker('BTC/USDT'))"

# Collecter données BTC sur 30 jours (à implémenter)
# python -m data_collection.data_fetcher --symbols BTC/USDT --days 30
```

---

## 📚 Ordre de Développement Recommandé

### Phase 1: Fondations (Semaines 1-2) ✅ COMMENCER ICI

**Objectif:** Setup complet et collecte de données

#### 1.1 Créer le module de configuration
```bash
# À créer: utils/config.py
```
Fonctions à implémenter:
- `load_config()` - Charge config.yaml
- `load_env()` - Charge variables .env
- `get_symbols()` - Liste des cryptos depuis symbols.yaml
- `get_timeframes()` - Liste des timeframes depuis timeframes.yaml

#### 1.2 Créer le système de logging
```bash
# À créer: utils/logger.py
```
Fonctions à implémenter:
- Setup des handlers (console, file, errors)
- Format personnalisé
- Rotation des logs

#### 1.3 Implémenter le client Binance
```bash
# À créer: data_collection/binance_client.py
```
Classe `BinanceClient`:
- Authentification
- Rate limiting (1200 req/min)
- Retry logic avec backoff
- Gestion des erreurs

#### 1.4 Implémenter le data fetcher
```bash
# À créer: data_collection/data_fetcher.py
```
Fonctions:
- `fetch_ohlcv(symbol, timeframe, since, limit)`
- `fetch_multiple_timeframes(symbol, timeframes)`
- `fetch_multiple_symbols(symbols, timeframe)`
- Sauvegarde en Parquet

#### 1.5 Tester la collecte
```bash
# Collecter 1 an de données pour BTC, ETH, BNB
python -m data_collection.data_fetcher --symbols BTC/USDT,ETH/USDT,BNB/USDT --timeframes 1h,4h,1d --days 365
```

### Phase 2: Premier Indicateur (Semaines 2-3)

**Objectif:** Implémenter Money Flow Index

#### 2.1 Créer le module Money Flow
```bash
# À créer: indicators/money_flow.py
```

Fonction principale:
```python
def calculate_mfi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Money Flow Index.
    
    Args:
        df: DataFrame with OHLCV data
        period: MFI period (default 14)
        
    Returns:
        Series with MFI values
    """
    # 1. Calculate Typical Price
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # 2. Calculate Raw Money Flow
    money_flow = typical_price * df['volume']
    
    # 3. Positive and Negative Money Flow
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    
    # 4. Money Flow Ratio
    positive_mf = positive_flow.rolling(window=period).sum()
    negative_mf = negative_flow.rolling(window=period).sum()
    mf_ratio = positive_mf / negative_mf
    
    # 5. MFI
    mfi = 100 - (100 / (1 + mf_ratio))
    
    return mfi
```

#### 2.2 Visualiser MFI
```bash
# Créer: notebooks/01_mfi_visualization.ipynb
```

Cellules du notebook:
1. Import des données
2. Calcul du MFI
3. Plot prix + MFI
4. Identifier zones oversold/overbought
5. Marquer les signaux potentiels

### Phase 3: Premier Modèle ML (Semaines 3-4)

**Objectif:** Classifier les signaux MFI

#### 3.1 Labellisation des données
```bash
# À créer: training/data_labeling.py
```

#### 3.2 Feature engineering
```bash
# À créer: training/feature_engineering.py
```

#### 3.3 Entraîner le modèle
```bash
# À créer: ml_models/money_flow_classifier.py
```

#### 3.4 Évaluer les performances
```bash
# Créer: notebooks/02_mfi_ml_training.ipynb
```

### Phases Suivantes

Continuer selon le TODO.md:
- Phase 4: Autres indicateurs (Wave Trend, Momentum, etc.)
- Phase 5: Modèles ML pour chaque indicateur
- Phase 6: Scanner temps réel
- Phase 7: Backtesting
- Phase 8: Production

---

## 🎓 Concepts Clés à Comprendre

### 1. Market Cipher B

Market Cipher B combine plusieurs indicateurs pour donner une vue complète:
- **MFI:** Indique si l'argent entre ou sort (volume-weighted)
- **Wave Trend:** Oscillateur de momentum avec croisements
- **Momentum:** Force de la tendance (RSI composite)
- **Divergences:** Désaccords prix/indicateur = retournement potentiel
- **VWAP & Levels:** Prix moyen pondéré volume + supports/résistances

### 2. Machine Learning pour le Trading

**Problème classique:** Les indicateurs techniques donnent des faux signaux

**Solution ML:**
- Labelliser historiquement: signal → prix monte = BON, prix baisse = MAUVAIS
- Extraire features: valeurs indicateurs, contexte, volume, etc.
- Entraîner modèle: apprend quels patterns = vrais signaux
- Prédire: sur nouveaux signaux, modèle prédit probabilité de succès

### 3. Multi-Timeframe Analysis

Confluence = signal présent sur plusieurs timeframes
- 1h dit BUY, 4h dit BUY, 1d dit BUY → Signal fort!
- 1h dit BUY, 4h dit SELL → Signal contradictoire, éviter

### 4. Backtesting

Tester la stratégie sur données historiques:
- Simuler tous les trades
- Calculer profits/pertes
- Métriques: Win Rate, Sharpe Ratio, Max Drawdown
- Valider avant de trader réellement

---

## 🛠️ Outils et Technologies

### Python (3.10+)
Langage principal, moderne et puissant pour data science

### Pandas
Manipulation de données tabulaires (comme Excel mais en code)

### NumPy
Calculs numériques rapides

### TA-Lib / pandas-ta
Bibliothèques d'indicateurs techniques pré-faits

### Scikit-learn
ML classique (Random Forest, etc.)

### XGBoost / LightGBM
Gradient boosting, très performant pour données tabulaires

### CCXT
Bibliothèque unifiée pour accéder à toutes les exchanges crypto

### Streamlit
Créer dashboard web en Python pur

---

## ⚠️ Points d'Attention

### 1. API Rate Limits
Binance limite à 1200 requêtes/minute
- Implémenter rate limiting
- Cacher les données
- Batch requests

### 2. Qualité des Données
- Vérifier les gaps (données manquantes)
- Fill forward pour combler
- Valider OHLCV (open <= high, low <= close, etc.)

### 3. Overfitting ML
Modèle trop adapté aux données passées
- Split train/validation/test
- Cross-validation
- Walk-forward testing
- Régularisation

### 4. Slippage & Commissions
En backtest, inclure coûts réels:
- Commission Binance: ~0.1%
- Slippage: ~0.05-0.1%
- Impact majeur sur performance

### 5. Money Management
- Ne jamais risquer >2% du capital par trade
- Diversifier (plusieurs cryptos)
- Stop-loss obligatoires

---

## 📖 Ressources Utiles

### Documentation
- **Binance API:** https://binance-docs.github.io/apidocs/
- **CCXT:** https://docs.ccxt.com/
- **pandas-ta:** https://github.com/twopirllc/pandas-ta
- **Scikit-learn:** https://scikit-learn.org/

### Apprentissage
- **Indicateurs Techniques:** Investopedia.com
- **ML pour Trading:** "Advances in Financial Machine Learning" par Marcos López de Prado
- **Python Trading:** QuantStart.com

### Communauté
- **Reddit:** r/algotrading
- **Discord:** Servers de trading algo
- **GitHub:** Chercher projets similaires

---

## 🎯 Objectifs Court Terme

### Cette Semaine
1. ✅ Comprendre le plan complet (ce document)
2. ⬜ Exécuter `setup_project.py`
3. ⬜ Installer dépendances Python
4. ⬜ Configurer clés API Binance
5. ⬜ Implémenter `utils/config.py` et `utils/logger.py`

### Semaine Prochaine
1. ⬜ Implémenter `data_collection/binance_client.py`
2. ⬜ Implémenter `data_collection/data_fetcher.py`
3. ⬜ Collecter 1 an de données BTC/ETH/BNB
4. ⬜ Implémenter Money Flow Index
5. ⬜ Créer premier notebook de visualisation

### Ce Mois
1. ⬜ Tous les indicateurs implémentés
2. ⬜ Données de 2 ans pour Top 10 cryptos
3. ⬜ Premier modèle ML (Money Flow Classifier)
4. ⬜ Notebook complet d'analyse

---

## 💡 Conseils pour Réussir

### 1. Commencer Simple
Ne pas tout faire d'un coup:
- 1 indicateur à la fois
- 1 crypto pour tester (BTC)
- 1 timeframe (1h ou 1d)
Ensuite, généraliser

### 2. Tester Constamment
Après chaque fonction:
- Écrire un test unitaire
- Vérifier visuellement
- Comparer avec TradingView si possible

### 3. Documenter
- Commenter le code
- README dans chaque module
- Notebooks pour expliquer

### 4. Version Control
Commit régulièrement:
```bash
git add .
git commit -m "feat(indicators): implement MFI calculation"
git push
```

### 5. Itérer
V1 ne sera pas parfaite:
- Faire fonctionner d'abord
- Optimiser ensuite
- Refactor si nécessaire

---

## 🚨 Disclaimer Important

**Ce projet est éducatif et expérimental.**

### Risques du Trading
- ❌ Perte totale du capital possible
- ❌ Marchés crypto très volatils
- ❌ Aucune garantie de profit
- ❌ Pas de conseil financier

### Recommandations
- ✅ Backtester extensivement avant trading réel
- ✅ Commencer avec paper trading (simulation)
- ✅ N'investir que ce qu'on peut perdre
- ✅ Toujours faire ses propres recherches (DYOR)

### Responsabilité
Les auteurs ne sont pas responsables des pertes financières.
Le code est fourni "AS IS" sans garantie.

---

## 🎉 Conclusion

Tu as maintenant:
- ✅ Un plan complet sur 14 semaines
- ✅ Toute l'architecture définie
- ✅ Tous les fichiers de configuration
- ✅ Une roadmap claire
- ✅ Ce guide de démarrage

**Prochaine action:** Exécute `python setup_project.py` et commence par la Phase 1!

Bonne chance dans ce projet ambitieux! 🚀

---

**Créé le:** 30 Octobre 2025  
**Version:** 1.0  
**Auteur:** Assistant IA pour @lbarreteau
