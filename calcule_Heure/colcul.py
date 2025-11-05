from datetime import datetime, timedelta

def calculer_moyennes(horaires):
    """Calcule les moyennes des heures d'arrivée, de départ et de pause."""
    total_depart = timedelta()
    total_arrivee = timedelta()
    total_pause = timedelta()
    nb_lignes = len(horaires)

    for ligne in horaires:
        try:
            debut = datetime.strptime(ligne["Heure début"], "%H:%M")
            depart = datetime.strptime(ligne["Heure départ calculée"], "%H:%M")
            pause_debut = datetime.strptime(ligne["Heure début pause"], "%H:%M")
            pause_fin = datetime.strptime(ligne["Heure fin pause"], "%H:%M")
        except ValueError:
            nb_lignes -= 1
            continue
        total_arrivee += timedelta(hours=debut.hour, minutes=debut.minute)
        total_depart += timedelta(hours=depart.hour, minutes=depart.minute)
        total_pause += (pause_fin - pause_debut)

    if nb_lignes == 0:
        return None, None, None

    arrivee_moy = total_arrivee / nb_lignes
    depart_moy = total_depart / nb_lignes
    pause_moy = total_pause / nb_lignes

    arrivee_moy_str = f"{int(arrivee_moy.seconds // 3600):02d}:{int((arrivee_moy.seconds % 3600) // 60):02d}"
    depart_moy_str = f"{int(depart_moy.seconds // 3600):02d}:{int((depart_moy.seconds % 3600) // 60):02d}"
    pause_moy_str = f"{int(pause_moy.seconds // 3600):02d}:{int((pause_moy.seconds % 3600) // 60):02d}"

    return depart_moy_str, pause_moy_str, arrivee_moy_str
