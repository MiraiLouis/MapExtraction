import os
import sys
import numpy as np

# Obtenir le chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
current_dir = os.path.dirname(__file__)
resources_dir = os.path.join(current_dir, "..", "Ressources")  # Chemin vers le répertoire des ressources

# Ajouter le chemin du répertoire parent au chemin de recherche des modules
sys.path.append(parent_dir)

# Maintenant, vous pouvez importer le module
from Load_IA import Load_IA


x_test_path = os.path.join(resources_dir, "x_test.npy")
y_test_path = os.path.join(resources_dir, "y_test.npy")

x_test = np.load(x_test_path)
y_test = np.load(y_test_path)
y_test = y_test.reshape(-1, 1)

traind_model = Load_IA.Load_IA()
loss, accuracy = traind_model.evaluate(x_test, y_test)
print("Perte sur l'ensemble de test :", loss)
print("Précision sur l'ensemble de test :", accuracy)
