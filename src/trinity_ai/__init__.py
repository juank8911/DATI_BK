from .models import trinityModel, tensorflowAiAdapter
from .datasets import load_training_data, load_test_data
from .training import train_model, evaluate_model

__all__ = [
    'trinityModel',
    'tensorflowAiAdapter',
    'load_training_data',
    'load_test_data',
    'train_model',
    'evaluate_model',
    'initialize_trinity_model',
]

def initialize_trinity_model():
    """
    Inicializa el modelo de IA de Trinity.

    Esta función carga el modelo pre-entrenado o entrena un nuevo modelo si no existe.
    """
    # Cargar el modelo pre-entrenado si existe
    try:
        model = tensorflowAiAdapter.load_model('./models')
        print("Modelo de IA de Trinity cargado correctamente.")
        return model
    except FileNotFoundError:
        print("No se encontró un modelo pre-entrenado. Entrenando un nuevo modelo...")

    # Entrenar un nuevo modelo si no existe
    training_data = load_training_data()
    test_data = load_test_data()
    model = train_model(training_data, test_data)
    evaluate_model(model, test_data)
    tensorflowAiAdapter.save_model(model, 'path/to/your/model')
    print("Modelo de IA de Trinity entrenado y guardado correctamente.")
    return model
