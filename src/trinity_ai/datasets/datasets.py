import json
import tensorflow as tf


def load_test_data(file_path='test.json'):
    """
    Carga los datos de prueba desde un archivo JSON.

    Args:
        file_path (str): La ruta al archivo JSON.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un ejemplo de prueba.
    """
    try:
        with open(file_path, 'r') as f:
            test_data = json.load(f)
        return test_data
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{file_path}' contiene datos JSON inválidos.")
        return None
    except PermissionError:
        print(f"Error: No se tiene permiso para leer el archivo '{file_path}'.")
        return None

def load_training_data():   #file_path='./training.json'):
    """
    Carga los datos de entrenamiento desde un archivo JSON.

    Args:
        file_path (str): La ruta al archivo JSON.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un ejemplo de entrenamiento.
    """
    try:
        # with open(file_path, 'r') as f:
        #     training_data = json.load(f)
        #     print(training_data.length)
        trainig_data = training
        print(len(trainig_data))
        return training_data
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{file_path}' contiene datos JSON inválidos.")
        return None
    except PermissionError:
        print(f"Error: No se tiene permiso para leer el archivo '{file_path}'.")
    return None

def create_tfrecords():
    """
    Genera un archivo TFRecord a partir de un archivo JSON.

    Args:
        json_file (str): La ruta al archivo JSON.
        tfrecord_file (str): La ruta al archivo TFRecord de salida.
    """
    with open('training.json', 'r') as f:
     data = json.load(f)
