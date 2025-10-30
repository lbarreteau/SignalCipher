# 🔐 SignalCipher

> **Reproduction intelligente de Market Cipher B avec Machine Learning**

Un système d'analyse technique avancé qui reproduit l'indicateur Market Cipher B et utilise l'IA pour apprendre automatiquement à identifier les meilleurs signaux de trading sur le Top 10 des cryptomonnaies en multi-timeframes.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()

---

## 🎯 Objectifs

- ✅ **Reproduction fidèle** de tous les sous-indicateurs de Market Cipher B
- 🤖 **IA pour chaque indicateur** - apprentissage automatique des patterns
- 📊 **Scanner automatique** - Top 10 cryptos en temps réel
- ⏰ **Multi-timeframes** - Analyse simultanée de 1m à 1W
- 📈 **Signaux exploitables** - Notifications avec niveau de confiance

---

## 📊 Sous-Indicateurs Implémentés

| Indicateur | Description | IA Intégrée | Status |
|-----------|-------------|-------------|--------|
| **Money Flow Index** | Volume-weighted RSI | ✅ Classifier | 🔴 TODO |
| **Wave Trend** | Oscillateur de tendance | ✅ Predictor | 🔴 TODO |
| **Momentum Waves** | Multi-RSI composite | ✅ Analyzer | 🔴 TODO |
| **Divergences** | Détection divergences | ✅ Recognizer | 🔴 TODO |
| **VWAP & Levels** | Support/Résistance | ✅ Level Detector | 🔴 TODO |

---

## 🚀 Installation Rapide

### Prérequis
```bash
Python 3.10+
pip
Git
```

### Installation

```bash
# Cloner le repo
git clone https://github.com/lbarreteau/SignalCipher.git
cd SignalCipher

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec vos clés API
```

### Configuration API Binance

