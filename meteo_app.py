# Les imports de tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Les imports de l'API
import urllib.request
import json


# ================ les fonctions API


# (ville → coordonnées)
def get_coordonnees(nom_ville):
    """Transforme un nom de ville en coordonnées GPS"""
    
    # On remplace les espaces par %20 pour l'URL
    ville_encodee = nom_ville.replace(" ", "%20")
    url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={ville_encodee}&count=1&format=json"
    try:
        reponse = urllib.request.urlopen(url_geo)
        donnees = reponse.read().decode('utf-8')  
        resultat = json.loads(donnees)
    except Exception as e:
        print("Erreur lors de la requête à l'API de géocodage :", e)
        return None
    
    

    """ 
    resultat est un dictionnaire Python qui ressemble à ça (pour la ville de Paris) :

    {'results': [{'id': 2988507, 'name': 'Paris', 'latitude': 48.85341, 'longitude': 2.3488, 
    'elevation': 42.0, 'feature_code': 'PPLC', 'country_code': 'FR', 'admin1_id': 3012874, 
    'admin2_id': 2968815, 'admin3_id': 2988506, 'admin4_id': 6455259, 'timezone': 'Europe/Paris',
      'population': 2138551, 'postcodes': ['75001', '75020', '75002', '75003', '75004', '75005', 
      '75006', '75007', '75008', '75009', '75010', '75011', '75012', '75013', '75014', '75015', 
      '75016', '75017', '75018', '75019'], 'country_id': 3017382, 'country': 'France', 
      'admin1': 'Île-de-France', 'admin2': 'Paris', 'admin3': 'Paris', 'admin4': 'Paris'}],
     'generationtime_ms': 0.6864071}
    """
    
    if resultat.get('results'):  
        infos_ville = resultat['results'][0]
        return {
            'nom': infos_ville['name'],
            'pays': infos_ville['country'],
            'latitude': infos_ville['latitude'],
            'longitude': infos_ville['longitude']
        }
    else:
        return None


# (coordonnees → meteo)
def get_meteo(latitude, longitude):
    url_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    try:
        reponse = urllib.request.urlopen(url_meteo)
        donnees = reponse.read().decode('utf-8')  
        return json.loads(donnees)
    except Exception as e:
        print("Erreur lors de la requête à l'API de météo :", e)
        return None
    

 

# ================= Les fonctions tkinter


# code meteo
codes_meteo = {
    0: "☀️ Ciel clair",
    1: "⛅ Nuageux", 
    2: "⛅ Nuageux",
    3: "☁️ Couvert",
    45: "🌫️ Brouillard",
    48 : "🌫️ Brouillard" ,
    51: "🌧️ Bruine",
    53 : "🌧️ Bruine",
    55 : "🌧️ Bruine",
    61: "🌧️ Pluie",
    63: "🌧️ Pluie",
    65: "🌧️ Pluie",
    71: "❄️ Neige",
    73: "❄️ Neige",
    75: "❄️ Neige",
    95: "⛈️ Orage",
    96: "⛈️ Orage",
    99: "⛈️ Orage"
 }

def rechercher():
    ville = nom_ville.get().strip()
    if not ville:
        messagebox.showerror("Erreur", "Veuillez entrer un nom de ville.")
        return
    
    # print(f"Recherche de {ville}")
    coordonnees = get_coordonnees(ville)
    if not coordonnees:
        messagebox.showerror("Erreur", f"Impossible de trouver les coordonnées de {ville}.")
        return
    """ 
    print("Coordonnées trouvées : ")
    print(f"Ville : {coordonnees['nom']}")
    print(f"Pays : {coordonnees['pays']}")
    print(f"Latitude : {coordonnees['latitude']}")
    print(f"Longitude : {coordonnees['longitude']}")
    print("\n")
    """

    if coordonnees:
        meteo = get_meteo(coordonnees['latitude'], coordonnees['longitude'])
        """ 
        print(f"Météo trouvé : ")
        print(f"Dernière mise à jour : {meteo['current_weather']['time']}")
        print(f"Temperature : {meteo['current_weather']['temperature']} °C")
        print(f"Vitesse du vent : {meteo['current_weather']['windspeed']} km/h")
        print(f"Direction du vent : {meteo['current_weather']['winddirection']} °")
        print("\n")
        """
        
        actuel = meteo['current_weather']
        # global  codes_meteo  : Pas necessaire car la lecture d'une variable globale est automatique, elle serait necessaire que si on réassignait la variable
        description = codes_meteo.get(actuel['weathercode'], "❓ Inconnu")
    
        if actuel['temperature'] < 10 : 
            fg = "blue"
        elif actuel['temperature'] <= 20 :
            fg = "green"
        else:
            fg = "red"

        
        affichage.config(
            text=(
                f"Ville : {coordonnees['nom']}, {coordonnees['pays']}\n"
                f"Dernière mise à jour : {actuel['time']}\n"
                f"🌡️ Température : {actuel['temperature']}°C\n"
                f"☁️ Conditions : {description}\n"
                f"💨 Vent : {actuel['windspeed']} km/h\n"
                f"🧭 Direction : {actuel['winddirection']}°"
            ),
            bg="lightblue",
            font=("Arial", 12),
            fg=fg
        )

        #print("Météo affiché")
                        
        

def effacer():
    affichage.config(text = "")
    nom_ville.delete(0, tk.END)






# ============================ La fenetre
fenetre = tk.Tk()
fenetre.title("Meteo App")
fenetre.geometry("500x400")

ville = tk.Label(fenetre, text = "Entrez le nom de la ville :")
ville.pack(pady = 10)
nom_ville = tk.Entry(fenetre )
nom_ville.pack()

bouton = tk.Button(fenetre, text = "Rechercher", command = rechercher)
bouton.pack(pady=10)
fenetre.bind("<Return>", lambda event: rechercher())    


affichage = tk.Label(fenetre, text = "")
affichage.pack()


# effacer = tk.Button(fenetre, text = "Effacer", command = lambda: affichage.config(text = "") )
effacer = tk.Button(fenetre, text = "Effacer", command = effacer)
effacer.pack()




fenetre.mainloop()