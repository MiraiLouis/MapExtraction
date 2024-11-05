import tensorflow as tf
import numpy as np
import random
import os
from PIL import Image

# Fixer la seed pour la reproductibilité
random.seed(42)
print("Begining the creation of Data")

def get_resized_image_array(image_path):
    image = Image.open(image_path).convert('RGB')  # Convertir l'image en RGB
    image_array = np.array(image)
    resized_image = image.resize((100, 100))
    resized_image_array = np.array(resized_image)
    resized_image_array = resized_image_array.reshape(1, 100, 100, 3)  # Pour une image RGB
    resized_image_array = resized_image_array / 255.0
    return resized_image_array

def process_image(image_path):
    return get_resized_image_array(image_path)

def create_data(image_paths):
    image_path = image_paths.pop(0)
    resized_image_array = get_resized_image_array(image_path)
    resized_images_array = np.array(resized_image_array)
    for image_path in image_paths:
        resized_image_array = get_resized_image_array(image_path)
        resized_images_array = np.append(resized_images_array, resized_image_array, axis=0)
    return resized_images_array
    
#-----------------------------------------------------------------------#
# False Data
print("Starting the creation of False Data")
directory = "False Data Creation/FalseData"

image_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(".png")]

false_data = create_data(image_paths)

print("Creation of False Data finished")
#-----------------------------------------------------------------------#
# True Data
print("Starting the creation of True Data")
directory = "True Data Creation/TrueData"

image_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(".png")]

true_data = create_data(image_paths)

print("Creation True Data finished")
print("Map Data Ready")
#-----------------------------------------------------------------------#

##Create Data (x_train, y_train, x_test, y_test)

# Concaténer les données
x = np.append(true_data, false_data, axis=0)

# Créer les étiquettes
y = np.array([1] * len(true_data) + [0] * len(false_data))

# Taille de l'ensemble de données
size_x = len(x)

# Fonction pour ajouter et supprimer des éléments
def append_and_pop(random_index, x_train, y_train, x, y):
    x_test_value = x[random_index]
    x = np.delete(x, random_index, axis=0)
    
    y_test_value = y[random_index]
    y = np.delete(y, random_index)
    
    x_train = np.append(x_train, [x_test_value], axis=0)
    y_train = np.append(y_train, y_test_value)
    return x_train, y_train, x, y

#-----------------------------------------------------------------------#
#Initialiser x_train et y_train
random_index = random.randint(0, len(x)-1) # Sélectionner un index aléatoire

x_test_value = x[random_index]
x = np.delete(x, random_index, axis=0)
    
y_test_value = y[random_index]
y = np.delete(y, random_index)

x_train = np.array([x_test_value])
y_train = np.array(y_test_value)
#-----------------------------------------------------------------------#
print("Generating x_train, y_train, x_test, y_test")
#Généraliser x_train et y_train
# Générer l'ensemble de test
for size_test in range(0,int(0.2*size_x)): # 20% pour les valeurs de test
    random_index = random.randint(0, len(x)-1) # Sélectionner un index aléatoire
    x_train, y_train, x, y = append_and_pop(random_index, x_train, y_train, x, y)

# Données d'entraînement et de test
x_test = x
y_test = y

np.save("x_train.npy", x_train)
np.save("y_train.npy", y_train)
np.save("x_test.npy", x_test)
np.save("y_test.npy", y_test)
print("Data Created")
