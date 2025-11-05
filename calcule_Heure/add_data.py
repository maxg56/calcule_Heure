from datetime import datetime, timedelta
import csv
import os

fichier_csv = 'calcule_Heure/horaires.csv'

def ajouter_donnees(heure_debut=None, heure_pause_debut=None, heure_pause_fin=None):
    """
    Ajoute des données d'horaires dans le CSV.
    Si les heures ne sont pas fournies, demande à l'utilisateur de les saisir.
    Retourne l'heure de départ calculée.
    """
    tab_heure_debut = []

    if heure_debut and heure_pause_debut and heure_pause_fin:
        # Mode programmation : utiliser les valeurs fournies
        tab_heure_debut = [heure_debut, heure_pause_debut, heure_pause_fin]
    else:
        # Mode interactif : demander à l'utilisateur
        for texte in ["début travail", "début pause", "fin pause"]:
            while True:
                heure = input(f"Entrez l'heure {texte} (HH:MM) : ")
                try:
                    datetime.strptime(heure, "%H:%M")
                    tab_heure_debut.append(heure)
                    break
                except ValueError:
                    print("Format incorrect, veuillez entrer au format HH:MM.")

    # Calcul de l'heure de départ
    duree_travail = timedelta(hours=7, minutes=10)
    heure_debut_dt = datetime.strptime(tab_heure_debut[0], "%H:%M")
    pause_debut = datetime.strptime(tab_heure_debut[1], "%H:%M")
    pause_fin = datetime.strptime(tab_heure_debut[2], "%H:%M")
    duree_pause = pause_fin - pause_debut
    heure_depart = heure_debut_dt + duree_travail + duree_pause

    # Vérifie si le fichier existe
    fichier_existe = os.path.exists(fichier_csv)

    # Écriture dans le CSV
    with open(fichier_csv, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not fichier_existe:
            writer.writerow([
                "Date de saisie",
                "Heure début",
                "Heure début pause",
                "Heure fin pause",
                "Heure départ calculée"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tab_heure_debut[0],
            tab_heure_debut[1],
            tab_heure_debut[2],
            heure_depart.strftime("%H:%M")
        ])

    return heure_depart.strftime("%H:%M")
