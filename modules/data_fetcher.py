# modules/data_fetcher.py

import yfinance as yf
import pandas as pd

def get_crypto_data(ticker, period, interval):
    """
    Récupère les données historiques OHLCV pour une cryptomonnaie depuis Yahoo Finance.

    Cette fonction se connecte à l'API de yfinance, télécharge les données,
    standardise le format des colonnes et gère les erreurs potentielles.

    Args:
        ticker (str): Le symbole de la cryptomonnaie (ex: 'BTC-USD').
        period (str): La période de données à récupérer (ex: '1y' pour 1 an).
        interval (str): L'intervalle de temps entre les points de données (ex: '1d' pour journalier).

    Returns:
        pandas.DataFrame: Un DataFrame contenant les données OHLCV. 
                          Les colonnes sont standardisées en minuscules.
                          Retourne None si une erreur survient ou si aucune donnée n'est trouvée.
    """
    print(f"Tentative de récupération des données pour {ticker}...")
    try:
        # Téléchargement des données depuis yfinance
        data = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            progress=False  # Désactive la barre de progression pour un script propre
        )

        # Vérification si le DataFrame est vide
        if data.empty:
            print(f"ERREUR : Aucune donnée n'a été trouvée pour le ticker '{ticker}'.")
            print("Veuillez vérifier que le ticker est correct et qu'il existe pour la période demandée.")
            return None
        
        # yfinance retourne parfois des colonnes avec des majuscules. On standardise.
        data.columns = [col.lower().replace(' ', '_') for col in data.columns]
        
        print(f"SUCCÈS : Données pour {ticker} récupérées. {len(data)} lignes chargées.")
              
        return data

    except Exception as e:
        print(f"ERREUR CRITIQUE : Une exception est survenue lors de la récupération des données : {e}")
        return None 