import os
from pdf_to_docx_to_pdf import pdf_to_docx_to_pdf
from extract_images_from_pdf import extract_images_from_pdf
from get_plu import get_all_documents
from get_plu import download_all_documents
def process_pdf_files(directory):
    list_of_all_documents = get_all_documents()
    download_all_documents(list_of_all_documents)
    # Parcourir tous les fichiers et répertoires dans le répertoire donné
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".pdf"):  # Vérifier si le fichier est un PDF
                pdf_path = os.path.join(root, file)  # Chemin complet du fichier PDF
                pdf_to_docx_to_pdf(pdf_path)  # Convertir le fichier en PDF puis en word puis en PDF pour éviter les problèmes d'extrations d'images
                extract_images_from_pdf(pdf_path, output_directory)
# Exemple d'utilisation
pdf_directory = "PLU"
output_directory = "IMAGES"
process_pdf_files(pdf_directory)
