
# Les imports de tkinter
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image  # Pour l'affichage d'images 
# pip install Pillow

# Les imports de l'API
import urllib.request
import json

# ================ Les ameliorations : 

""" 
💾 AMÉLIORATION 3 : Sauvegarde de la dernière ville
Objectif
Quand l'utilisateur ferme et rouvre l'application, la dernière ville recherchée est automatiquement rechargée.

Concepts à comprendre
json.dump() : sauvegarder des données

json.load() : charger des données

try/except : gérer l'absence du fichier

Tâches à réaliser
Tâche 1 : Créer une fonction sauvegarder_derniere_ville(ville)
Ouvre un fichier derniere_ville.json

Écrit la ville à l'intérieur

Utilise json.dump()

Tâche 2 : Appeler cette fonction après une recherche réussie
Dans rechercher(), après avoir trouvé la météo

Sauvegarde ville (le nom tapé)

Tâche 3 : Créer une fonction charger_derniere_ville()
Essaie d'ouvrir derniere_ville.json

Si le fichier existe, retourne la ville

Sinon, retourne None

Tâche 4 : Au démarrage de l'application
Appelle charger_derniere_ville()

Si une ville existe :

La mettre dans l'Entry

Appeler automatiquement rechercher() pour afficher la météo

Tâche 5 : Gérer l'absence de fichier
Si le fichier n'existe pas (premier lancement), ne rien faire

Format du fichier JSON
json
{
    "derniere_ville": "Paris"
}
✅ Vérification
Après avoir recherché "Tokyo", ferme et rouvre l'app → Tokyo apparaît

La météo se charge automatiquement au démarrage

Si aucune ville sauvegardée, l'app est vide (pas d'erreur)

"""


""" Amélioration 4 :  Bouton "Ma position"
Objectif
L'utilisateur peut cliquer sur un bouton pour obtenir la météo à sa position actuelle (via géolocalisation IP).

Concepts à comprendre
API de géolocalisation par IP (gratuite, sans clé)

Une API retourne la ville approximative à partir de l'adresse IP

API à utiliser
text
https://ipapi.co/json/
Cette API retourne (entre autres) :

city : la ville
country_name : le pays
latitude et longitude

Tâches à réaliser
Tâche 1 : Créer une fonction get_position_actuelle()
Appelle l'API https://ipapi.co/json/

Extrait la city du JSON

Retourne le nom de la ville

Tâche 2 : Créer un bouton "📍 Ma position"
Dans frame_principal, ajouter un bouton à côté du champ de saisie

Texte : "📍 Ma position" ou "📍 Me localiser"

Tâche 3 : Créer la fonction me_localiser()
Appelle get_position_actuelle()

Met la ville trouvée dans nom_ville

Appelle rechercher()

Tâche 4 : Gérer les erreurs
Si l'API ne répond pas → message d'erreur

Si la ville n'est pas trouvée → message approprié

⚠️ Difficulté
L'API par IP donne une approximation (pas la position exacte). Pour une ville à 5km près, c'est suffisant.

✅ Vérification
Le bouton "Ma position" existe

En cliquant, la météo de ta ville approximative s'affiche

Le champ de saisie se remplit automatiquement

"""






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


def get_emoji_meteo(code):
    emojis = {
        0: "image_lumiere_soleil", 1: "image_nuage", 2: "image_nuage", 
        3: "image_couvert",
        45: "image_brouillard", 48: "image_brouillard",
        51: "image_bruine", 53: "image_bruine", 55: "image_bruine",
        61: "image_pluie", 63: "image_pluie", 65: "image_pluie",
        71: "image_neige", 73: "image_neige", 75: "image_neige",
        95: "image_orage", 96: "image_orage", 99: "image_orage"
    }
    return emojis.get(code, "❓")





