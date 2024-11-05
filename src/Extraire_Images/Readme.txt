
-main télécharge les PLU, les dézip, corrige les pdfs et extrait les images.
-Les opérations de conversions sont couteuses et prennent du temps
-Pour tester, il peut être judicieux de ne faire qu'avec un pdf.


-extract_images_from_pdf extrait toutes les images d'un pdf
-get_plu permet de télécharger et de décompresser les derniers PLU à partir de l'API
-pdf_to_docx_to_pdf convertie les pdf en docx puis en pdf afin de régler les problèmes d'extractions d'images, en effet certaines images sont coupées si elle sont extraites depuis le pdf directement téléchargé de l'API
