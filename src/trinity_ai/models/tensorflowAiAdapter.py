
import tensorflow as tf
# print('tensorFlow')
# # Función para cargar un modelo de IA pre-entrenado
def load_model(model_path):
  try:
    return tf.keras.models.load_model(model_path)
  except Exception as error:
    print(f'Error al cargar el modelo de IA: {error}')
  return None

# # Función para realizar una predicción con el modelo de IA
def predict(model, input_data):
  try:
    input_tensor = tf.convert_to_tensor(input_data)
    prediction = model.predict(input_tensor)
    return prediction.numpy()
  except Exception as error:
    print(f'Error al realizar la predicción: {error}')
  return None

def save_model(model, model_path):
  try:
    tf.keras.models.save_model(model, model_path)
    print(f'Modelo de IA guardado en: {model_path}')
  except Exception as error:
    print(f'Error al guardar el modelo de IA: {error}')