1. Créer un compte sur [Binance](https://www.binance.com)
2. Générer API Key (Read Only suffit)
3. Ajouter dans `.env`:

```bash
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_secret_here
```

---

## 📖 Usage

### 1. Collecter les Données

```bash
# Télécharger données historiques (1 an)
python -m data_collection.data_fetcher \
    --symbols BTC,ETH,BNB,SOL \
    --timeframes 1h,4h,1d \
    --days 365
```

### 2. Calculer les Indicateurs

```bash
# Calculer tous les indicateurs Market Cipher B
python -m indicators.calculate_all \
    --input data/raw/ \
    --output data/processed/
```

### 3. Entraîner les Modèles IA

```bash
# Entraîner le modèle Money Flow
python -m training.model_trainer \
    --indicator money_flow \
    --data data/processed/ \
    --output models/

# Entraîner tous les modèles
python -m training.train_all_models
```

### 4. Scanner en Temps Réel

```bash
# Scanner le Top 10 cryptos
python main.py \
    --mode scanner \
    --top 10 \
    --timeframes 1h,4h,1d \
    --interval 300  # scan toutes les 5 minutes
```

### 5. Dashboard Web

```bash
# Lancer l'interface Streamlit
streamlit run dashboard/app.py
```

Accéder à: `http://localhost:8501`

---

## 🏗️ Structure du Projet

```
SignalCipher/
├── 📊 data/                    # Données de marché
│   ├── raw/                    # OHLCV brutes
│   ├── processed/              # Avec indicateurs
│   └── training/               # Datasets ML
│
├── 📈 indicators/              # Indicateurs Market Cipher B
│   ├── money_flow.py          # MFI
│   ├── wave_trend.py          # Wave Trend
│   ├── momentum_waves.py      # Momentum
│   ├── divergences.py         # Divergences
│   └── vwap.py                # VWAP & Levels
│
├── 🤖 ml_models/               # Modèles d'IA
│   ├── money_flow_classifier.py
│   ├── wave_trend_predictor.py
│   ├── momentum_analyzer.py
│   └── signal_aggregator.py
│
├── 🔍 scanner/                 # Scanner crypto
│   ├── crypto_scanner.py
│   ├── timeframe_analyzer.py
│   └── signal_generator.py
│
├── 🎓 training/                # Entraînement ML
│   ├── data_labeling.py
│   ├── feature_engineering.py
│   └── model_trainer.py
│
├── 📱 dashboard/               # Interface web
│   └── app.py
│
├── 🛠️ utils/                   # Utilitaires
│   ├── config.py
│   ├── logger.py
│   └── visualizer.py
│
├── 📋 config/                  # Configuration
│   ├── config.yaml
│   ├── symbols.yaml
│   └── timeframes.yaml
│
├── 🧪 tests/                   # Tests
├── 📓 notebooks/               # Jupyter notebooks
├── 💾 models/                  # Modèles sauvegardés
└── 📄 docs/                    # Documentation
```

---

## 🤖 Modèles d'IA

### Money Flow Classifier
- **Type:** Binary Classification
- **Algo:** LightGBM
- **Objectif:** Détecter vrais signaux de retournement
- **Performance cible:** Accuracy > 65%, Precision > 70%

### Wave Trend Predictor
- **Type:** Multi-class (BUY/HOLD/SELL)
- **Algo:** XGBoost
- **Objectif:** Prédire direction après croisement
- **Performance cible:** F1-Score > 0.70

### Momentum Analyzer
- **Type:** Regression + Classification
- **Algo:** Random Forest
- **Objectif:** Mesurer force du momentum
- **Performance cible:** ROC-AUC > 0.75

### Pattern Recognizer
- **Type:** Detection + Classification
- **Algo:** Ensemble (RF + GB)
- **Objectif:** Identifier divergences valides
- **Performance cible:** Recall > 80%

### Signal Aggregator (Meta-Modèle)
- **Type:** Ensemble Stacking
- **Algo:** Voting + LogisticRegression
- **Objectif:** Combiner tous les signaux
- **Performance cible:** Win Rate > 55%, Sharpe > 1.5

---

## 📊 Timeframes Supportés

- **Ultra Court Terme:** 1m, 5m, 15m (Scalping)
- **Court Terme:** 30m, 1h (Intraday)
- **Moyen Terme:** 4h, 1D (Swing)
- **Long Terme:** 3D, 1W (Position)

**Signal optimal:** Confluence sur au moins 3 timeframes alignés

---

## 🔍 Cryptos Scannées (Top 10)

1. BTC/USDT - Bitcoin
2. ETH/USDT - Ethereum
3. BNB/USDT - Binance Coin
4. SOL/USDT - Solana
5. XRP/USDT - Ripple
6. ADA/USDT - Cardano
7. AVAX/USDT - Avalanche
8. DOT/USDT - Polkadot
9. MATIC/USDT - Polygon
10. LINK/USDT - Chainlink

*Configuration ajustable dans `config/symbols.yaml`*

---

## 📈 Exemple de Signal

```json
{
  "symbol": "BTC/USDT",
  "timestamp": "2025-10-30 14:30:00",
  "signal": "STRONG_BUY",
  "confidence": 0.87,
  "price": 67850.00,
  "indicators": {
    "money_flow": {
      "value": 18.5,
      "status": "oversold",
      "signal": "bullish"
    },
    "wave_trend": {
      "wt1": -58.3,
      "wt2": -52.1,
      "cross": "bullish",
      "signal": "buy"
    },
    "momentum": {
      "value": 45.2,
      "color": "green",
      "strength": "moderate"
    },
    "divergence": {
      "type": "regular_bullish",
      "strength": 0.82
    }
  },
  "timeframe_alignment": {
    "1h": "BUY",
    "4h": "BUY",
    "1d": "NEUTRAL"
  },
  "key_levels": {
    "support": [67200, 66500],
    "resistance": [68500, 69200]
  },
  "ml_predictions": {
    "mfi_classifier": 0.91,
    "wave_predictor": 0.84,
    "momentum_analyzer": 0.79,
    "meta_model": 0.87
  }
}
```

---

## 🧪 Backtesting

```bash
# Backtest sur données historiques
python -m backtesting.run_backtest \
    --symbol BTC/USDT \
    --start 2023-01-01 \
    --end 2024-12-31 \
    --timeframe 1h \
    --initial_capital 10000

# Résultats attendus
# Total Return: 45.2%
# Sharpe Ratio: 1.82
# Max Drawdown: -12.3%
# Win Rate: 58.7%
# Profit Factor: 2.1
```

---

## 🔔 Notifications

### Telegram Bot

```bash
# Configuration
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Test
python -m utils.send_test_notification
```

### Discord Webhook

```bash
# Configuration
DISCORD_WEBHOOK_URL=your_webhook_url

# Test
python -m utils.send_test_discord
```

---

## 📚 Documentation Complète

- 📋 **[Plan du Projet](PROJECT_PLAN.md)** - Roadmap détaillée
- 🔬 **[Spécifications Techniques](TECHNICAL_SPECS.md)** - Détails techniques
- 📖 **[Guide d'Utilisation](docs/USER_GUIDE.md)** - Guide utilisateur
- 🤖 **[Documentation IA](docs/ML_DOCUMENTATION.md)** - Modèles ML
- 📊 **[Guide de Trading](docs/TRADING_GUIDE.md)** - Interprétation des signaux

---

## 🛠️ Développement

### Installer en mode développement

```bash
pip install -e .
pip install -r requirements-dev.txt
```

### Tests

```bash
# Tous les tests
pytest

# Tests avec coverage
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest tests/test_indicators.py
```

### Linting & Formatting

```bash
# Format code
black .

# Lint
flake8 .

# Type checking
mypy .
```

---

## 🤝 Contribution

Les contributions sont bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

### Workflow
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📊 Roadmap

- [x] **Phase 0:** Définition du plan (✅ Terminé)
- [ ] **Phase 1:** Setup & Data Collection (🔴 En cours)
- [ ] **Phase 2:** Implémentation Indicateurs
- [ ] **Phase 3:** Préparation ML
- [ ] **Phase 4:** Entraînement IA
- [ ] **Phase 5:** Scanner Multi-Crypto
- [ ] **Phase 6:** Backtesting
- [ ] **Phase 7:** Production

*Durée estimée: 14 semaines*

Voir [PROJECT_PLAN.md](PROJECT_PLAN.md) pour détails complets.

---

## ⚠️ Disclaimer

**ATTENTION:** Ce projet est à des fins éducatives et de recherche uniquement.

- ❌ Pas de conseil financier
- ❌ Pas de garantie de profits
- ❌ Trading crypto = risque élevé de perte
- ✅ Toujours faire ses propres recherches (DYOR)
- ✅ N'investir que ce qu'on peut se permettre de perdre

**Les auteurs ne sont pas responsables des pertes financières.**

---

## 📄 License

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

**Lucas Barreteau**  
- GitHub: [@lbarreteau](https://github.com/lbarreteau)

---

## 🙏 Remerciements

- Market Cipher pour l'inspiration de l'indicateur
- Communauté crypto pour le support
- Binance pour l'API

---

## 📞 Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/lbarreteau/SignalCipher/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/lbarreteau/SignalCipher/discussions)
- 📧 **Email:** support@signalcipher.com

---

<div align="center">

**⭐ Si ce projet t'aide, donne-lui une étoile sur GitHub ! ⭐**

Made with ❤️ and ☕ by the SignalCipher Team

</div>
