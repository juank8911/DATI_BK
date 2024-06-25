# ./trinity_ai/__init__.py
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf


from .datasets.datasets import load_test_data,load_training_data,create_TFRecords
# from datasets import datasets
print('carga datasets')
from .models.tensorflowAiAdapter import load_model, save_model
print('carga models')
from .training.train import train_model, evaluate_model
print('carga train')



async def initialize_trinity_model():
    """
    Inicializa el modelo de IA de Trinity.

    Esta función carga el modelo pre-entrenado o entrena un nuevo modelo si no existe.
    """
    
    # Cargar el modelo pre-entrenado si existe
    try:
        await create_TFRecords()
        model = load_model('./models/')
        print(model)
        if model != None:
            print('inicia modelo')
            print("Modelo de IA de Trinity cargado correctamente.")
            # Evaluar el modelo cargado
            test_data = load_test_data('J:\ProyectosCriptoMon\DATI\src\trinity_ai\datasets\dataFut.json')
            accuracy = evaluate_model(model, test_data)
            print(f"Precisión del modelo: {accuracy:.2f}%")
            if accuracy < 0.8:  # Si la precisión es menor al 80%
                print("Precisión del modelo inferior al 80%. Reentrenando...")
                training_data = load_training_data()
                model = train_model(training_data, test_data)
                evaluate_model(model, test_data)
                save_model(model, './models')
                print("Modelo de IA de Trinity reentrenado y guardado correctamente.")
        else:
        # except FileNotFoundError:
            print("No se encontró un modelo pre-entrenado. Entrenando un nuevo modelo...")

            # Entrenar un nuevo modelo si no existe
            training_data = load_training_data('J:\ProyectosCriptoMon\DATI\src\\trinity_ai\datasets\dataFut.json')
            test_data = load_test_data('J:\ProyectosCriptoMon\DATI\src\\trinity_ai\datasets\dataFut.json')
            model = train_model(training_data, test_data)
            print('evaluate')
            evaluate_model(model, test_data)
            save_model(model, './models')
            print("Modelo de IA de Trinity entrenado y guardado correctamente.")
        return model
    except FileNotFoundError:
        print("Error: ",FileNotFoundError)
        
        
async def train_model_directly():
    """
    Función para iniciar el entrenamiento del modelo de IA directamente.
    """
    # 1. Cargar los datos de entrenamiento y prueba
    training_data = load_training_data()
    test_data = load_test_data()

    # 2. Entrenar el modelo
    model = train_model(training_data, test_data)

    # 3. Evaluar el modelo
    evaluate_model(model, test_data)

    # 4. Guardar el modelo entrenado
    save_model(model)

    print("¡Entrenamiento completado!")
        
__all__ = [
    'load_model',
    'load_test_data',
    'load_training_data',
    'train_model',
    'evaluate_model',
    'save_model',
    'initialize_trinity_model',
    'train_model_directly',
]
