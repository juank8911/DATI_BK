# trinity_ai/datasets/datasets.py

import json

def load_training_data():
    """
    Carga los datos de entrenamiento desde el archivo training.json.

    Returns:
        list: Una lista de diccionarios que representan los datos de entrenamiento.
    """
    with open('training.json', 'r') as f:
        training_data = json.load(f)
    return training_data

def load_test_data():
    """
    Carga los datos de prueba desde el archivo test.json.

    Returns:
        list: Una lista de diccionarios que representan los datos de prueba.
    """
    with open('test.json', 'r') as f:
        test_data = json.load(f)
    return test_data
