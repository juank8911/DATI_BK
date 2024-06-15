// src/infrastructure/adapters/models/trinityModel.js

const tf = require('@tensorflow/tfjs-node');

// Función para inicializar el modelo Trinity con las capas y activaciones especificadas
async function initializeTrinityModel() {
    const trinityModel = tf.sequential();
    trinityModel.add(tf.layers.dense({ units: 182, activation: 'relu', inputShape: [10] }));
    trinityModel.add(tf.layers.dense({ units: 64, activation: 'relu' }));
    trinityModel.add(tf.layers.dense({ units: 1, activation: 'sigmoid' }));

    // Compilar el modelo
    trinityModel.compile({ optimizer: 'adam', loss: 'meanSquaredError' });

    return trinityModel;
}

// Función para entrenar el modelo Trinity con los datos de entrada y salida
async function trainTrinityModel(model, inputData, outputData) {
    const inputTensor = tf.tensor2d(inputData);
    const outputTensor = tf.tensor2d(outputData);

    await model.fit(inputTensor, outputTensor, { epochs: 50 });

    return model;
}

// Función para realizar predicciones con el modelo Trinity
async function predictWithTrinityModel(model, inputData) {
    const inputTensor = tf.tensor2d(inputData);
    const prediction = model.predict(inputTensor);

    return prediction.dataSync();
}

module.exports = {
    initializeTrinityModel,
    trainTrinityModel,
    predictWithTrinityModel
};
