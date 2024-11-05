from qgis.core import QgsRectangle, QgsPointXY, QgsMapSettings, QgsProject, QgsMapRendererParallelJob
from PyQt5.QtCore import QSize
from qgis.core import QgsVectorLayerSimpleLabeling, QgsPalLayerSettings
import random
from PyQt5.QtGui import QColor
import time
# Charger le projet QGIS
project = QgsProject.instance()
project.read("Test Donnes en vracV2.qgz")
#project.read()


# Définir le chemin de sauvegarde pour les captures d'écran
dossier_sauvegarde = "H:/Documents/ING2/Semestre 2/Projet/Projet GSI V2/Création DATA/True Data Creation/TrueData/"

# Obtenir toutes les couches du projet une seule fois
layers = QgsProject.instance().mapLayers().values()
test_layers = {}
#Layer 0 to not get it at the begining
for layer in layers:
    layer0 = layer
    break
buffer_layers = {}
for layer in layers:
    print(f"Layer Name:", layer.name())
    if layer != layer0:
        buffer_layers[layer.name()] = layer
        
buffer_layers[layer0.name()] = layer0
layers = buffer_layers.values()

def create_map(emplacement, layers):
    # Définir le rectangle d'extent pour la carte
    rectangle = QgsRectangle(QgsPointXY(emplacement[0][0], emplacement[0][1]),
                             QgsPointXY(emplacement[1][0], emplacement[1][1]))
    print("rectangle:",rectangle)
    # Définir les paramètres de la carte
    mapSettings = QgsMapSettings()
    mapSettings.setExtent(rectangle)
    mapSettings.setOutputSize(QSize(800, 600))  # Définir la taille de l'image de sortie


    # Définir les couches pour la carte
    mapSettings.setLayers(layers)
    #print("layers", layers)
    # Définir le système de coordonnées de destination
    mapSettings.setDestinationCrs(project.crs())

    # Créer la carte avec les paramètres définis
    render = QgsMapRendererParallelJob(mapSettings)
    render.start()
    render.waitForFinished()

    # Sauvegarder l'image de la carte
    image = render.renderedImage()
    image.save(f"{dossier_sauvegarde}carte_{emplacement[0][0]}_{emplacement[0][1]}_{emplacement[1][0]}_{emplacement[1][1]}.png", "png")

    print("Image de carte générée avec succès !")
#Here Wego Terrain 110
#Google Hybrid 110
#Google Labels 110
#Google Roads 30
#Google Satellite 50
#Google Terrain 110
#Positron 300
#Bing Map 10
#OpenStreetMap 120
#Google Hybrid / Google Traffic 120
#Google Terrain 100
#Here Wego Satellite 220
#Positron 200
#Here Wego Hybrid 330
#ESRI Standard 200
# Liste pour stocker les emplacements

def get_emplacement():
    xMax = random.randint(-8800, 660000)
    yMax = random.randint(5400000, 6300000)
    list_echelle = [400000, 100000, 42000, 22000]
    echelle = list_echelle[random.randint(0,len(list_echelle)-1)]
    xMin, yMin = xMax - echelle/6, yMax - echelle/6
    return [(xMin,yMin),(xMax,yMax)]


emplacements = [get_emplacement() for i in range(0,10)]

for emplacement in emplacements:
    create_map(emplacement, layers)