
# Les imports de tkinter
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

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
    
    # Démarrer la barre de progression
    progress_bar.pack(pady=10)
    progress_bar.start()
    fenetre.update()  # Force la mise à jour de la fenêtre pour afficher la barre avant de faire les requêtes API
    
    coordonnees = get_coordonnees(ville)
    if not coordonnees:
        # Arrêter et cacher la barre de progression
        progress_bar.stop()
        progress_bar.pack_forget()   

        messagebox.showerror("Erreur", f"Impossible de trouver '{ville}'.")
        return
    
    meteo = get_meteo(coordonnees['latitude'], coordonnees['longitude'])
    if not meteo:
        progress_bar.stop()
        progress_bar.pack_forget()
        messagebox.showerror("Erreur", "Impossible de récupérer la météo.")
        return
    
    
    progress_bar.stop()
    progress_bar.pack_forget()
    
    actuel = meteo['current_weather']
    description = traduire_code_meteo(actuel['weathercode'])
    
    # Couleur selon la température
    if actuel['temperature'] < 10:
        couleur_texte = "blue"
    elif actuel['temperature'] <= 20:
        couleur_texte = "green"
    else:
        couleur_texte = "red"
    
    # Afficher le résultat (dans un CTkFrame avec fond)
    frame_resultat.configure(fg_color="lightblue")
    affichage.configure(
        text=(
            f"📍 {coordonnees['nom']}, {coordonnees['pays']}\n"
            f"🕐 {actuel['time']}\n"
            f"🌡️ {actuel['temperature']}°C\n"
            f"☁️ {description}\n"
            f"💨 Vent : {actuel['windspeed']} km/h\n"
            f"🧭 Direction : {actuel['winddirection']}°"
        ),
        text_color=couleur_texte
    )
    # Réafficher le frame résultat
    frame_resultat.pack(pady=10, fill="both", expand=True)


def effacer():
    affichage.configure(text="")
    frame_resultat.pack_forget()  # Cache le cadre de résultat
    nom_ville.delete(0, tk.END)


def changer_theme():
    current_mode = ctk.get_appearance_mode()  # Récupère le mode actuel ("Light", "Dark" )
    new_mode = "Dark" if current_mode == "Light"  else "Light"
    ctk.set_appearance_mode(new_mode)




# ================ création de la fenêtre

ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue") 

fenetre = ctk.CTk()
fenetre.title("🌤️ Météo App")
fenetre.geometry("500x600")
# fenetre.resizable(False, False)  # Empêche le redimensionnement de la fenêtre


# Frame principal :
# Creation d'un cadre principal pour mieux organiser les widgets et permettre un meilleur affichage
frame_principal = ctk.CTkFrame(fenetre)
frame_principal.pack(padx=20, pady=20, fill="both", expand=True)
# fill="both" et expand=True permettent à l'affichage de prendre tout l'espace disponible dans le frame,
#  même si la fenêtre est redimensionnée (ici on a mis resizable à False, mais c'est une bonne pratique pour les futurs projets).


# Bouton thème (en haut à droite)
btn_theme = ctk.CTkButton(
    frame_principal,
    text="🌓 Changer de thème",
    width=150,
    height=40,
    fg_color="#963A3A",
    command=changer_theme
)

btn_theme.pack(pady=5, anchor="ne")
# anchor="ne"  permet d'ancrer le bouton au nord-est du frame, c'est-à-dire en haut à droite du frame.
# Les autres option d'ancrage sont : "n" (nord), "e" (est), "s" (sud), "w" (ouest), "nw" (nord-ouest), "se" (sud-est) et "sw" (sud-ouest).


# Titre
ctk.CTkLabel(
    frame_principal,
    text="🌤️ Météo App",
    font=ctk.CTkFont(size=24, weight="bold"),
    text_color="#2E86C1"
).pack(pady=10)


# Label instruction
ctk.CTkLabel(
    frame_principal,
    text="Entrez le nom de la ville :",
    font=ctk.CTkFont(size=14, weight="bold")
).pack(pady=10)

# Champ de saisie
nom_ville = ctk.CTkEntry(
    frame_principal,
    width=300,
    height=40,
    font=ctk.CTkFont(size=12),
    placeholder_text="Ex : Abidjan, Paris, New York..."
)
nom_ville.pack()

# Bouton recherche
ctk.CTkButton(
    frame_principal,
    text="Rechercher",
    width=100,
    height=40,
    command=rechercher
).pack(pady=10)


# Barre de progression (cachée au départ)
progress_bar = ctk.CTkProgressBar(
    frame_principal,
    # length=400,
    mode="indeterminate"   
)
# Ne pas la pack() ici, elle sera affichée uniquement pendant la recherche


# Cadre pour le résultat (caché au départ)
frame_resultat = ctk.CTkFrame(frame_principal, corner_radius=10)  # corner_radius=10 pour arrondir les coins du cadre
# Ne pas le pack() ici, il sera affiché uniquement quand il y a un résultat


# Label d'affichage (à l'intérieur du cadre résultat)
affichage = ctk.CTkLabel(
    frame_resultat,
    text="",
    font=ctk.CTkFont(size=12)
)
affichage.pack(padx=20, pady=20)

# Bouton effacer
ctk.CTkButton(
    frame_principal,
    text="Effacer",
    fg_color="gray",
    width=80,
    height=40,
    command=effacer
).pack(pady=5)

# Raccourci clavier
fenetre.bind("<Return>", lambda event: rechercher())


fenetre.mainloop()



