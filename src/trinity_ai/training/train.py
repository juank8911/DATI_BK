import json as json
import pandas as pd
import yfinance as yf
# import ..models.tensorflowAiAdapter. as get_klines_data
from ..models.tensorflowAiAdapter import get_klines_data
# from ..models.tensorflowAiAdapter import 
# from ..models import tensorflowAiAdapter
# from ..datasets import datasets


def get_wallet_balance():
    
    """
    Obtiene el saldo actual de la billetera.

    Returns:
        float: El saldo de la billetera.
    """
    return 1000.0

# def train_model(training_data, test_data):
#     # """
#     # Entrena un modelo de IA para predecir el movimiento de precios de criptomonedas.

#     # Args:
#     #     training_data (list): Lista de diccionarios con datos de entrenamiento.
#     #     test_data (list): Lista de diccionarios con datos de prueba.

#     # Returns:
#     #     tensorflow.keras.Model: El modelo de IA entrenado.
#     # """

#     # # 1. recorrer los datos de el archivo tranin_data, obtener los que tienen el valor
#     # logro mas alto, la media, promedio, ema, sma para obtener los tokens con mayor fluctuacion
    

#     # # 2. una vez tiene los datos de los tokens mas prometedores, solicitar los datos por soket 
#     # las klines de los tokens seleccionados.
    

#     # # 3. Buscar los token que generen mas de 0.5% cada nueva vela puede ser en largo o en corto 
#     #(de subida o bajada del precio ) segun los datos del archivo y el valor actual 


#     # # 4. buscar las mejores oportunidades para comprar en largo o vender en corto para obtener el mayor
#     # porcentaje de ganancia posible que debe ser minimo 0.5% por minuto 
    

#     # # 5. Pronosticar el movimiento de precios
#     # predictions = predict_price_movement(model, training_data)

#     # # 6. Simular operaciones de trading
#     backtest_results = simulate_trading(predictions, training_data)

#     # # 7. Entrenar el modelo de IA
#     model = tensorflowAiAdapter.create_model()
#     model.fit(filtered_training_data, epochs=10)  # Ajustar los parámetros de entrenamiento según sea necesario

#     return null

def evaluate_model(model, test_data):
    """
    Evalúa el rendimiento del modelo de IA.

    Args:
        model (tensorflow.keras.Model): El modelo de IA entrenado.
        test_data (list): Lista de diccionarios con datos de prueba.
    """
    print()
    # # Evaluar el modelo con los datos de prueba
    # loss, accuracy = model.evaluate(test_data)
    # print(f"Pérdida: {loss}, Precisión: {accuracy}")

    # # Mostrar resultados de la evaluación
    # Plot_evaluation_results(loss, accuracy)

def train_model(training_data, test_data):
    """
    Entrena un modelo de IA para predecir el movimiento de precios de criptomonedas.

    Args:
        training_data (list): Lista de diccionarios con datos de entrenamiento.
        test_data (list): Lista de diccionarios con datos de prueba.

    Returns:
        tensorflow.keras.Model: El modelo de IA entrenado.
    """

    # 1. Identificar tokens volátiles
    volatile_symbols = find_volatile_symbols(training_data)

    # 2. Obtener datos de klines para tokens volátiles
    klines_data = get_klines_data()

    # 3. Filtrar tokens con oportunidades de trading
    filtered_training_data = filter_trading_opportunities(training_data)

    # 4. Buscar oportunidades de compra en largo o venta en corto
    trading_opportunities = find_trading_opportunities(filtered_training_data)

    # 5. Pronosticar el movimiento de precios
    predictions = predict_price_movement(model, filtered_training_data)

    # 6. Simular operaciones de trading
    backtest_results = simulate_trading(predictions, filtered_training_data)

    # 7. Entrenar el modelo de IA
    model = tensorflowAiAdapter.create_model()
    model.fit(filtered_training_data, epochs=10)  # Ajustar los parámetros de entrenamiento según sea necesario

    return model

def find_volatile_symbols(training_data):
    print(training_data)
 # 1. 
    


