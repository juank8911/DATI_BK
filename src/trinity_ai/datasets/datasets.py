import json
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

# file_path = 'J:\ProyectosCriptoMon\DATI\src\trinity_ai\datasets\dataFut.json'



async def load_data_from_tfrecords(tfrecords_file_path='J:\ProyectosCriptoMon\DATI\src\\trinity_ai\datasets\\training.tfrecord'):
  """
  Loads training data from a TFRecords file.

  Args:
      tfrecords_file_path (str): Path to the TFRecords file.

  Returns:
      list: List of dictionaries, where each dictionary represents a training example in TensorFlow format.
  """

  tf_data = []
  for example in tf.data.TFRecordDataset(tfrecords_file_path):
    features = tf.io.parse_single_example(
        example,
        features={
            'name': tf.io.FixedLenFeature([], tf.string),
            'data': tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),  # Parse 'data' as a sequence of floats
            'promedio': tf.io.FixedLenFeature([], tf.string),
            'logro': tf.io.FixedLenFeature([], tf.int64),
            'ema': tf.io.FixedLenFeature([], tf.float32),
            'pft': tf.io.FixedLenFeature([], tf.float32),
            'SMA': tf.io.FixedLenFeature([], tf.float32),
        }
    )

    # Create a dictionary with TensorFlow tensors
    tf_symbol = {
        'name': features['name'],
        'data': features['data'],  # 'data' is already a TensorFlow tensor
        'promedio': features['promedio'],
        'logro': features['logro'],
        'ema': features['ema'],
        'pft': features['pft'],
        'SMA': features['SMA'],
    }

    tf_data.append(tf_symbol)

  return tf_data

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
                'data': data_klines,
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


