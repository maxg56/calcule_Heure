"""
Version ligne de commande de l'application de gestion des horaires.
Pour la version web, utilisez : streamlit run app.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'calcule_Heure'))

from graphique import generer_graphiques
from add_data import ajouter_donnees
from colcul import calculer_moyennes
from open_csv import lire_horaires
from utiles import afficher_resume
import matplotlib.pyplot as plt

fichier_csv = 'calcule_Heure/horaires.csv'

# ----------------- MENU INTERACTIF -----------------
def menu():
    while True:
        print("\n=== Menu Horaires ===")
        print("1. Ajouter une nouvelle saisie")
        print("2. Analyser les données et générer graphiques")
        print("3. Quitter")
        choix = input("Choisissez une option (1-3) : ")
        arge = choix.split(" ")

        if arge[0] == "1":
            ajouter_donnees()
            print(f"Les données ont été ajoutées dans '{fichier_csv}'.")

        elif arge[0] == "2":
            try:
                horaires = lire_horaires(fichier_csv)
            except FileNotFoundError:
                print(f"Le fichier '{fichier_csv}' est introuvable.")
                continue

            afficher_resume(horaires)
            depart_moy, pause_moy, arrivee_moy = calculer_moyennes(horaires)

            if depart_moy and pause_moy:
                print(f"\nHeure moyenne d'arrivée : {arrivee_moy}")
                print(f"Heure moyenne de départ : {depart_moy}")
                print(f"Durée moyenne de pause : {pause_moy}")

            fig1, fig2, fig3 = generer_graphiques(horaires, depart_moy, arrivee_moy)
            if fig1 and fig2 and fig3:
                plt.show()
        else:
            print("Au revoir!")
            break

# ----------------- MAIN -----------------
if __name__ == "__main__":
    menu()
