import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, Dropout, Flatten, BatchNormalization
import numpy as np
import os




def build_model_bis(base_model, size = 3, activation = 'relu', dropout = True):


    model = Sequential()
    model.add(base_model)

    #Aplatir les sorties du modèle de base pour les connecter aux couches denses
    model.add(Flatten())

    # Ajout de couches Dense
    for i in range(size):
        model.add(Dense(512, activation=activation)) # Utilisez 512 comme nombre de neurones exemple
        if dropout:
            model.add(Dropout(0.5)) # Exemple de taux de dropout

    model.add(Dense(1, activation='sigmoid'))

    model.compile(
        loss='binary_crossentropy',
        optimizer=tf.keras.optimizers.Adam(0.0001),
        metrics=['accuracy']
    )

    return model

def build_model (x_train_path = "x_train.npy",
                 weights_path = "vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5"):

    x_train = np.load(x_train_path)
    input_shape = x_train.shape[1:]
    num_classes = 1

    base_model = VGG16(include_top=False, weights=weights_path, input_shape=input_shape)
    base_model.trainable = False

    model = build_model_bis(base_model)
    return model

def train_model(model,
                x_train_path = "x_train.npy",
                x_test_path = "x_test.npy",
                y_train_path = "y_train.npy",
                y_test_path = "y_test.npy"):
    x_train = np.load(x_train_path)
    x_test = np.load(x_test_path)
    y_train = np.load(y_train_path)
    y_test = np.load(y_test_path)
    y_train = y_train.reshape(-1, 1)
    y_test = y_test.reshape(-1, 1)
    model.fit(x_train, y_train, epochs=3, validation_data=(x_test, y_test))
    return model

def build_and_train_model(x_train_path = "x_train.npy",
                          x_test_path = "x_test.npy",
                          y_train_path = "y_train.npy",
                          y_test_path = "y_test.npy",
                          weights_path = "vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5"):
    return train_model(build_model(x_train_path, weights_path),
                       x_train_path,
                       x_test_path,
                       y_train_path,
                       y_test_path)
