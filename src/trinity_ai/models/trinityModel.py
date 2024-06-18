import tensorflow as tf

# Función para inicializar el modelo Trinity con las capas y activaciones especificadas
def initialize_trinity_model():
    trinity_model = tf.keras.Sequential()
    trinity_model.add(tf.keras.layers.Dense(units=182, activation='relu', input_shape=(10,)))
    trinity_model.add(tf.keras.layers.Dense(units=64, activation='relu'))
    trinity_model.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

    # Compilar el modelo
    trinity_model.compile(optimizer='adam', loss='mean_squared_error')

    return trinity_model

# Función para entrenar el modelo Trinity con los datos de entrada y salida
def train_trinity_model(model, input_data, output_data):
    input_tensor = tf.convert_to_tensor(input_data)
    output_tensor = tf.convert_to_tensor(output_data)

    model.fit(input_tensor, output_tensor, epochs=50)

    return model

# Función para realizar predicciones con el modelo Trinity
def predict_with_trinity_model(model, input_data):
    input_tensor = tf.convert_to_tensor(input_data)
    prediction = model.predict(input_tensor)

    return prediction.numpy()

# Exporta las funciones
if __name__ == "__main__":
    initialize_trinity_model()
    train_trinity_model()
    predict_with_trinity_model()
