import tensorflow.keras as keras
from keras.models import load_model
import numpy as np
import os
from PIL import Image
import sys


# Obtenir le chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Ajouter le chemin du répertoire parent au chemin de recherche des modules
sys.path.append(parent_dir)
from Load_IA import Load_IA
def get_resized_image_array(image_path):
    image = Image.open(image_path).convert('RGB')  # Convertir l'image en RGB
    resized_image = image.resize((100, 100))
    resized_image_array = np.array(resized_image)
    resized_image_array = resized_image_array.reshape(1, 100, 100, 3)  # Pour une image RGB
    resized_image_array = resized_image_array / 255.0
    return resized_image_array

def prediction(model, image_path):
    resized_image_array = get_resized_image_array(image_path)
    # Obtenir la prédiction du modèle sur l'image de test
    prediction = model.predict(resized_image_array)
    return prediction[0][0]  # Renvoie la valeur de prédiction
def main():

    traind_model = Load_IA.Load_IA()
    
    # Répertoire contenant les images de test
    images_dir = "ImagesDeTest"
    # Créer les répertoires Carte et PasCarte s'ils n'existent pas
    carte_dir = "Carte"
    if not os.path.exists(carte_dir):
        os.makedirs(carte_dir)
    pas_carte_dir = "PasCarte"
    if not os.path.exists(pas_carte_dir):
        os.makedirs(pas_carte_dir)

    # Lister tous les fichiers .png dans le répertoire ImagesDeTest
    list_image_path = [os.path.join(images_dir, file) for file in os.listdir(images_dir) if file.endswith(".png")]

    for image_path in list_image_path:
        # Effectuer la prédiction sur chaque image
        prediction_value = prediction(traind_model, image_path)
        
        # Déplacer l'image vers le répertoire Carte ou PasCarte en fonction de la prédiction
        if prediction_value >= 0.5:
            # Carte
            output_path = os.path.join(carte_dir, os.path.basename(image_path))
            os.rename(image_path, output_path)
            print(f"{image_path} déplacé vers {carte_dir}.")
        else:
            # PasCarte
            output_path = os.path.join(pas_carte_dir, os.path.basename(image_path))
            os.rename(image_path, output_path)
if __name__ == "__main__":
    main()
