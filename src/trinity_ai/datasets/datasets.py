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

def load_training_data(file_path='.\training.tfrecord'):
    """
    Carga los datos de entrenamiento desde un archivo TFRecord.

    Args:
        file_path (str): La ruta al archivo TFRecord.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un ejemplo de entrenamiento.
    """
    try:
        # Crea un dataset de TFRecord
        dataset = tf.data.TFRecordDataset(file_path)

        # Define las características del dataset
        feature_description = {
            'name': tf.io.FixedLenFeature([], tf.string),
            'data': tf.io.FixedLenFeature([8], tf.float32),
            'promedio': tf.io.FixedLenFeature([], tf.string),
            'logro': tf.io.FixedLenFeature([], tf.int64),
            'ema': tf.io.FixedLenFeature([], tf.float32),
            'pft': tf.io.FixedLenFeature([], tf.float32),
            'SMA': tf.io.FixedLenFeature([], tf.float32),
        }

        # Define una función para parsear los ejemplos del dataset
        def _parse_function(example_proto):
            # Parse the input tf.train.Example proto
            example = tf.io.parse_single_example(example_proto, feature_description)

            # Decode the features
            name = tf.io.decode_raw(example['name'], tf.string)
            data = example['data']
            promedio = tf.io.decode_raw(example['promedio'], tf.string)
            logro = example['logro']
            ema = example['ema']
            pft = example['pft']
            SMA = example['SMA']

            # Convert the features to a dictionary
            features = {
                'symbol': symbol.numpy().decode('utf-8'),
                'data': data.numpy(),
                'promedio': promedio.numpy().decode('utf-8'),
                'logro': logro.numpy(),
                'ema': ema.numpy(),
                'pft': pft.numpy(),
                'SMA': SMA.numpy(),
            }

            return features

        # Aplica la función de parseo al dataset
        parsed_dataset = dataset.map(_parse_function)

        # Convierte el dataset a una lista de diccionarios
        training_data = list(parsed_dataset.as_numpy_iterator())

        return training_data

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return None
    except tf.errors.InvalidArgumentError:
        print(f"Error: El archivo '{file_path}' no es un archivo TFRecord válido.")
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
      candles = symbol_data['data']

      for candle in candles:
        # Convert candle data to features
        features = {
          'symbol': tf.train.Feature(bytes_list=tf.train.BytesList(value=[symbol['name'].encode()])),
          'data': tf.train.Feature(float_list=tf.train.FloatList(value=[float(x) for x in candle])),  
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


    
