import json
import os
import tensorflow as tf
# file_path = 'J:\ProyectosCriptoMon\DATI\src\trinity_ai\datasets\dataFut.json'

def load_test_data(file_path):
    """
    Convierte datos JSON al formato TensorFlow para entrenamiento de modelos.

    Args:
        file_path (str, optional): Ruta al archivo JSON que contiene los datos. Defaults to '/dataFut.json'.

    Returns:
         list: Lista de diccionarios, donde cada diccionario representa un ejemplo de entrenamiento.
    """
    # sourcery skip: return-or-yield-outside-function
    try:
        # Check if the file exists at the specified path
        if not os.path.isfile(file_path):
         raise FileNotFoundError(f"File not found: {file_path}")
        #  print(file_path)
        # Cargar datos JSON
        with open(file_path) as f:
            # print(f)
            datas = json.load(f)

        # Convertir datos a formato TensorFlow
        tf_data = []
        # data = data[1]
        
        for symbol_data in datas:
            symbol_dict = symbol_data['symbol']
            print(symbol_dict)
            name = symbol_dict['name']
            data_klines =  symbol_dict['data'][0]  # Extraer la primera lista de data_klines (asumiendo 180 elementos)

        #     # Convertir data_klines (lista) a tensor de TensorFlow
            data_tensor = tf.convert_to_tensor(data_klines, dtype=tf.float32)

        #     # Crear un diccionario con los datos en formato TensorFlow
            tf_symbol = {
                'name': tf.convert_to_tensor(name, dtype=tf.string),
                'data': data_tensor,
                'promedio': tf.convert_to_tensor(symbol['promedio'], dtype=tf.string),
                'logro': tf.convert_to_tensor(symbol['logro'], dtype=tf.int64),
                'ema': tf.convert_to_tensor(symbol['ema'], dtype=tf.float32),
                'pft': tf.convert_to_tensor(symbol['pft'], dtype=tf.float32),
                'SMA': tf.convert_to_tensor(symbol['SMA'], dtype=tf.float32),
            }

        #     # Agregar el diccionario a la lista de datos TensorFlow
        tf_data.append(tf_symbol)
        return tf_data
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None  # Indicate file not found  


import json
import tensorflow as tf
import os  # Import for file path handling

def load_training_data(file_path='/dataFut.json'):
  """
  Convierte datos JSON al formato TensorFlow para entrenamiento de modelos.

  Args:
      file_path (str, optional): Ruta al archivo JSON que contiene los datos. Defaults to '/dataFut.json'.

  Returns:
      list: Lista de diccionarios, donde cada diccionario representa un ejemplo de entrenamiento en formato TensorFlow,
          o None si el archivo no se encuentra.
  """

  try:
    # Check if the file exists at the specified path
    if not os.path.isfile(file_path):
      raise FileNotFoundError(f"File not found: {file_path}")

    # Open the file and load JSON data
    with open(file_path) as f:
      datas = json.load(f)

    # Process each symbol's data
    tf_data = []
    for symbol_data in datas:
      symbol_dict = symbol_data['symbol']

      # Extract necessary information
      name = symbol_dict['name']
      data_klines = symbol_dict['data'][0]  # Assuming the first list contains kline data

      # Separate and convert data_klines (assuming specific structure)
      timestamps = tf.convert_to_tensor([int(x) for x in data_klines[::7]], dtype=tf.int64)  # Extract timestamps
      numeric_values = tf.convert_to_tensor([float(x) for x in data_klines[1::7] if x != '0'], dtype=tf.float32)  # Extract numeric values, excluding '0'

      # Create a dictionary with TensorFlow tensors
      tf_symbol = {
          'name': tf.convert_to_tensor(name, dtype=tf.string),
          'data': tf.stack([timestamps, numeric_values]),  # Stack timestamps and numeric values (assuming consistent structure)
          'promedio': tf.convert_to_tensor(symbol_dict['promedio'], dtype=tf.string),
          'logro': tf.convert_to_tensor(symbol_dict['logro'], dtype=tf.int64),
          'ema': tf.convert_to_tensor(symbol_dict['ema'], dtype=tf.float32),
          'pft': tf.convert_to_tensor(symbol_dict['pft'], dtype=tf.float32),
          'SMA': tf.convert_to_tensor(symbol_dict['SMA'], dtype=tf.float32),
      }

      # Add the dictionary to the training data list
      tf_data.append(tf_symbol)

    return tf_data

  except FileNotFoundError as e:
    print(f"Error: {e}")
    return None  # Indicate file not found





async def create_TFRecords():
  """Converts dataFut.json to TFRecords and saves it to src\trinity_ai\datasets."""

  # Path to the JSON file
  json_file_path = 'src/trinity_ai/datasets/dataFut.json'  # Corrected path

  # Path to save the TFRecords file
  tfrecords_file_path = 'src/trinity_ai/datasets/training.tfrecord'

  # Load the JSON data
  with open(json_file_path, 'r') as f:
    data = json.load(f)

  # Create a TFRecord writer
  with tf.io.TFRecordWriter(tfrecords_file_path) as writer:
    for symbol_data in data:
      symbol = symbol_data['symbol']
      candles = symbol_data['symbol']['data'] 
    # Convert candle data to features using the function
    features = {
      'name': tf.train.Feature(bytes_list=tf.train.BytesList(value=[symbol['name'].encode()])),
      'data': create_candlestick_feature(candles),  # Use the function here
      'promedio': tf.train.Feature(bytes_list=tf.train.BytesList(value=[symbol['promedio'].encode()])),
      'logro': tf.train.Feature(int64_list=tf.train.Int64List(value=[symbol['logro']])),
      'ema': tf.train.Feature(float_list=tf.train.FloatList(value=[float(symbol['ema'])])),
      'pft': tf.train.Feature(float_list=tf.train.FloatList(value=[float(symbol['pft'])])),
      'SMA': tf.train.Feature(float_list=tf.train.FloatList(value=[float(symbol['SMA'])])),
    }

        # Create a TFRecord example
    example = tf.train.Example(features=tf.train.Features(feature=features))

        # Write the example to the TFRecords file
    writer.write(example.SerializeToString())

  print(f'TFRecords file created successfully at: {tfrecords_file_path}')
  
  
def create_candlestick_feature(candles):
    """
    Convierte una lista de datos de una vela (candlestick) en una característica TensorFlow.

    Args:
      candle (list): Lista que contiene los datos de la vela.

    Returns:
      tf.train.Feature: Una característica TensorFlow con los datos de la vela.
    """
    for candel in candles:
      # Nombres descriptivos para los datos de la vela (en español)
      timestamp_apertura = int(candel[0])  # Assuming timestamp is in milliseconds
      precio_apertura = float(candel[1])
      precio_maximo = float(candel[2])
      precio_minimo = float(candel[3])
      precio_cierre = float(candel[4])
      volumen = float(candel[5])
      timestamp_cierre = int(candel[6])  # Assuming timestamp is in milliseconds
      volumen_activo_cotizacion = float(candel[7])
      numero_operaciones = int(candel[8])
      precio_promedio = float(candel[9])
      volumen_cotizacion_promedio = float(candel[10])

      # Crear una característica TensorFlow con nombres claros
      vela_caracteristica = tf.train.Feature(
          float_list=tf.train.FloatList(value=[
              timestamp_apertura,
              precio_apertura,
              precio_maximo,
              precio_minimo,
              precio_cierre,
              volumen,
              timestamp_cierre,
              volumen_activo_cotizacion,
              numero_operaciones,
              precio_promedio,
              volumen_cotizacion_promedio,
          ])
  )

    return vela_caracteristica