def calculate_volatility(ticker, period="1y", timeperiod=14):
    """
    Calcula la volatilidad de los precios de un activo utilizando YFinance.

    Args:
        ticker (str): El símbolo del activo (por ejemplo, "BTC-USD").
        period (str, optional): El período de tiempo para descargar los datos. 
                                 Defaults to "1y" (1 año).
        timeperiod (int, optional): El período de tiempo para calcular la desviación estándar. 
                                    Defaults to 14 (14 días).

    Returns:
        float: La volatilidad del activo.
    """

    # Descarga los datos de precios del activo
    # data = yf.download(ticker, period=period)

    return null

def predict_price_movement(model, input_data):
    """
    Pronostica el movimiento de precios usando el modelo de IA.

    Args:
        model (tensorflow.keras.Model): El modelo de IA entrenado.
        input_data (list): Lista de diccionarios con datos de entrada para la predicción.

    Returns:
        list: Una lista de predicciones de movimiento de precios.
    """
    return null

def simulate_trading(predictions, filtered_training_data):
  """
  Función para simular operaciones de trading con base en las predicciones.

  Args:
    predictions: Lista de predicciones con información de probabilidad de subida/bajada y magnitud de la fluctuación.
    filtered_training_data: Conjunto de datos filtrado con características etiquetadas.
  """

  # Obtener información de las predicciones
  probability_up = predictions["upward_probability"]
  probability_down = predictions["downward_probability"]
  price_fluctuation = predictions["price_fluctuation"]

  # Obtener datos del conjunto de datos filtrado
  features = filtered_training_data.features
  labels = filtered_training_data.labels

  token_name = features["token_name"]
  # Obtener apalancamiento máximo del token
  max_leverage = get_token_leverage(token_name)  # Función no implementada

  # Inicializar variables de trading
  balance = get_wallet_balance()  # Obtener balance inicial
  position = 0  # Posición actual (0: sin posición, 1: compra, -1: venta)
  entry_price = 0  # Precio de entrada a la operación actual
  cumulative_profit = 0  # Ganancia acumulada

  # Recorrer las predicciones
  for i in range(len(predictions)):
    # Obtener características y etiqueta de la vela actual
    current_features = features[i]
    current_label = labels[i]

    # Verificar si hay predicción de subida o bajada
    if probability_up > probability_down:
      # Predicción de subida
      if position == 0:  # Sin posición actual
        # Calcular cantidad a invertir
        amount_to_invest = calculate_investment_amount(balance, max_leverage, current_features)

        # Comprar token
        buy_token(token_name, amount_to_invest)
        position = 1  # Actualizar posición a compra
        entry_price = current_features["precio_cierre"]  # Registrar precio de entrada

      elif position == -1:  # Posición de venta actual
        # Vender token para cerrar posición
        sell_token(token_name)
        position = 0  # Actualizar posición a sin posición

    elif probability_down > probability_up:
      # Predicción de bajada
      if position == 0:  # Sin posición actual
        # Calcular cantidad a invertir
        amount_to_invest = calculate_investment_amount(balance, max_leverage, current_features)

        # Vender token en corto
        sell_token_short(token_name, amount_to_invest)
        position = -1  # Actualizar posición a venta
        entry_price = current_features["precio_cierre"]  # Registrar precio de entrada

      elif position == 1:  # Posición de compra actual
        # Comprar token para cerrar posición
        buy_token(token_name)
        position = 0  # Actualizar posición a sin posición

    # Calcular ganancia/pérdida en la operación actual
    current_profit = calculate_profit_loss(current_features["precio_cierre"], entry_price, position)

    # Actualizar balance y ganancia acumulada
    balance += current_profit
    cumulative_profit += current_profit

    # Guardar el 25% de las ganancias cuando el balance aumenta en $100
    if balance >= previous_balance + 100:
      save_profit(cumulative_profit * 0.25)  # Función no implementada
      previous_balance = balance  # Actualizar balance anterior

    # Imprimir información de la operación
    print(f"Operación {i+1}:")
    print(f"Predicción: {probability_up:.2%} subida, {probability_down:.2%} bajada")
    print(f"Magnitud de fluctuación: {price_fluctuation:.2%}")
    print(f"Posición: {position}")
    print(f"Ganancia/pérdida actual: {current_profit:.2%}")
    print(f"Balance actual: {balance:.2%}")
    print(f"Ganancia acumulada: {cumulative_profit:.2%}")
    print("-------------------------")

