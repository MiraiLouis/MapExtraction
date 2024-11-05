import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures
import threading
thread_numbers = {} #Dictionnaire pour donner un nom unique pour toutes les images
#Récupère les urls des images depuis une recherche
def fetch_image_links(search_url, headers):
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    image_links = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("https://"):
            image_links.append(src)
    return image_links

# Récupère les urls des images par bloc de 20 et lance un thread pour chaque bloc
def get_image_urls(keyword, num_images=10):
    search_urls = [f"https://www.google.com/search?q={keyword}&tbm=isch&start={i * 20}" for i in range(num_images // 20 + 1)]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    image_links = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_image_links, url, headers) for url in search_urls]
        for future in concurrent.futures.as_completed(futures):
            image_links.extend(future.result())

    return image_links[:num_images]

#Télécharge toutes les images depuis une liste de liens des images
def download_and_save_batch(image_links_batch, download_directory, thread_id):
    
    for index, url in enumerate(image_links_batch):
        # Incrémenter le nombre de téléchargements pour ce thread
        if thread_numbers.get(thread_id, 0) == 20:
            thread_numbers[thread_id] = 0
        else:
            thread_numbers[thread_id] = thread_numbers.get(thread_id, 0) + 1
        thread_number = thread_numbers[thread_id]
        try:
            response = requests.get(url)
            response.raise_for_status()  # Vérifie si la requête a réussi
            
            # Obtention du nom du fichier à partir de l'URL
            filename = os.path.basename(url)
            # Ajout de l'ID du thread au nom du fichier
            filename_with_thread_id = f"image_{thread_id}_{thread_number}_{index}.png"
            save_path = os.path.join(download_directory, filename_with_thread_id)

            # Écriture du contenu dans le fichier
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Image {index} téléchargée par le thread {thread_id}.")
        except Exception as e:
            print(f"Erreur lors du téléchargement de {url} : {e}")

if __name__ == "__main__":
    keyword = "insee graph"
    num_images = 100
    global DOWNLOAD_DIRECTORY
    DOWNLOAD_DIRECTORY = "FalseData"

    # Récupérer les liens des images
    image_links = get_image_urls(keyword, num_images)

    # Diviser les liens en blocs de 20 pour la distribution entre les threads
    image_links_batches = [image_links[i:i+20] for i in range(0, len(image_links), 20)]

    # Télécharger les images en parallèle
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for thread_id, image_links_batch in enumerate(image_links_batches):
            executor.submit(download_and_save_batch, image_links_batch, DOWNLOAD_DIRECTORY, thread_id)
