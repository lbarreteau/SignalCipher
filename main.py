# main.py

import pandas as pd
from modules import data_fetcher, indicators
import config

def run_analysis():
    """
    Fonction principale qui orchestre le pipeline d'analyse de CipherSignal.
    
    Ce pipeline se déroule en trois étapes :
    1. Récupération des données de marché brutes.
    2. Calcul et ajout des indicateurs techniques sur ces données.
    3. Affichage du résultat final pour vérification.
    """
    print("--- Lancement du script d'analyse CipherSignal ---")
    
    # --- Étape 1: Récupérer les données de marché depuis la source ---
    market_data = data_fetcher.get_crypto_data(
        ticker=config.CRYPTO_TICKER,
        period=config.DATA_PERIOD,
        interval=config.DATA_INTERVAL
    )

    # Vérification après l'étape 1 : Si les données n'ont pas pu être récupérées, on arrête tout.
    if market_data is None:
        print("--- Arrêt du script : Échec de la récupération des données. ---")
        return

    # --- Étape 2: Calculer et ajouter les indicateurs techniques ---
    data_with_indicators = indicators.add_all_indicators(
        df=market_data,
        config=config
    )

    # Vérification après l'étape 2 : Si les indicateurs n'ont pas pu être calculés, on arrête.
    if data_with_indicators is None:
        print("--- Arrêt du script : Échec du calcul des indicateurs. ---")
        return

    # --- Étape 3: Afficher les résultats pour vérification ---
    print("\n--- ✅ Analyse terminée. Aperçu des dernières données analysées : ---")
    
    # On configure Pandas pour afficher toutes les colonnes, c'est plus pratique
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000) # Élargit la console pour éviter les retours à la ligne
    
    # On affiche les 5 dernières lignes du DataFrame final
    print(data_with_indicators.tail(25))
    
    print("\n--- Fin du script CipherSignal ---")

if __name__ == "__main__":
    # Cette syntaxe garantit que run_analysis() n'est appelé que lorsque
    # le script est exécuté directement (et non quand il est importé).
    run_analysis() 