import os
import sys

from Extraires_Images.pdf_to_docx_to_pdf import pdf_to_docx_to_pdf
from Extraires_Images.extract_images_from_pdf import extract_images_from_pdf
from IA.Load_IA.Load_IA import Load_IA
from IA.Prediction_IA.Prediction_IA import Prediction_IA
pdf_directory = "PLU"
All_Images_Directory = "IMAGES"

def extract_images():
    # Parcourir tous les fichiers et répertoires dans le répertoire donné
    for root, dirs, files in os.walk(pdf_directory):
        for file in files:
            if file.lower().endswith(".pdf"):  # Vérifier si le fichier est un PDF
                pdf_path = os.path.join(root, file)  # Chemin complet du fichier PDF
                pdf_to_docx_to_pdf(pdf_path)  # Convertir le fichier en PDF puis en word puis en PDF pour éviter les problèmes d'extrations d'images
                extract_images_from_pdf(pdf_path, All_Images_Directory)


def trier_images():
    model = Load_IA()
    # Répertoire contenant les images de test
    images_dir = "IMAGES"
    # Créer les répertoires Carte et PasCarte s'ils n'existent pas
    carte_dir = "CARTE"
    if not os.path.exists(carte_dir):
        os.makedirs(carte_dir)
    pas_carte_dir = "PAS_CARTE"
    if not os.path.exists(pas_carte_dir):
        os.makedirs(pas_carte_dir)

    # Lister tous les fichiers .png dans le répertoire ImagesDeTest
    list_image_path = [os.path.join(images_dir, file) for file in os.listdir(images_dir) if file.endswith(".png")]

    for image_path in list_image_path:
        # Effectuer la prédiction sur chaque image
        prediction_value = Prediction_IA(model, image_path)
        # Déplacer l'image vers le répertoire CARTE ou PAS_CARTE en fonction de la prédiction
        if prediction_value >= 0.5:
            output_path = os.path.join(carte_dir, os.path.basename(image_path))
            os.rename(image_path, output_path)
            print(f"{image_path} déplacé vers {carte_dir}.")
        else:
            # PasCarte
            output_path = os.path.join(pas_carte_dir, os.path.basename(image_path))
            os.rename(image_path, output_path)
    
if __name__ == "__main__":
    extract_images()
    trier_images()
