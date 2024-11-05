import requests
import os
import time
import threading
import zipfile
#
def get_document_list():
    url = "https://www.geoportail-urbanisme.gouv.fr/api/document?originalName=anciennes&status=document.production"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        headers = response.headers
        print_headers(headers)
        # Traitement des données de la liste des documents
        for document in data:
            print(f"ID: {document['id']}, Titre: {document['titre']}")
    else:
        print(f"Erreur {response.status_code}: {response.text}")

def print_headers(headers):
    for key,value in headers.items():
        print(f"{key}: {value}")

#Retourne une list avec les métadonnées de tout les documents
def get_all_documents():
    url = "https://www.geoportail-urbanisme.gouv.fr/api/document"
    response = requests.get(url)
    list_of_all_documents = []
    if response.status_code == 200:
        documents = response.json()
        for document in documents:
            list_of_all_documents.append(document)
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return list_of_all_documents

#Retourne une list avec tout les PLU
def get_all_documents_PLU():
    url = "https://www.geoportail-urbanisme.gouv.fr/api/document"
    response = requests.get(url)
    list_of_all_documents = []
    if response.status_code == 200:
        documents = response.json()
        for document in documents:
            if document['type'] == 'PLU':
                list_of_all_documents.append(document)
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return list_of_all_documents

#Affiche les données d'un document
def print_document(document):
    print('-'*50)
    for key,value in document.items():
        print(f"{key}: {value}")

#Affiche les données des document d'une liste de document
def print_list_of_all_documents(list_of_all_documents):
    for document in list_of_all_documents:
        print_document(document)


#Code qui créait le fichier de sauvegarde et télécharge
def download_and_save_with_progress(document_id, document_name, index=0):
    url = f"https://www.geoportail-urbanisme.gouv.fr/api/document/{document_id}/download/{document_name}.zip"
    #print(url)
    time_start = time.time()
    chunk_size = 8192
    download_directory = r"PLU_ZIP"
    try:
        print(f"Thread {index} starts")        
        with requests.get(url, stream=True) as response:
            base_filename = os.path.basename(url)
            filename = os.path.join(download_directory, base_filename)
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)

        time_end = time.time()
    
        print(f"Thread {index} starts, file downloaded")    
        # Une fois le téléchargement terminé, dézippez le fichier
        extract_to_directory = r"H:/Documents/ING2/Semestre 2/Projet/Projet GSI V2/Extraire Images de PDFs/PLU"
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to_directory)
        
        # Supprimer le fichier zip après extraction
        os.remove(filename)
        print(f"Thread {index} finished in {time_end - time_start}\n")
        
    except Exception as e:
        print(f"Thread {index} encountered an error: {e}")

def download_all_documents(list_of_all_documents):
    threads = []
    for index, document in enumerate(list_of_all_documents):
        document_id = document['id']
        document_name = document['name']
        thread = threading.Thread(target=download_and_save_with_progress, args=(document_id, document_name, index))
        threads.append(thread)
        thread.start()


    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()
        
#Afficher la liste des documents
#list_of_all_documents = get_all_documents()
#print_list_of_all_documents(list_of_all_documents)
#download_all_documents(list_of_all_documents)

#Sauvegarder un document
#download_and_save_with_progress(document_id, document_name)