def filter_trading_opportunities(training_data):

  """
  Función para procesar datos de entrenamiento y generar un conjunto de datos para el modelo.

  Args:
    training_data: Lista de diccionarios con datos de Klines.

  Returns:
    Conjunto de datos de TensorFlow con características y etiquetas.
  """

  # Inicializar listas vacías para almacenar datos
  candles = []
  labels = []

  # Recorrer los datos de entrenamiento
  for token_data in training_data:
    # Extraer datos de Klines
    klines = token_data["data"]

    # Recorrer las velas
    for i in range(len(klines) - 1):
      # Calcular cambio de precio
      price_change = (klines[i + 1]["precio_cierre"] - klines[i]["precio_cierre"]) / klines[i]["precio_cierre"]

      # Verificar si hay oportunidad de trading
      if abs(price_change) > 0.005:
        # Extraer características relevantes
        candle_features = extract_features(klines[i], klines[i + 1])

        # Calcular etiqueta de predicción
    if price_change > 0:
          label = 1  # Subida
    else:
          label = 0  # Bajada

        # Añadir datos a las listas
    candles.append(candle_features)
    labels.append(label)

    # Convertir listas a arrays de NumPy
    candles = np.array(candles)
    labels = np.array(labels)

    # Crear conjunto de datos de TensorFlow
    dataset = tf.data.Dataset.from_tensor_slices((candles, labels)) 
    print(training_data)
      # Retornar el conjunto de datos
  return dataset
    
    
def find_trading_opportunities(filtered_training_data):
  """
  Función para filtrar tokens prometedores del conjunto de datos filtrado.

  Args:
    filtered_training_data: Conjunto de datos de TensorFlow filtrado.

  Returns:
    Lista de tokens prometedores.
  """

  # Extraer datos del conjunto de datos
  features, labels = filtered_training_data

  # Calcular métricas de rendimiento
  performance_metrics = calculate_performance_metrics(features, labels)

  # Filtrar tokens
  filtered_tokens = []
  for token_data, metrics in zip(filtered_training_data, performance_metrics):
    token_name = token_data[0][0]  # Obtener nombre del token
    average_profit = metrics["average_profit"]
    win_rate = metrics["win_rate"]
    sharpe_ratio = metrics["sharpe_ratio"]

    # Aplicar criterios de filtrado
    if (average_profit > 0.005) and (win_rate > 0.5) and (sharpe_ratio > 1):
      filtered_tokens.append(token_name)

  # Retornar lista de tokens prometedores
  return filtered_tokens

def predict_price_movement(model, filtered_training_data):
  """
  Función para predecir el movimiento del precio del token en la siguiente vela.

  Args:
    model: Modelo de aprendizaje automático entrenado.
    filtered_training_data: Conjunto de datos de TensorFlow filtrado.

  Returns:
    Información de predicción para el token.
  """

  # Extraer datos del conjunto de datos
  features, labels = filtered_training_data

  # Preparar datos de entrada
  last_candle_features = extract_last_candle_features(features)
  historical_features = extract_historical_features(features)

  # Realizar predicción
  predictions = model.predict([last_candle_features, historical_features])

  # Interpretar resultados
  prediction_probabilities = predictions[0]  # Probabilidades de subida y bajada
  price_fluctuation = predictions[1]  # Magnitud de la fluctuación

  # Calcular probabilidad de predicción correcta
  prediction_accuracy = calculate_prediction_accuracy(prediction_probabilities, labels)  # Función no implementada

  # Generar información de predicción
  prediction_info = {
    "token_name": token_name,  # Obtener nombre del token
    "upward_probability": prediction_probabilities[0],  # Probabilidad de subida
    "downward_probability": prediction_probabilities[1],  # Probabilidad de bajada
    "price_fluctuation": price_fluctuation,  # Magnitud de la fluctuación
    "prediction_accuracy": prediction_accuracy,  # Probabilidad de predicción correcta
  }

  # Retornar información de predicción
  return prediction_info

