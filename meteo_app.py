
# Les imports de tkinter
import tkinter as tk
from tkinter import messagebox

# Les imports de l'API
import urllib.request
import json


# ================ les fonctions API

# Ville -> coordonnées GPS 
def get_coordonnees(nom_ville):
    ville_encodee = nom_ville.replace(" ", "%20")
    url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={ville_encodee}&count=1&format=json"
    
    try:
        reponse = urllib.request.urlopen(url_geo)
        donnees = reponse.read().decode('utf-8')
        resultat = json.loads(donnees)
    except Exception as e:
        print("Erreur lors de la requête à l'API de géocodage :", e)
        return None
    
    if resultat.get('results'):
        infos_ville = resultat['results'][0]
        return {
            'nom': infos_ville['name'],
            'pays': infos_ville['country'],
            'latitude': infos_ville['latitude'],
            'longitude': infos_ville['longitude']
        }
    return None


# Coordonnées GPS -> météo actuelle
def get_meteo(latitude, longitude):
    url_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    try:
        reponse = urllib.request.urlopen(url_meteo)
        donnees = reponse.read().decode('utf-8')
        return json.loads(donnees)
    except Exception as e:
        print("Erreur lors de la requête à l'API de météo :", e)
        return None


# Traduction du code météo WMO en texte lisible
def traduire_code_meteo(code):
    codes = {
        0: "☀️ Ciel clair",
        1: "⛅ Nuageux", 2: "⛅ Nuageux",
        3: "☁️ Couvert",
        45: "🌫️ Brouillard", 48: "🌫️ Brouillard",
        51: "🌧️ Bruine", 53: "🌧️ Bruine", 55: "🌧️ Bruine",
        61: "🌧️ Pluie", 63: "🌧️ Pluie", 65: "🌧️ Pluie",
        71: "❄️ Neige", 73: "❄️ Neige", 75: "❄️ Neige",
        95: "⛈️ Orage", 96: "⛈️ Orage", 99: "⛈️ Orage"
    }
    return codes.get(code, "❓ Inconnu")


# ================ les fonctions Tkinter


# Fonction de recherche et d'affichage de la météo
def rechercher():
    ville = nom_ville.get().strip()
    if not ville:
        messagebox.showerror("Erreur", "Veuillez entrer un nom de ville.")
        return
    
    coordonnees = get_coordonnees(ville)
    if not coordonnees:
        messagebox.showerror("Erreur", f"Impossible de trouver '{ville}'.")
        return
    
    meteo = get_meteo(coordonnees['latitude'], coordonnees['longitude'])
    if not meteo:
        messagebox.showerror("Erreur", "Impossible de récupérer la météo.")
        return
    
    actuel = meteo['current_weather']
    description = traduire_code_meteo(actuel['weathercode'])
    
    # Couleur selon la température
    if actuel['temperature'] < 10:
        fg = "blue"
    elif actuel['temperature'] <= 20:
        fg = "green"
    else:
        fg = "red"
    
    affichage.config(
        text=(
            f"📍 {coordonnees['nom']}, {coordonnees['pays']}\n"
            f"🕐 {actuel['time']}\n"
            f"🌡️ {actuel['temperature']}°C\n"
            f"☁️ {description}\n"
            f"💨 Vent : {actuel['windspeed']} km/h\n"
            f"🧭 Direction : {actuel['winddirection']}°"
        ),
        bg="lightblue",
        font=("Arial", 12),
        fg=fg
    )


def effacer():
    affichage.config(text="")
    nom_ville.delete(0, tk.END)


# ================ création de la fenêtre

fenetre = tk.Tk()
fenetre.title("Météo App")
fenetre.geometry("500x450")

# Widgets
tk.Label(fenetre, text="Entrez le nom de la ville :").pack(pady=10)
nom_ville = tk.Entry(fenetre, width=30)
nom_ville.pack()

tk.Button(fenetre, text="Rechercher", command=rechercher).pack(pady=10)
fenetre.bind("<Return>", lambda event: rechercher())

affichage = tk.Label(fenetre, text="", bg="lightblue", font=("Arial", 12))
affichage.pack(pady=20, fill="both", expand=True)
# fill="both" et expand=True permettent à l'affichage de prendre tout l'espace disponible

tk.Button(fenetre, text="Effacer", command=effacer).pack(pady=5)

fenetre.mainloop()