import os
import PyPDF2

from pdf2docx import Converter
from docx2pdf import convert

# Convertir le PDF en document Word
def pdf_to_docx(pdf_path, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

# Convertir le document Word en PDF
def docx_to_pdf(docx_path, pdf_path):
    convert(docx_path, pdf_path)

# Supprimer le fichier Word
def delete_file(file_path):
    os.remove(file_path)

# Supprimer l'ancien PDF et renommer le nouveau PDF
def replace_pdf(old_pdf_path, new_pdf_path):
    os.remove(old_pdf_path)
    os.rename(new_pdf_path, old_pdf_path)

def pdf_to_docx_to_pdf(pdf_file):
    docx_file = "buffer.docx"
    new_pdf_file = pdf_file
    # Conversion du PDF en document Word
    pdf_to_docx(pdf_file, docx_file)

    # Conversion du document Word en PDF
    docx_to_pdf(docx_file, new_pdf_file)

    # Suppression du fichier Word
    delete_file(docx_file)

#pdf_to_docx_to_pdf("PLU/44093_PADD_20140121.pdf")

#pdf_to_docx_to_pdf("44003_info_surf_19_03_20140922-50-100.pdf")