def get_position_actuelle():
    """Utilise une API pour obtenir la position actuelle de l'utilisateur (ville)"""
    
    # Première tentative : ipinfo.io
    try:
        reponse = urllib.request.urlopen("https://ipinfo.io/json")
        donnees = reponse.read().decode('utf-8')
        info = json.loads(donnees)
        ville = info.get('city')
        if ville:
            return ville
    except Exception as e:
        print("Erreur ipinfo.io :", e)
    
    # Deuxième tentative : ipapi.co (alternative gratuite)
    try:
        reponse = urllib.request.urlopen("https://ipapi.co/json/")
        donnees = reponse.read().decode('utf-8')
        info = json.loads(donnees)
        ville = info.get('city')
        if ville:
            return ville
    except Exception as e:
        print("Erreur ipapi.co :", e)
    
    return None  # Si les deux APIs échouent



def me_localiser():
    ville = get_position_actuelle()
    if ville:
        nom_ville.delete(0, tk.END)  # Efface le champ de saisie
        nom_ville.insert(0, ville)  # Met la ville trouvée dans le champ de saisie
        rechercher()  
    else:
        messagebox.showerror("Erreur", "Impossible de récupérer votre position actuelle.")




# ================ les fonctions Tkinter


# Fonction de recherche et d'affichage de la météo
def rechercher():
    ville = nom_ville.get().strip()
    if not ville:
        messagebox.showerror("Erreur", "Veuillez entrer un nom de ville.")
        return
    
    # Sauvegarde la ville recherchée dans un fichier JSON
    sauvegarder_derniere_ville(ville)  
    
    
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
    code_meteo = actuel['weathercode']
    image_a_afficher = dict_images_meteo.get(code_meteo, image_nuage)  # image_nuage par défaut
    
    # Mise à jour du label d'image
    label_image_meteo.configure(image=image_a_afficher, text="")
   


    description = traduire_code_meteo(actuel['weathercode'])
    # description = get_emoji_meteo(actuel['weathercode']) + " " + traduire_code_meteo(actuel['weathercode'])
    
    # Couleur selon la température
    if actuel['temperature'] < 10:
        couleur_texte = "blue"
    elif actuel['temperature'] <= 20:
        couleur_texte = "green"
    else:
        couleur_texte = "red"
    
    # Afficher le résultat (dans un CTkFrame avec fond)
    frame_resultat.configure(fg_color="lightblue")

    label_temperature.configure(
        text=f"{actuel['temperature']}°C",
        text_color=couleur_texte
    )
    label_details.configure(    
        text=(
            f"📍 {coordonnees['nom']}, {coordonnees['pays']}"
            f"\n🕐 {actuel['time']}\n"
            f"{description}\n"
            f"💨 Vent : {actuel['windspeed']} km/h\n"
            f"🧭 Direction : {actuel['winddirection']}°"
        )
    )


    # Réafficher le frame résultat
    frame_resultat.pack(pady=10, fill="both", expand=True)


def effacer():
    label_temperature.configure(text="")
    label_details.configure(text="")
    frame_resultat.pack_forget()  # Cache le cadre de résultat
    nom_ville.delete(0, tk.END)


def changer_theme():
    current_mode = ctk.get_appearance_mode()  # Récupère le mode actuel ("Light", "Dark" )
    new_mode = "Dark" if current_mode == "Light"  else "Light"
    ctk.set_appearance_mode(new_mode)



# sauvergarde de la dernière ville recherchée dans un fichier JSON
def sauvegarder_derniere_ville(ville):
    with open("derniere_ville.json", "w") as f:
        json.dump({"derniere_ville": ville}, f)

# chargement de la dernière ville recherchée au démarrage de l'application
def charger_derniere_ville():
    try:
        with open("derniere_ville.json", "r") as f:
            data = json.load(f)
            return data.get("derniere_ville")
    except FileNotFoundError:
        return None






# ============ Chargements des images pour les icônes météo au démarrage de l'application


