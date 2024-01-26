# {'u4' : {'301' : {'temperature' : ['nom1', 'nom2'], 
#                    'co2' : ['nom1', 'nom2', '...'],
#                    'humudity' : ['nom1', 'nom2', '...'],
#                    'luminosity' : ['nom1', 'nom2', '...'],
#                    'energy' : ['nom1', 'nom2', '...']},
#          '302' : {'temperature' : ['nom1', 'nom2', '...'], 
#                    'co2' : ['nom1', 'nom2', '...'],
#                    'humudity' : ['nom1', 'nom2', '...'],
#                    'luminosity' : ['nom1', 'nom2', '...'],
#                    'energy' : ['nom1', 'nom2', '...']}, 
#          '303' : {'temperature' : ['nom1', 'nom2', '...'], 
#                    'co2' : ['nom1', 'nom2', '...'],
#                    'humudity' : ['nom1', 'nom2', '...'],
#                    'luminosity' : ['nom1', 'nom2', '...'],
#                    'energy' : ['nom1', 'nom2', '...']}}}

listTypeCapteur = []
lCapteurs = {}

#exists
def capteurExists(batiment, salle, typeCapteur, name, liste):
    if not(batiment in liste):
        liste[batiment] = {}

    if not(salle in liste[batiment]):
        liste[batiment][salle] = {}

    if not(typeCapteur in liste[batiment][salle]):
        liste[batiment][salle][typeCapteur] = []
        listTypeCapteur.append(typeCapteur)

    return name in liste[batiment][salle][typeCapteur]

#add

def addCapteur(batiment, salle, typeCapteur, name, liste):
    if not(capteurExists(batiment, salle, typeCapteur, name, liste)):
        liste[batiment][salle][typeCapteur].append(name)