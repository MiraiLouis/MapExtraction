import fitz #installer pymupdf si Directory 'static/' does not exist
import os
import numpy as np


def extract_images_from_pdf(pdf_path, output_directory):
    # Ouvrir le fichier PDF
    pdf_document = fitz.open(pdf_path)

    # Créer le répertoire de sortie s'il n'existe pas déjà
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Parcourir chaque page du PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        # Parcourir chaque image sur la page
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Récupérer le mode de couleur de l'image
            color_space = base_image["colorspace"]
            if color_space == 1:  # espace colorimétrique en niveaux de gris
                mode = "L"
            elif color_space == 3:  # espace colorimétrique en RGB
                mode = "RGB"
            else:
                mode = "RGB"  # Par défaut, conserver l'alpha channel si présent


            # Enregistrer l'image au format PNG avec le mode de couleur d'origine
            image_path = os.path.join(output_directory, f"page_{page_number + 1}_image_{img_index + 1}.png")
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

    # Fermer le document PDF
    pdf_document.close()
#extract_images_from_pdf("44003_info_surf_19_03_20140922-50-100.pdf","IMAGES")