# chargement des images pour les icônes météo
image_soleil = ctk.CTkImage(Image.open("assets/img_meteo_app/soleil.png"), size=(64, 64))
image_nuage = ctk.CTkImage(Image.open("assets/img_meteo_app/nuageuse.png"), size=(64, 64))
image_pluie = ctk.CTkImage(Image.open("assets/img_meteo_app/averse.png"), size=(64, 64))
image_neige = ctk.CTkImage(Image.open("assets/img_meteo_app/neige.png"), size=(64, 64))
image_orage = ctk.CTkImage(Image.open("assets/img_meteo_app/tonnerre.png"), size=(64, 64)) 
image_brouillard = ctk.CTkImage(Image.open("assets/img_meteo_app/vent.png"), size=(64, 64)) 
image_couvert = ctk.CTkImage(Image.open("assets/img_meteo_app/couvert.png"), size=(64, 64))
image_bruine = ctk.CTkImage(Image.open("assets/img_meteo_app/bruine.png"), size=(64, 64))
image_lumiere_soleil = ctk.CTkImage(Image.open("assets/img_meteo_app/lumiere_soleil.png"), size=(64, 64))


# dictionnaire pour stocker les images et les associer aux codes météo
dict_images_meteo = {
    0: image_lumiere_soleil,
    1: image_nuage,
    2: image_nuage,
    3: image_couvert,
    45: image_brouillard,
    48: image_brouillard,
    51: image_bruine,
    53: image_bruine,
    55: image_bruine,
    61: image_pluie,
    63: image_pluie,
    65: image_pluie,
    71: image_neige,
    73: image_neige,
    75: image_neige,
    95: image_orage,
    96: image_orage,
    99: image_orage
}





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



# Frame horizontal pour champ + bouton
frame_recherche = ctk.CTkFrame(frame_principal, fg_color="transparent")
frame_recherche.pack(pady=10)  # fill="x" pour que le frame prenne toute la largeur disponible


# champs de saisie du nom de la ville
nom_ville =  ctk.CTkEntry(
    frame_recherche,
    width=300,
    height=40,
    font=ctk.CTkFont(size=12),
    placeholder_text="Ex : Abidjan, Paris, New York..."
)
nom_ville.pack(side="left", padx=(0, 10))


# Bouton "Ma position"
btn_position = ctk.CTkButton(
    frame_recherche,
    text= "📍 Me localiser",
    width=100,
    height=40,
    fg_color="#28B463",  
    command=lambda: me_localiser()
)
btn_position.pack(side="left")


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

# Sous-cadre pour la partie haute (température + image)
frame_haut = ctk.CTkFrame(frame_resultat, fg_color="transparent")
frame_haut.pack(pady=(20, 10))



# Label d'affichage (à l'intérieur du cadre résultat)

label_temperature = ctk.CTkLabel(
    frame_haut,
    text="",
    font=ctk.CTkFont(size=48, weight="bold") )
# label_temperature.pack(pady=(20, 10))  # Plus d'espace en haut que en bas

label_details = ctk.CTkLabel(
    frame_resultat, 
    text="",
    font=ctk.CTkFont(size=14) )
# label_details.pack(pady=(0, 20))  # Plus d'espace en bas que en haut


label_image_meteo = ctk.CTkLabel(frame_haut, image= None, text="")
# label_image_meteo.pack(pady=(0, 10))  # Plus d'espace en bas que en haut


# Organisation verticale du cadre résultat
# Ligne du haut : image + température côte à côte

label_image_meteo.pack(in_=frame_haut, side="left", padx=10)
label_temperature.pack(in_=frame_haut, side="left", padx=10)

# Détails en dessous
label_details.pack(pady=(0, 20))




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





# Charge la dernière ville recherchée au démarrage de l'application
derniere_ville = charger_derniere_ville()  
if derniere_ville:
    nom_ville.insert(0, derniere_ville)  # Met la ville dans l'Entry
    rechercher()  # Appelle automatiquement la fonction de recherche pour afficher la météo




fenetre.mainloop()