def extract_features(kline1, kline2):
  """
  Función para extraer características relevantes de dos velas.

  Args:
    kline1: Diccionario de datos de la primera vela.
    kline2: Diccionario de datos de la segunda vela.

  Returns:
    Lista de características extraídas.
  """

  # Extraer características básicas
  features = [
    kline2["precio_cierre"] - kline1["precio_cierre"],  # Cambio de precio
    kline2["volumen"],  # Volumen de la segunda vela
    kline2["precio_maximo"] - kline2["precio_minimo"],  # Rango de precios
    (kline2["precio_cierre"] - kline2["precio_minimo"]) / kline2["precio_minimo"] * 100,  # Sombra inferior
    (kline2["precio_maximo"] - kline2["precio_cierre"]) / kline2["precio_maximo"] * 100,  # Sombra superior
  ]

  # Calcular indicadores técnicos (ejemplos)
  rsi = calculate_rsi(kline1["precio_cierre"], kline2["precio_cierre"])
  macd = calculate_macd(kline1["precio_cierre"], kline2["precio_cierre"])
  features.extend([rsi, macd[0], macd[1], macd[2]])  # RSI, MACD (línea de señal, MACD, histograma)

  # Retornar lista de características
  return features

def extract_last_candle_features(features):
  """
  Función para extraer características relevantes de la última vela.

  Args:
    features: Matriz de características del conjunto de datos.

  Returns:
    Lista de características de la última vela.
  """

  # Extraer características de la última vela
  last_candle_features = features[-1]

  # Retornar lista de características de la última vela
  return last_candle_features

def extract_historical_features(features):
  """
  Función para extraer características históricas del token.

  Args:
    features: Matriz de características del conjunto de datos.

  Returns:
    Lista de características históricas.
  """

  # Convertir la matriz a DataFrame para facilitar el manejo de datos
  df = pd.DataFrame(features)

  # Calcular características históricas (ejemplos)
  average_profit = df["cambio_precio"].mean()  # Ganancia promedio por operación
  win_rate = df[df["cambio_precio"] > 0].shape[0] / len(df)  # Porcentaje de operaciones ganadoras
  # ... (añadir más características históricas si es necesario)

  # Convertir las características a lista
  historical_features = [average_profit, win_rate]

  # Retornar lista de características históricas
  return historical_features

def calculate_prediction_accuracy(prediction_probabilities, labels):
  """
  Función para calcular la probabilidad de predicción correcta.

  Args:
    prediction_probabilities: Lista de probabilidades predichas (subida, bajada).
    labels: Lista de etiquetas reales (1 para subida, 0 para bajada).

  Returns:
    Probabilidad de predicción correcta.
  """

  # Calcular índice de aciertos
  correct_predictions = np.sum(np.argmax(prediction_probabilities, axis=1) == labels)

  # Calcular probabilidad de predicción correcta
  prediction_accuracy = correct_predictions / len(prediction_probabilities)

  # Retornar probabilidad de predicción correcta
  return prediction_accuracy

def calculate_investment_amount(balance, max_leverage, current_features):
  """
  Función para calcular la cantidad a invertir en una operación de trading.

  Args:
    balance: Balance disponible en la cuenta (float).
    max_leverage: Apalancamiento máximo del token (float).
    current_features: Vector de características de la vela actual (dict).

  Returns:
    Cantidad a invertir (float).
  """

  # Obtener precio actual del token
  current_price = current_features["precio_cierre"]

  # Establecer inversión mínima por token
  min_investment_per_token = 0.7  # USD

  # Determinar número máximo de tokens a invertir
  if balance < 3:
    number_of_tokens = 1
  elif balance < 6:
    number_of_tokens = 2
  elif balance < 10:
    number_of_tokens = 3
  else:
    number_of_tokens = int(balance / min_investment_per_token)

  # Calcular inversión total por token
  investment_per_token = balance / number_of_tokens

  # Limitar inversión por token a la inversión mínima
  investment_per_token = max(investment_per_token, min_investment_per_token)

  # Calcular cantidad total a invertir
  total_investment = investment_per_token * number_of_tokens

  # Aplicar apalancamiento
  total_investment *= max_leverage

  # Retornar cantidad total a invertir
  return total_investment
    