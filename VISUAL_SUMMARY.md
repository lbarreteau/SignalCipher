# 📊 SignalCipher - Résumé Visuel du Projet

```
┌─────────────────────────────────────────────────────────────────────┐
│                     🔐 SIGNALCIPHER PROJECT                         │
│          Reproduction de Market Cipher B avec Machine Learning      │
└─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════
                         📊 ARCHITECTURE GLOBALE
═══════════════════════════════════════════════════════════════════════

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   BINANCE    │─────▶│     DATA     │─────▶│  INDICATORS  │
│     API      │      │  COLLECTION  │      │  CALCULATION │
└──────────────┘      └──────────────┘      └──────────────┘
                                                     │
                                                     ▼
                              ┌─────────────────────────────────┐
                              │    FEATURE ENGINEERING          │
                              └─────────────────────────────────┘
                                                     │
                                                     ▼
                              ┌─────────────────────────────────┐
                              │    ML MODELS (5 modèles)        │
                              │  • Money Flow Classifier        │
                              │  • Wave Trend Predictor         │
                              │  • Momentum Analyzer            │
                              │  • Pattern Recognizer           │
                              │  • Signal Aggregator (Meta)     │
                              └─────────────────────────────────┘
                                                     │
                              ┌─────────────────────┴─────────────────┐
                              ▼                                       ▼
                   ┌──────────────────┐                   ┌──────────────────┐
                   │   LIVE SCANNER   │                   │   BACKTESTING    │
                   │  Top 10 Cryptos  │                   │   Historical     │
                   │  Multi-Timeframe │                   │   Validation     │
                   └──────────────────┘                   └──────────────────┘
                              │
                              ▼
                   ┌──────────────────┐
                   │  NOTIFICATIONS   │
                   │ Telegram/Discord │
                   └──────────────────┘

═══════════════════════════════════════════════════════════════════════
                      📈 SOUS-INDICATEURS MARKET CIPHER B
═══════════════════════════════════════════════════════════════════════

1. 💰 MONEY FLOW INDEX (MFI)
   ╔════════════════════════════════════════════════════════════════╗
   ║ • Volume-weighted RSI                                          ║
   ║ • Zones: Oversold (<20), Overbought (>80)                     ║
   ║ • IA: Classifier bon vs mauvais signal                        ║
   ║ • Features: MFI value, slope, divergences, volume, trend      ║
   ╚════════════════════════════════════════════════════════════════╝

2. 🌊 WAVE TREND OSCILLATOR
   ╔════════════════════════════════════════════════════════════════╗
   ║ • Oscillateur de momentum                                      ║
   ║ • Signal: Croisement WT1/WT2                                  ║
   ║ • IA: Predictor multi-class (BUY/HOLD/SELL)                   ║
   ║ • Features: WT values, cross patterns, zones extrêmes         ║
   ╚════════════════════════════════════════════════════════════════╝

3. 📊 MOMENTUM WAVES
   ╔════════════════════════════════════════════════════════════════╗
   ║ • Multi-RSI composite (14, 21, 28)                            ║
   ║ • Changement de couleur (vert/rouge)                          ║
   ║ • IA: Analyzer force momentum                                 ║
   ║ • Features: RSI multiple, alignment, persistence              ║
   ╚════════════════════════════════════════════════════════════════╝

4. 🔄 DIVERGENCES
   ╔════════════════════════════════════════════════════════════════╗
   ║ • Regular Bullish/Bearish                                      ║
   ║ • Hidden Bullish/Bearish                                       ║
   ║ • IA: Pattern recognizer + validation                         ║
   ║ • Features: Type, strength, context, pivot quality            ║
   ╚════════════════════════════════════════════════════════════════╝

5. 📉 VWAP & SUPPORT/RESISTANCE
   ╔════════════════════════════════════════════════════════════════╗
   ║ • VWAP daily/weekly/monthly                                    ║
   ║ • Détection automatique niveaux (clustering)                   ║
   ║ • IA: Level detector + force scoring                          ║
   ║ • Features: Distance VWAP, touches, volume aux niveaux        ║
   ╚════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════
                         🤖 PIPELINE MACHINE LEARNING
═══════════════════════════════════════════════════════════════════════

PHASE 1: DATA LABELING
┌─────────────────────────────────────────────────────────────────┐
│  Input: Historical OHLCV + Indicators                           │
│         ▼                                                       │
│  Lookforward: Analyze price 48h ahead                          │
│         ▼                                                       │
│  Label: BON si +3-5% gain sans -2% drawdown                    │
│         MAUVAIS sinon                                           │
│         ▼                                                       │
│  Output: Labeled dataset                                       │
└─────────────────────────────────────────────────────────────────┘

PHASE 2: FEATURE ENGINEERING
┌─────────────────────────────────────────────────────────────────┐
│  • Indicator values (MFI, WT, RSI, etc.)                       │
│  • Derivatives (slope, acceleration)                            │
│  • Multi-timeframe context                                      │
│  • Volume ratios                                                │
│  • Volatility measures                                          │
│  • Trend alignment (MA 50/200)                                  │
│  • Divergence flags                                             │
│  • 20-30 features par modèle                                    │
└─────────────────────────────────────────────────────────────────┘

PHASE 3: MODEL TRAINING
┌─────────────────────────────────────────────────────────────────┐
│  Split: 70% Train / 15% Validation / 15% Test                  │
│         ▼                                                       │
│  Algorithms: LightGBM, XGBoost, Random Forest                  │
│         ▼                                                       │
│  Hyperparameter Tuning: Optuna (Bayesian optimization)         │
│         ▼                                                       │
│  Cross-Validation: 5-fold time-series split                    │
│         ▼                                                       │
│  Output: Trained models (.pkl files)                           │
└─────────────────────────────────────────────────────────────────┘

PHASE 4: META-MODEL (Signal Aggregator)
┌─────────────────────────────────────────────────────────────────┐
│  Input: Predictions from all 4 base models                     │
│         ▼                                                       │
│  Stacking: Logistic Regression meta-learner                    │
│         ▼                                                       │
│  Confidence Scoring: 0.0 to 1.0                                │
│         ▼                                                       │
│  Output: STRONG_BUY / BUY / HOLD / SELL / STRONG_SELL          │
└─────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════
                         🔍 SCANNER EN TEMPS RÉEL
═══════════════════════════════════════════════════════════════════════

WORKFLOW (Every 5 minutes):

1. FETCH DATA
   ┌─────────────────────────────────────────┐
   │  Top 10 Cryptos × 3 Timeframes          │
   │  BTC, ETH, BNB, SOL, XRP, ADA, AVAX,   │
   │  DOT, MATIC, LINK                       │
   │  Timeframes: 1h, 4h, 1d                 │
   └─────────────────────────────────────────┘
                    ▼
2. CALCULATE INDICATORS
   ┌─────────────────────────────────────────┐
   │  MFI, Wave Trend, Momentum,             │
   │  Divergences, VWAP, Levels              │
   └─────────────────────────────────────────┘
                    ▼
3. ML PREDICTIONS
   ┌─────────────────────────────────────────┐
   │  Run all 5 models                       │
   │  Get probabilities & confidence         │
   └─────────────────────────────────────────┘
                    ▼
4. MULTI-TIMEFRAME CONFLUENCE
   ┌─────────────────────────────────────────┐
   │  Check alignment across timeframes      │
   │  Boost confidence if 3+ aligned         │
   └─────────────────────────────────────────┘
                    ▼
5. FILTER & RANK
   ┌─────────────────────────────────────────┐
   │  Filter: Confidence > 0.75              │
   │  Rank: By confidence score              │
   └─────────────────────────────────────────┘
                    ▼
6. ALERT
   ┌─────────────────────────────────────────┐
   │  Send top 3 opportunities               │
   │  Telegram / Discord notification        │
   └─────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════
                         📊 EXEMPLE DE SIGNAL
═══════════════════════════════════════════════════════════════════════

🔔 STRONG BUY ALERT - BTC/USDT
═════════════════════════════════════════════════

💰 Price: $67,850.00
📊 Confidence: 87%
⏰ Timestamp: 2025-10-30 14:30:00

─────────────────────────────────────────────────
INDICATORS:
─────────────────────────────────────────────────
💵 Money Flow: 18.5 (OVERSOLD) → Bullish
🌊 Wave Trend: WT1(-58) crossed WT2(-52) → BUY
📈 Momentum: 45.2 (GREEN) → Moderate
🔄 Divergence: Regular Bullish (Strength: 82%)
📉 VWAP: Price below VWAP → Opportunity

─────────────────────────────────────────────────
TIMEFRAME ALIGNMENT:
─────────────────────────────────────────────────
1h:  🟢 BUY
4h:  🟢 BUY
1d:  🟡 NEUTRAL
→ 2/3 timeframes aligned (GOOD)

─────────────────────────────────────────────────
KEY LEVELS:
─────────────────────────────────────────────────
🔻 Support:   $67,200 | $66,500
🔺 Resistance: $68,500 | $69,200

─────────────────────────────────────────────────
ML PREDICTIONS:
─────────────────────────────────────────────────
MFI Classifier:      91% (Excellent)
Wave Predictor:      84% (Good)
Momentum Analyzer:   79% (Good)
Pattern Recognizer:  82% (Good)
Meta-Model:          87% (STRONG BUY)

─────────────────────────────────────────────────
SUGGESTED TRADE:
─────────────────────────────────────────────────
Entry:       $67,850
Stop Loss:   $66,500 (-2.0%)
Take Profit: $71,250 (+5.0%)
Risk/Reward: 1:2.5

═════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════
                         📅 ROADMAP (14 SEMAINES)
═══════════════════════════════════════════════════════════════════════

SEMAINES 1-2:  🏗️  Fondations & Data Collection
               └─ Setup, API Binance, collecte données

SEMAINES 3-4:  📊 Indicateurs Market Cipher B
               └─ MFI, Wave Trend, Momentum, Divergences, VWAP

SEMAINES 5-6:  🔬 Préparation ML
               └─ Labeling, feature engineering, datasets

SEMAINES 7-9:  🤖 Entraînement Modèles IA
               └─ 5 modèles ML + optimisation

SEMAINES 10-11: 🔍 Scanner Multi-Crypto
                └─ Scanner temps réel, notifications

SEMAINES 12-13: 🧪 Backtesting
                └─ Validation historique, métriques

SEMAINE 14+:    🚀 Production
                └─ Deployment, dashboard, monitoring

═══════════════════════════════════════════════════════════════════════
                         🎯 MÉTRIQUES DE SUCCÈS
═══════════════════════════════════════════════════════════════════════

MODÈLES ML:
───────────────────────────────────────
Money Flow Classifier:     Accuracy > 65%, Precision > 70%
Wave Trend Predictor:      F1-Score > 0.70
Momentum Analyzer:         ROC-AUC > 0.75
Pattern Recognizer:        Recall > 80%
Signal Aggregator:         Win Rate > 55%

BACKTEST:
───────────────────────────────────────
Total Return:              Target: > 30% annual
Sharpe Ratio:              Target: > 1.5
Max Drawdown:              Target: < 20%
Profit Factor:             Target: > 1.8
Win Rate:                  Target: > 55%

PRODUCTION:
───────────────────────────────────────
Scan Cycle:                < 5 minutes (10 cryptos × 8 TF)
API Response:              < 200ms
Code Coverage:             > 80%

═══════════════════════════════════════════════════════════════════════
                         📦 STACK TECHNOLOGIQUE
═══════════════════════════════════════════════════════════════════════

LANGAGE:             Python 3.10+
DATA:                pandas, numpy
TECHNICAL ANALYSIS:  ta-lib, pandas-ta
MACHINE LEARNING:    scikit-learn, XGBoost, LightGBM
DEEP LEARNING:       TensorFlow, PyTorch (optionnel)
DATA COLLECTION:     ccxt, python-binance
VISUALIZATION:       matplotlib, plotly, seaborn
DASHBOARD:           Streamlit
BACKTESTING:         Custom framework
NOTIFICATIONS:       python-telegram-bot, discord-webhook
DATABASE:            SQLite / PostgreSQL, Redis (cache)

═══════════════════════════════════════════════════════════════════════
                         🚀 PROCHAINES ACTIONS
═══════════════════════════════════════════════════════════════════════

IMMÉDIAT:
  ☐ Exécuter: python setup_project.py (✅ FAIT)
  ☐ Créer environnement virtuel
  ☐ Installer dépendances (pip install -r requirements.txt)
  ☐ Configurer .env avec clés API Binance

CETTE SEMAINE:
  ☐ Implémenter utils/config.py
  ☐ Implémenter utils/logger.py
  ☐ Implémenter data_collection/binance_client.py
  ☐ Test connexion API

SEMAINE PROCHAINE:
  ☐ Implémenter data_collection/data_fetcher.py
  ☐ Collecter 1 an de données BTC/ETH/BNB
  ☐ Implémenter indicators/money_flow.py
  ☐ Créer notebook de visualisation MFI

═══════════════════════════════════════════════════════════════════════
                         ⚠️  DISCLAIMER
═══════════════════════════════════════════════════════════════════════

❌ Ce projet est ÉDUCATIF et EXPÉRIMENTAL
❌ Aucune garantie de profit
❌ Trading crypto = risque élevé de perte totale
❌ Pas de conseil financier
✅ Toujours faire ses propres recherches (DYOR)
✅ N'investir que ce qu'on peut se permettre de perdre
✅ Backtester extensivement avant trading réel

═══════════════════════════════════════════════════════════════════════

📚 DOCUMENTATION COMPLÈTE:
   • README.md - Vue d'ensemble
   • PROJECT_PLAN.md - Plan détaillé
   • TECHNICAL_SPECS.md - Spécifications techniques
   • GETTING_STARTED.md - Guide de démarrage
   • TODO.md - Liste de tâches
   • CONTRIBUTING.md - Guide de contribution

═══════════════════════════════════════════════════════════════════════

            🎉 PROJET SIGNALCIPHER PRÊT À DÉMARRER! 🎉
                      Bonne chance! 🚀

═══════════════════════════════════════════════════════════════════════
```
