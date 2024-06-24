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

def simulate_trading(predictions, training_data, leverage=2, min_profit_percentage=0.01):
    """
    Simula operaciones de trading con las predicciones del modelo.

    Args:
        predictions (list): Lista de predicciones de movimiento de precios.
        training_data (list): Lista de diccionarios con datos de entrenamiento.
        leverage (int): El apalancamiento a utilizar en las operaciones.
        min_profit_percentage (float): El porcentaje mínimo de ganancia para cerrar una operación.

    Returns:
        list: Una lista de resultados de las operaciones simuladas.
    """
    trading_results = []
    # for i, prediction in enumerate(predictions):
        # Verifica si la predicción indica una operación en largo o corto
        # if prediction > 0.5:  # Ajusta el umbral según sea necesario
            # Abre una operación en largo
            # entry_price = training_data[i]['candles'][-1]['close']
            # Simula la operación y calcula la ganancia
            # ...
            # Cierra la operación cuando se alcanza el objetivo de ganancia o se alcanza un límite de tiempo
            # ...
            # trading_results.append({'symbol': training_data[i]['symbol'], 'operation': 'largo', 'profit': profit, 'duration': duration})
        # else:
            # Abre una operación en corto
            # ...
    return trading_results

def filter_trading_opportunities(training_data):
    print(training_data)
    
    