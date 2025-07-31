# modules/indicators.py

import pandas_ta as ta
import pandas as pd

def add_all_indicators(df, config):
    """
    Ajoute tous les indicateurs techniques nécessaires au DataFrame en utilisant pandas-ta.

    Cette fonction modifie le DataFrame en place en y ajoutant les colonnes
    correspondant à chaque indicateur.

    Args:
        df (pandas.DataFrame): Le DataFrame OHLCV ('open', 'high', 'low', 'close', 'volume').
        config (module): Le module de configuration du projet important les paramètres.

    Returns:
        pandas.DataFrame: Le DataFrame avec les colonnes d'indicateurs ajoutées.
                          Retourne None si le DataFrame d'entrée est invalide.
    """
    if df is None or df.empty:
        print("ERREUR : Le DataFrame fourni est vide. Impossible d'ajouter des indicateurs.")
        return None

    print("Calcul et ajout des indicateurs techniques...")
    
    try:
        # Appliquer une stratégie personnalisée avec pandas-ta.
        # C'est plus propre que d'appeler chaque indicateur un par un.
        custom_strategy = ta.Strategy(
            name="CipherSignal_Base",
            description="Indicateurs de base pour CipherSignal",
            ta=[
                {"kind": "mfi", "length": config.MFI_LENGTH},
                {"kind": "vwap"},
                {"kind": "stochrsi", "rsi_length": config.RSI_LENGTH, "length": config.STOCH_RSI_LENGTH, "k": config.K_SMOOTH, "d": config.D_SMOOTH},
                {"kind": "rsi", "length": config.RSI_LENGTH},
                {"kind": "macd", "fast": config.MACD_FAST, "slow": config.MACD_SLOW, "signal": config.MACD_SIGNAL}
            ]
        )
        
        # Appliquer la stratégie au DataFrame
        df.ta.strategy(custom_strategy)
        
        # Les indicateurs sont ajoutés avec des noms de colonnes comme 'MFI_14'.
        # On nettoie les lignes qui contiennent des NaN après les calculs.
        df.dropna(inplace=True)
        
        print("SUCCÈS : Indicateurs (MFI, VWAP, StochRSI, RSI, MACD) ajoutés.")
        
        return df
        
    except Exception as e:
        print(f"ERREUR CRITIQUE : Une exception est survenue lors du calcul des indicateurs : {e}")
        return None 