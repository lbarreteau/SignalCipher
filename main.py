# main.py

import pandas as pd
from modules import data_fetcher, indicators
import config
import operator


def compute_interval(interval):
    """Exécute le pipeline complet pour un intervalle donné et retourne (data, score)."""
    print(f"\n=== ⏱️ Analyse de l'intervalle {interval} ===")
    market_data = data_fetcher.get_crypto_data(
        ticker=config.CRYPTO_TICKER,
        period=config.DATA_PERIOD,
        interval=interval
    )
    if market_data is None:
        print(f"⚠️  Données manquantes pour l'intervalle {interval}. On ignore.")
        return None, None

    data_with_indicators = indicators.add_all_indicators(df=market_data, config=config)
    if data_with_indicators is None or len(data_with_indicators) == 0:
        print(f"⚠️  Indicateurs non calculés pour {interval}. On ignore.")
        return None, None

    current_score = data_with_indicators['global_score'].iloc[-1]
    print(f"Score global {interval}: {current_score:.1f}/100")
    return data_with_indicators, current_score


def display_detailed(data_with_indicators):
    """Réutilise l'affichage détaillé déjà présent pour un seul DataFrame."""
    # Reprise du code d'affichage détaillé (valorisation + scores)
    total_data = len(data_with_indicators)
    print(f"\n📊 Données analysées : {total_data} points")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(data_with_indicators.tail(5))

    # Scores moyens
    print("\n--- 📊 Scores moyens des indicateurs (sur 100) : ---")
    score_columns = ['rsi_score', 'mfi_score', 'vwap_score', 'macd_score', 'stoch_rsi_score', 'bb_score', 'adx_score', 'global_score']
    for col in score_columns:
        if col in data_with_indicators.columns:
            avg_score = data_with_indicators[col].mean()
            print(f"{col.replace('_score', '').upper()}: {avg_score:.1f}/100")

    # Détail dernière bougie (valeurs + scores)
    if len(data_with_indicators) > 0:
        print("\n--- 🔍 Détail des indicateurs (dernière donnée) : ---")
        last_row = data_with_indicators.iloc[-1]
        def safe(col):
            return last_row[col] if col in last_row else float('nan')
        print(f"RSI: {safe('rsi'):.2f} → Score: {safe('rsi_score'):.1f}/100")
        print(f"MFI: {safe('mfi'):.2f} → Score: {safe('mfi_score'):.1f}/100")
        print(f"VWAP: {safe('vwap'):.2f} → Score: {safe('vwap_score'):.1f}/100")
        print(f"MACD: {safe('macd'):.4f} | Signal: {safe('macd_signal'):.4f} | Hist: {safe('macd_histogram'):.4f} → Score: {safe('macd_score'):.1f}/100")
        print(f"StochRSI: K={safe('stoch_rsi_k'):.2f} | D={safe('stoch_rsi_d'):.2f} → Score: {safe('stoch_rsi_score'):.1f}/100")
        print(f"Bollinger: Upper={safe('bb_upper'):.2f} | Middle={safe('bb_middle'):.2f} | Lower={safe('bb_lower'):.2f} → Score: {safe('bb_score'):.1f}/100")
        print(f"ADX: {safe('adx'):.2f} → Score: {safe('adx_score'):.1f}/100")


def run_analysis():
    """Teste plusieurs intervalles et affiche celui avec le meilleur score global."""
    print("--- Lancement du script d'analyse CipherSignal (multi-intervalles) ---")

    test_intervals = getattr(config, 'TEST_INTERVALS', [config.DATA_INTERVAL])
    results = {}

    for itv in test_intervals:
        data, score = compute_interval(itv)
        if score is not None:
            results[itv] = (data, score)

    if not results:
        print("❌ Aucune analyse valide n'a pu être effectuée.")
        return

    # Trouver le meilleur intervalle
    best_interval, (best_data, best_score) = max(results.items(), key=lambda x: x[1][1])
    print("\n==============================")
    print(f"🏆 Meilleur intervalle : {best_interval} avec un score {best_score:.1f}/100")
    print("==============================")

    # Affichage détaillé pour le meilleur intervalle
    display_detailed(best_data)

    print("\n--- Fin du script CipherSignal ---")


if __name__ == "__main__":
    run_analysis() 