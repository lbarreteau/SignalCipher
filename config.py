# config.py

# -- Configuration du Marché --
# Le ticker de la cryptomonnaie à analyser (format Yahoo Finance)
# Exemples : 'BTC-USD', 'ETH-USD', 'SOL-USD'
CRYPTO_TICKER = 'BTC-USD'

# La période des données à récupérer
# Exemples : '1y' (1 an), '6mo' (6 mois), '1d' (1 jour)
DATA_PERIOD = '1y'

# L'intervalle de temps pour les bougies
# Exemples : '1d' (journalier), '1h' (horaire), '4h'
DATA_INTERVAL = '1h'

# Liste des intervalles à tester pour trouver le meilleur (optionnel)
# Exemple : ['15m', '30m', '1h', '2h', '4h', '1d']
TEST_INTERVALS = ['15m', '30m', '1h', '2h', '4h']

# Nombre de données récentes à analyser (0 = toutes les données)


# -- Configuration des Indicateurs --
# Ces valeurs sont des standards couramment utilisés, mais peuvent être ajustées.

# Paramètres pour le Money Flow Index (MFI)
MFI_LENGTH = 14

# Paramètres pour le Relative Strength Index (RSI)
# Utilisé comme base pour la détection de divergence et pour le StochRSI.
RSI_LENGTH = 14

# Paramètres pour le Stochastic RSI (StochRSI)
STOCH_RSI_LENGTH = 14
# Le 'k' et 'd' sont des périodes de lissage pour le StochRSI.
K_SMOOTH = 3
D_SMOOTH = 3

# Paramètres pour le MACD (Proxy des Ondes de Tendance)
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9 