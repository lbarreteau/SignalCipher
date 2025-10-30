# SignalCipher - Plan de Projet

## 📋 Vue d'ensemble
Reproduction de l'indicateur **Market Cipher B** avec intelligence artificielle pour analyser automatiquement les signaux sur le Top 10 des cryptomonnaies en multi-timeframes.

---

## 🎯 Objectifs du Projet

### Objectif Principal
Créer un système d'analyse technique basé sur Market Cipher B capable d'apprendre et de détecter automatiquement les meilleures opportunités de trading via IA.

### Objectifs Spécifiques
1. ✅ Reproduire fidèlement tous les sous-indicateurs de Market Cipher B
2. 🤖 Entraîner un modèle IA pour chaque sous-indicateur
3. 📊 Scanner automatiquement le Top 10 des cryptos
4. ⏰ Analyser plusieurs timeframes simultanément
5. 📈 Générer des signaux de trading exploitables

---

## 🔧 Architecture du Projet

```
SignalCipher/
├── data/                          # Données de marché
│   ├── raw/                       # Données brutes des exchanges
│   ├── processed/                 # Données nettoyées et calculées
│   └── training/                  # Datasets d'entraînement IA
│
├── indicators/                    # Sous-indicateurs Market Cipher B
│   ├── __init__.py
│   ├── money_flow.py             # Money Flow Index (MFI)
│   ├── wave_trend.py             # Wave Trend Oscillator
│   ├── momentum_waves.py         # Momentum (RSI-based)
│   ├── divergences.py            # Détection de divergences
│   └── vwap.py                   # Volume Weighted Average Price
│
├── ml_models/                     # Modèles d'apprentissage
│   ├── __init__.py
│   ├── money_flow_classifier.py  # Classifier pour MFI
│   ├── wave_trend_predictor.py   # Prédicteur Wave Trend
│   ├── momentum_analyzer.py      # Analyseur de momentum
│   ├── pattern_recognizer.py     # Reconnaissance de patterns
│   └── signal_aggregator.py      # Agrégation des signaux
│
├── data_collection/               # Collecte de données
│   ├── __init__.py
│   ├── binance_client.py         # Client API Binance
│   ├── data_fetcher.py           # Récupération multi-timeframes
│   └── data_validator.py         # Validation des données
│
├── training/                      # Entraînement des modèles
│   ├── __init__.py
│   ├── data_labeling.py          # Labellisation des données
│   ├── feature_engineering.py    # Extraction de features
│   ├── model_trainer.py          # Entraînement
│   └── model_evaluator.py        # Évaluation des performances
│
├── scanner/                       # Scanner multi-crypto
│   ├── __init__.py
│   ├── crypto_scanner.py         # Scanner principal
│   ├── timeframe_analyzer.py     # Analyse multi-timeframes
│   └── signal_generator.py       # Génération de signaux
│
├── utils/                         # Utilitaires
│   ├── __init__.py
│   ├── config.py                 # Configuration
│   ├── logger.py                 # Système de logs
│   └── visualizer.py             # Visualisation des résultats
│
├── tests/                         # Tests unitaires
│   ├── test_indicators.py
│   ├── test_ml_models.py
│   └── test_scanner.py
│
├── notebooks/                     # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_indicator_development.ipynb
│   ├── 03_ml_training.ipynb
│   └── 04_backtesting.ipynb
│
├── models/                        # Modèles sauvegardés
│   └── .gitkeep
│
├── config/                        # Fichiers de configuration
│   ├── config.yaml
│   ├── symbols.yaml              # Liste des cryptos
│   └── timeframes.yaml           # Timeframes à analyser
│
├── requirements.txt               # Dépendances Python
├── setup.py                       # Installation du package
├── README.md                      # Documentation
├── .env.example                   # Variables d'environnement
└── main.py                        # Point d'entrée principal
```

---

## 📊 Sous-Indicateurs de Market Cipher B

### 1. **Money Flow Index (MFI)** 🟢
**Composants:**
- Volume-weighted RSI
- Périodes: 14, 28
- Seuils: Oversold (<20), Overbought (>80)

**IA à développer:**
- Classification: "Bon signal" / "Faux signal"
- Features: tendance MFI, divergences, volume, contexte de marché
- Objectif: Apprendre quand le MFI donne de vrais signaux de retournement

### 2. **Wave Trend Oscillator** 🌊
**Composants:**
- Channel Length: 9
- Average Length: 12
- Cross de la ligne zéro
- Overbought/Oversold zones

**IA à développer:**
- Détection de patterns de croisement
- Prédiction de la continuation ou retournement
- Classification de la force du signal

