
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

def get_token_leverage(token_name):
  """
  Función para obtener el apalancamiento máximo de un token.

  Args:
    token_name: Nombre del token (por ejemplo, "BTC/USDT").

  Returns:
    Apalancamiento máximo del token (float).
  """

  # Obtener exchange de la API
  exchange = ccxt.binance()  # Suponiendo que se utiliza una API de CCXT inicializada

  # Consultar información del token
  token_info = exchange.fetch_ticker(token_name)

  # Extraer apalancamiento máximo
  max_leverage = token_info["info"]["maxLeverage"]

  # Retornar apalancamiento máximo
  return max_leverage

async def tokensData(symbolsD):
    """
    Suscribe a Webhooks para eventos 'kline_closed' en Binance Futures para los símbolos proporcionados.

    Args:
        symbolsD (list): Lista de símbolos a monitorear.
    """

    exchange = ccxt.binance()

    async def handle_kline_closed(data):
        """
        Procesa las notificaciones Webhook 'kline_closed' y actualiza los datos del token (implementación de ejemplo).

        Args:
            data (dict): Datos de notificación Webhook que contienen información sobre el símbolo y la vela.
        """

        symbol = data['symbol']
        open_time = data['k']['openTime']
        open_price = data['k']['open']
        close_price = data['k']['close']
        volume = data['k']['volume']

        # Actualiza los datos del token en tu sistema (adapta según tu estructura de datos)
        # Ejemplo:
        if symbol in token_data:
            token_data[symbol]['last_candle'] = {
                'open_time': open_time,
                'open_price': open_price,
                'close_price': close_price,
                'volume': volume
            }
        else:
            token_data[symbol] = {
                'last_candle': {
                    'open_time': open_time,
                    'open_price': open_price,
                    'close_price': close_price,
                    'volume': volume
                }
            }

        print(f"Notificación Webhook recibida para {symbol}: Apertura: {open_price}, Cierre: {close_price}")

    # Suscríbete a Webhooks para cada símbolo
    for symbol in symbolsD:
        await exchange.subscribe_to_kline_updates(symbol=symbol, interval='1m', callback=handle_kline_closed)

    # Mantén la conexión abierta para recibir notificaciones Webhook (opcional)
    await exchange.wait_for_subscription_response()

if __name__ == "__main__":
    get_klines_data(),
    load_model(),
    tokensData(),
  