# modules/indicators.py

import pandas as pd
import numpy as np

def add_all_indicators(df, config):
    """
    Ajoute tous les indicateurs techniques nécessaires au DataFrame en utilisant des calculs manuels.

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
        # Copie du DataFrame pour éviter de modifier l'original
        result_df = df.copy()
        
        # 1. Calcul du RSI
        result_df['rsi'] = calculate_rsi(result_df['close'], config.RSI_LENGTH)
        
        # 2. Calcul du MFI (Money Flow Index)
        result_df['mfi'] = calculate_mfi(result_df, config.MFI_LENGTH)
        
        # 3. Calcul du VWAP (Volume Weighted Average Price)
        result_df['vwap'] = calculate_vwap(result_df)
        
        # 4. Calcul du MACD
        macd_data = calculate_macd(result_df['close'], config.MACD_FAST, config.MACD_SLOW, config.MACD_SIGNAL)
        result_df['macd'] = macd_data['macd']
        result_df['macd_signal'] = macd_data['signal']
        result_df['macd_histogram'] = macd_data['histogram']
        
        # 5. Calcul du Stochastic RSI
        stoch_rsi = calculate_stoch_rsi(result_df['close'], config.RSI_LENGTH, config.STOCH_RSI_LENGTH, config.K_SMOOTH, config.D_SMOOTH)
        result_df['stoch_rsi_k'] = stoch_rsi['k']
        result_df['stoch_rsi_d'] = stoch_rsi['d']
        
        # Nettoyage des lignes avec des NaN
        result_df.dropna(inplace=True)
        
        print("SUCCÈS : Indicateurs (RSI, MFI, VWAP, MACD, StochRSI) ajoutés.")
        
        return result_df
        
    except Exception as e:
        print(f"ERREUR CRITIQUE : Une exception est survenue lors du calcul des indicateurs : {e}")
        return None

def calculate_rsi(prices, period=14):
    """Calcule le RSI (Relative Strength Index)"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_mfi(df, period=14):
    """Calcule le MFI (Money Flow Index)"""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    money_flow = typical_price * df['volume']
    
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(window=period).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(window=period).sum()
    
    mfi = 100 - (100 / (1 + positive_flow / negative_flow))
    return mfi

def calculate_vwap(df):
    """Calcule le VWAP (Volume Weighted Average Price)"""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    vwap = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
    return vwap

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calcule le MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }

def calculate_stoch_rsi(prices, rsi_length=14, stoch_length=14, k_smooth=3, d_smooth=3):
    """Calcule le Stochastic RSI"""
    rsi = calculate_rsi(prices, rsi_length)
    
    # Calcul du %K
    rsi_min = rsi.rolling(window=stoch_length).min()
    rsi_max = rsi.rolling(window=stoch_length).max()
    k_raw = 100 * (rsi - rsi_min) / (rsi_max - rsi_min)
    k = k_raw.rolling(window=k_smooth).mean()
    
    # Calcul du %D
    d = k.rolling(window=d_smooth).mean()
    
    return {
        'k': k,
        'd': d
    } 