### 3. **Momentum Waves (RSI-based)** 📈
**Composants:**
- Multiple RSI (14, 21, 28 périodes)
- Détection de momentum haussier/baissier
- Changements de couleur (vert/rouge)

**IA à développer:**
- Analyse de la force du momentum
- Prédiction de continuité
- Détection de faiblesses précoces

### 4. **Divergences** 🔄
**Types:**
- Divergences régulières (Regular)
- Divergences cachées (Hidden)
- Sur RSI, MACD, Price Action

**IA à développer:**
- Reconnaissance automatique de patterns de divergence
- Validation de la qualité de la divergence
- Probabilité de réussite du signal

### 5. **VWAP & Support/Resistance** 📉
**Composants:**
- VWAP journalier
- VWAP hebdomadaire
- Zones de support/résistance

**IA à développer:**
- Détection automatique de niveaux clés
- Force des niveaux (probabilité de rebond)
- Confluence avec autres indicateurs

---

## 🤖 Stratégie d'Apprentissage par IA

### Phase 1: Labellisation des Données
**Méthode:**
1. Collecter données historiques (2-3 ans minimum)
2. Calculer tous les indicateurs
3. **Labellisation automatique:**
   - Signal "BON" si prix monte de X% dans les Y heures suivantes
   - Signal "MAUVAIS" si prix baisse ou stagne
   - Seuils adaptatifs selon volatilité

### Phase 2: Feature Engineering
**Features par sous-indicateur:**
- Valeurs brutes de l'indicateur
- Dérivées (vitesse de changement)
- Contexte multi-timeframes
- Volume relatif
- Volatilité récente
- Position par rapport aux moyennes mobiles
- Confluence avec autres indicateurs

### Phase 3: Modèles ML
**Approches:**
1. **Random Forest** - Pour classification binaire simple
2. **Gradient Boosting (XGBoost/LightGBM)** - Performance optimale
3. **LSTM/Transformers** - Pour séquences temporelles
4. **Ensemble Methods** - Agrégation des modèles

### Phase 4: Validation
**Métriques:**
- Accuracy, Precision, Recall, F1-Score
- Profit Factor en backtest
- Sharpe Ratio
- Maximum Drawdown
- Win Rate

---

## 📅 Roadmap de Développement

### **PHASE 1: Fondations (Semaine 1-2)** 🏗️
- [ ] Setup environnement (Python, bibliothèques)
- [ ] Configuration API Binance
- [ ] Collecte de données historiques Top 10 cryptos
- [ ] Structure de base du projet
- [ ] Système de logging et configuration

### **PHASE 2: Indicateurs (Semaine 3-4)** 📊
- [ ] Implémentation Money Flow Index
- [ ] Implémentation Wave Trend
- [ ] Implémentation Momentum Waves
- [ ] Détection de divergences
- [ ] Calcul VWAP et niveaux
- [ ] Tests unitaires des indicateurs

### **PHASE 3: Préparation ML (Semaine 5-6)** 🔬
- [ ] Labellisation automatique des données
- [ ] Feature engineering pour chaque indicateur
- [ ] Création datasets d'entraînement
- [ ] Visualisation et analyse exploratoire
- [ ] Split train/validation/test

### **PHASE 4: Entraînement IA (Semaine 7-9)** 🤖
- [ ] Modèle Money Flow Classifier
- [ ] Modèle Wave Trend Predictor
- [ ] Modèle Momentum Analyzer
- [ ] Modèle Pattern Recognizer
- [ ] Modèle Signal Aggregator (meta-modèle)
- [ ] Optimisation hyperparamètres
- [ ] Validation croisée

### **PHASE 5: Scanner Multi-Crypto (Semaine 10-11)** 🔍
- [ ] Scanner temps réel Top 10 cryptos
- [ ] Analyse multi-timeframes (1m, 5m, 15m, 1h, 4h, 1D)
- [ ] Génération de signaux agrégés
- [ ] Système de scoring des opportunités
- [ ] Notifications (Discord/Telegram)

### **PHASE 6: Backtesting & Optimisation (Semaine 12-13)** 📈
- [ ] Framework de backtesting
- [ ] Tests sur données historiques
- [ ] Analyse des performances
- [ ] Optimisation des seuils
- [ ] Walk-forward analysis
- [ ] Stress testing

### **PHASE 7: Production & Monitoring (Semaine 14+)** 🚀
- [ ] Deployment en production
- [ ] Dashboard de monitoring
- [ ] Système d'alertes
- [ ] Logs et métriques
- [ ] Retraining automatique périodique
- [ ] Documentation complète

---

## 🛠️ Stack Technologique

