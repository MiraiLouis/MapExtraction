import numpy as np
from PIL import Image
def get_resized_image_array(image_path):
    image = Image.open(image_path).convert('RGB')  # Convertir l'image en RGB
    resized_image = image.resize((100, 100))
    resized_image_array = np.array(resized_image)
    resized_image_array = resized_image_array.reshape(1, 100, 100, 3)  # Pour une image RGB
    resized_image_array = resized_image_array / 255.0
    return resized_image_array

def Prediction_IA(model, image_path):
    resized_image_array = get_resized_image_array(image_path)
    # Obtenir la prédiction du modèle sur l'image de test
    prediction = model.predict(resized_image_array)
    return prediction[0][0]  # Renvoie la valeur de prédiction
