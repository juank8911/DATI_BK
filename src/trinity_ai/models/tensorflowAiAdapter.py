
import threading
import os
import time
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import ccxt as ccxt


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
    
    
# ... (tensorflowAiAdapter.py code from previous response) ...

def get_klines_data():
    """
    Conecta al socket de Binance y obtiene la vela actual de 1m cada segundo para los símbolos futuros volátiles.

    Args:
        volatile_symbols (list): Lista de símbolos futuros volátiles.

    Returns:
        dict: Diccionario con los datos de las velas de cada símbolo.
    """

    exchange = ccxt.binance()
    klines_data = {}

    def fetch_klines():
      markets = exchange.fetch_markets()

      # Filtrar los mercados de futuros
      future_symbols = [market['symbol'] for market in markets if market['type'] == 'future']
      while True:
            for symbol in future_symbols:
                try:
                    # Obtiene los datos de la vela actual de 1m
                    klines = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=1)
                    # Agrega los datos al diccionario
                    klines_data[symbol] = klines[0]
                except Exception as e:
                    print(f"Error al obtener datos de {symbol}: {e}")

            # Espera 1 segundo
            time.sleep(1)

  
    # Inicia un hilo separado para obtener los datos de las velas
    klines_thread = threading.Thread(target=fetch_klines)
    klines_thread.daemon = True
    klines_thread.start()

    return klines_data


if __name__ == "__main__":
    get_klines_data(),
    load_model(),
  