### Langages & Frameworks
- **Python 3.10+** - Langage principal
- **pandas** - Manipulation de données
- **numpy** - Calculs numériques
- **ta-lib** / **pandas-ta** - Indicateurs techniques

### Machine Learning
- **scikit-learn** - ML classique
- **XGBoost / LightGBM** - Gradient boosting
- **TensorFlow / PyTorch** - Deep Learning
- **Optuna** - Optimisation hyperparamètres

### Data Collection
- **ccxt** - API unifiée exchanges crypto
- **python-binance** - Client Binance spécialisé
- **requests** - API REST

### Visualisation
- **matplotlib / seaborn** - Graphiques statiques
- **plotly** - Graphiques interactifs
- **streamlit** - Dashboard web

### Base de Données
- **SQLite** / **PostgreSQL** - Stockage données
- **Redis** - Cache temps réel

### Outils
- **Jupyter** - Notebooks recherche
- **pytest** - Tests
- **black / flake8** - Formatting
- **Docker** - Containerisation

---

## 🎓 Critères de Succès pour l'IA

### Money Flow Classifier
✅ **Objectif:** Accuracy > 65% sur signaux de retournement  
✅ **Métrique clé:** Precision > 70% (éviter faux positifs)

### Wave Trend Predictor
✅ **Objectif:** F1-Score > 0.70  
✅ **Métrique clé:** Détection précoce des retournements

### Momentum Analyzer
✅ **Objectif:** ROC-AUC > 0.75  
✅ **Métrique clé:** Identification trends forts

### Pattern Recognizer
✅ **Objectif:** Recall > 80% sur divergences valides  
✅ **Métrique clé:** Validation qualité divergences

### Signal Aggregator (Meta-Modèle)
✅ **Objectif:** Win Rate > 55% en backtest  
✅ **Métrique clé:** Sharpe Ratio > 1.5, Profit Factor > 1.8

---

## 🔍 Top 10 Cryptos à Scanner

Configuration initiale (ajustable):
1. **BTC** (Bitcoin)
2. **ETH** (Ethereum)
3. **BNB** (Binance Coin)
4. **SOL** (Solana)
5. **XRP** (Ripple)
6. **ADA** (Cardano)
7. **AVAX** (Avalanche)
8. **DOT** (Polkadot)
9. **MATIC** (Polygon)
10. **LINK** (Chainlink)

### Timeframes à Analyser
- **Scalping:** 1m, 5m, 15m
- **Intraday:** 30m, 1h, 4h
- **Swing:** 1D, 3D
- **Position:** 1W

**Confluences:** Signal validé si présent sur au moins 3 timeframes alignés

---

## ⚠️ Risques et Mitigations

| Risque | Mitigation |
|--------|-----------|
| **Overfitting des modèles** | Validation croisée robuste, walk-forward testing |
| **Latence API** | Cache local, Rate limiting, webhooks |
| **Changement de régime de marché** | Retraining périodique, ensemble de modèles |
| **Faux signaux** | Meta-modèle d'agrégation, seuils de confiance |
| **Coûts API** | Optimisation des requêtes, stockage local |

---

## 📖 Documentation à Produire

1. **README.md** - Installation et usage
2. **API_DOCUMENTATION.md** - Documentation API interne
3. **MODEL_CARDS.md** - Description de chaque modèle IA
4. **TRADING_GUIDE.md** - Guide d'interprétation des signaux
5. **CHANGELOG.md** - Historique des versions

---

## 🚀 Commandes de Démarrage Rapide

```bash
# Installation
pip install -r requirements.txt

# Collecte de données
python -m data_collection.data_fetcher --symbols BTC,ETH --days 365

# Calcul des indicateurs
python -m indicators.calculate_all --data data/raw/

# Entraînement des modèles
python -m training.model_trainer --indicator money_flow

# Scanner en temps réel
python main.py --mode scanner --top 10 --timeframes 1h,4h,1D

# Dashboard
streamlit run dashboard/app.py
```

---

## 📊 KPIs du Projet

### Techniques
- Code coverage > 80%
- API response time < 200ms
- Scanner cycle < 5 minutes (10 cryptos × 8 timeframes)

### Business
- Win rate > 55%
- Profit factor > 1.8
- Sharpe ratio > 1.5
- Max drawdown < 20%

---

## 🎯 Prochaines Étapes Immédiates

1. ✅ **Valider ce plan de projet**
2. 📦 **Initialiser la structure du projet**
3. 📄 **Créer les fichiers de configuration**
4. 🔌 **Setup API Binance et collecte de données**
5. 📊 **Implémenter le premier indicateur (Money Flow)**

---

**Date de création:** 30 Octobre 2025  
**Durée estimée:** 14 semaines  
**Statut:** 🔴 Planning

