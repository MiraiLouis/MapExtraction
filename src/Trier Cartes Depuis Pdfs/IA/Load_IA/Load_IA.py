import os
import sys
import h5py

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from build_model import build_and_train_model

def Load_IA():
    current_dir = os.path.dirname(__file__)
    resources_dir = os.path.join(current_dir, "..", "Ressources")  # Chemin vers le répertoire des ressources

    mini_x_train_path = os.path.join(resources_dir, "mini_x_train.npy")
    mini_x_test_path = os.path.join(resources_dir, "mini_x_test.npy")
    mini_y_train_path = os.path.join(resources_dir, "mini_y_train.npy")
    mini_y_test_path = os.path.join(resources_dir, "mini_y_test.npy")
    vgg_weights_path = os.path.join(resources_dir, "vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5")
    model_weights_path = os.path.join(resources_dir, 'model.weights.h5')
    model = build_and_train_model(mini_x_train_path,
                                   mini_x_test_path,
                                   mini_y_train_path,
                                   mini_y_test_path,
                                   vgg_weights_path)

    model.load_weights(os.path.join(current_dir, model_weights_path))
    return model