def load_training_data(file_path='J:\ProyectosCriptoMon\DATI\src\trinity_ai\datasets\dataFut.json'):
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
      print('1N')
      raise FileNotFoundError(f"File not found: {file_path}")
    # Open the file and load JSON data
    with open(file_path) as f:
      datas = json.load(f)
      print('1S')
    # Process each symbol's data
    tf_data = []
    for symbol_data in datas:
      symbol_dict = symbol_data['symbol']
      print('1F')
      # Extract necessary information
      name = symbol_dict['name']
      data_klines = symbol_dict['data'][0]  # Assuming the first list contains kline data
      print(symbol_dict['data'])
      velas = []
      # Separate and convert data_klines (assuming specific structure)
      # for vela in data_klines:
      vela = data_klines
      timestamps= tf.convert_to_tensor(vela['timestamp_apertura'], dtype=tf.float64),
      precio_apertura = float(vela['precio_apertura'])
      precio_apertura = tf.convert_to_tensor(precio_apertura, dtype=tf.float64)
      precio_maximo = tf.convert_to_tensor(vela['precio_maximo'], dtype=tf.float64),
      precio_minimo= tf.convert_to_tensor(vela['precio_minimo'], dtype=tf.float64),
      precio_cierre = tf.convert_to_tensor(vela['precio_cierre'], dtype=tf.float64),
      volumen = tf.convert_to_tensor(vela['volumen'], dtype=tf.float64),
      timestamp_cierre = tf.convert_to_tensor(vela['timestamp_cierre'], dtype=tf.float64),
      volumen_activo_cotizacion = tf.convert_to_tensor(vela['volumen_activo_cotizacion'], dtype=tf.float64),
      numero_operaciones = tf.convert_to_tensor(vela['numero_operaciones'], dtype=tf.int64),
      precio_promedio = tf.convert_to_tensor(vela['precio_promedio'], dtype=tf.float64),
      volumen_cotizacion_promedio = tf.convert_to_tensor(vela['volumen_cotizacion_promedio'], dtype=tf.float64),
      fluctua = tf.convert_to_tensor(vela['fluctua'], dtype=tf.float64),
        
     

      # Create a dictionary with TensorFlow tensors
      tf_symbol = {
          'name': tf.convert_to_tensor(name, dtype=tf.string),
          'data': tf.stack([timestamps,
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
                            fluctua,]),  # Stack timestamps and numeric values (assuming consistent structure)
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
  """Converts dataFut.json to TFRecords and saves it to src\\trinity_ai\datasets."""

  # Path to the JSON file (corrected path)
  json_file_path = 'J:\ProyectosCriptoMon\DATI\src\\trinity_ai\datasets\dataFut.json'

  # Path to save the TFRecords file
  tfrecords_file_path = 'J:\ProyectosCriptoMon\DATI\src\\trinity_ai\datasets\\training.tfrecord'

  # Load the JSON data
  with open(json_file_path, 'r') as f:
    data = json.load(f)

  # Create a TFRecord writer
  with tf.io.TFRecordWriter(tfrecords_file_path) as writer:
    for symbol_data in data:
      symbol = symbol_data['symbol']
      candles = symbol_data['symbol']['data']
      # for symbol in symbol_data['symbol']:
      print(symbol['name'])
      print('----------------------------------------------------------------------------')
      # Convert candle data to features using the function
      features = {
          'name': tf.train.Feature(bytes_list=tf.train.BytesList(value=[symbol['promedio'].encode()])),
          'data': create_candlestick_feature(candles),  # Use the function here
          'promedio': tf.train.Feature(bytes_list=tf.train.BytesList(value=[symbol['promedio'].encode()])),
          'logro': tf.train.Feature(int64_list=tf.train.Int64List(value=[symbol['logro']])),
          'ema': tf.train.Feature(float_list=tf.train.FloatList(value=[float(symbol['ema'])])),
          'pft': tf.train.Feature(float_list=tf.train.FloatList(value=[float(symbol['pft'])])),
          'SMA': tf.train.Feature(float_list=tf.train.FloatList(value=[float(symbol['SMA'])])),
      }
      print(features)
       # Create a separate Example object for each symbol data
    example = tf.train.Example(features=features)

        # Write the example to the TFRecords file
    writer.write(example.SerializeToString())

  print(f'TFRecords file created successfully at: {tfrecords_file_path}')
  
  
def create_candlestick_feature(candles):
  # sourcery skip: merge-list-appends-into-extend
    """
    Convierte una lista de datos de una vela (candlestick) en una característica TensorFlow.

    Args:
      candle (list): Lista que contiene los datos de la vela.

    Returns:
      tf.train.Feature: Una característica TensorFlow con los datos de la vela.
    """
    vela_caracteristica = {} # Initialize an empty list to store candle data
    for candel in candles:
      timestamp = float(candel['timestamp_apertura'])  # Assuming timestamp is in milliseconds
      precio_apertura = float(candel['precio_apertura'])
      precio_maximo = float(candel['precio_maximo'])
      precio_minimo = float(candel['precio_minimo'])
      precio_cierre = float(candel['precio_cierre'])
      volumen = float(candel['volumen'])
      timestamp_cierre = int(candel['timestamp_cierre'])  # Assuming timestamp is in milliseconds
      volumen_activo_cotizacion = float(candel['timestamp_cierre'])
      numero_operaciones = int(candel['numero_operaciones'])
      precio_promedio = float(candel['precio_promedio'])
      volumen_cotizacion_promedio = float(candel['volumen_cotizacion_promedio'])
      fluctua = float(candel['fluctua'])

        # Append candle data to the list

      
      vela_caracteristica = {
          "timestamp": timestamp,
          "precio_apertura": precio_apertura,
          "precio_maximo": precio_maximo,
          "precio_minimo": precio_minimo,
          "precio_cierre": precio_cierre,
          "volumen": volumen,
          "timestamp_cierre": timestamp_cierre,
          "volumen_activo_cotizacion": volumen_activo_cotizacion,
          "numero_operaciones": numero_operaciones,
          "precio_promedio": precio_promedio,
          "volumen_cotizacion_promedio": volumen_cotizacion_promedio,
          "fluctua": fluctua,
      }

        # Create a TensorFlow Feature object
      vela_feature = tf.train.Feature(
        float_list=tf.train.FloatList(value=vela_caracteristica.values())
      )
    return vela_caracteristica
  
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'create_TFRecords':
        create_TFRecords()