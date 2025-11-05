import csv

def lire_horaires(fichier):
    """Lit les horaires depuis un fichier CSV."""
    with open(fichier, mode='r', encoding='utf-8') as f:
        return list(csv.DictReader(f))
