from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def generer_graphiques(horaires, depart_moy, arrivee_moy):
    """Génère les graphiques d'évolution des horaires."""
    dates, heures_depart, heures_arrivee, durees_pause = [], [], [], []

    for ligne in horaires:
        try:
            date = datetime.strptime(ligne["Date de saisie"], "%Y-%m-%d %H:%M:%S")
            debut = datetime.strptime(ligne["Heure début"], "%H:%M")
            depart = datetime.strptime(ligne["Heure départ calculée"], "%H:%M")
            pause_debut = datetime.strptime(ligne["Heure début pause"], "%H:%M")
            pause_fin = datetime.strptime(ligne["Heure fin pause"], "%H:%M")
        except ValueError:
            continue

        dates.append(date)
        heures_arrivee.append(debut.hour + debut.minute / 60)
        heures_depart.append(depart.hour + depart.minute / 60)
        durees_pause.append((pause_fin - pause_debut).seconds / 60)

    if not dates:
        print("Aucune donnée valide pour générer les graphiques.")
        return None, None, None

    # Conversion des heures moyennes
    h, m = map(int, arrivee_moy.split(":"))
    arrivee_moy_decimal = h + m / 60
    h, m = map(int, depart_moy.split(":"))
    depart_moy_decimal = h + m / 60

    # Graphique 1 : Heure d'arrivée
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(dates, heures_arrivee, marker='o', linestyle='-', label="Heure d'arrivée")
    ax1.set_title("Évolution des heures d'arrivée")
    ax1.set_xlabel("Date de saisie")
    ax1.set_ylabel("Heure d'arrivée (heures décimales)")
    ax1.axhline(arrivee_moy_decimal, color='red', linestyle='--', linewidth=2, label='Moyenne')
    ax1.grid(True)
    ax1.legend()
    plt.tight_layout()

    # Graphique 2 : Heure de départ
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(dates, heures_depart, marker='o', linestyle='-', color='green', label='Heure de départ')
    ax2.set_title("Évolution des heures de départ")
    ax2.set_xlabel("Date de saisie")
    ax2.set_ylabel("Heure de départ (heures décimales)")
    ax2.axhline(depart_moy_decimal, color='red', linestyle='--', linewidth=2, label='Moyenne')
    ax2.grid(True)
    ax2.legend()
    plt.tight_layout()

    # Graphique 3 : Durée des pauses
    class MidpointNormalize(mcolors.Normalize):
        def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
            self.midpoint = midpoint
            super().__init__(vmin, vmax, clip)

        def __call__(self, value, clip=None):
            result, is_scalar = self.process_value(value)
            vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint
            result = np.interp(result, [vmin, midpoint, vmax], [0, 0.5, 1])
            return np.ma.masked_array(result)

    norm = MidpointNormalize(vmin=min(durees_pause), vmax=max(durees_pause), midpoint=45)
    cmap = plt.cm.RdYlGn
    couleurs = [cmap(norm(val)) for val in durees_pause]

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.bar(dates, durees_pause, color=couleurs, label='Durée de la pause (min)')
    ax3.set_title("Durée des pauses au fil du temps")
    ax3.set_xlabel("Date de saisie")
    ax3.set_ylabel("Durée de la pause (minutes)")
    ax3.grid(True, axis='y')
    ax3.axhline(45, color='red', linestyle='--', linewidth=2, label='Seuil 45 min')
    ax3.legend()
    plt.tight_layout()

    return fig1, fig2, fig3
