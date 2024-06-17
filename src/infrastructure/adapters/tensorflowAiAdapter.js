// src/infrastructure/adapters/tensorflowAiAdapter.js

const tf = require('@tensorflow/tfjs-node');

// Función para cargar un modelo de IA pre-entrenado
async function loadModel(modelPath) {
  try {
    const model = await tf.loadLayersModel(`file://${modelPath}/model.json`);
    return model;
  } catch (error) {
    console.error('Error al cargar el modelo de IA:', error);
    return null;
  }
}

// Función para realizar una predicción con el modelo de IA
async function predict(model, inputData) {
  try {
    const inputTensor = tf.tensor2d(inputData);
    const prediction = model.predict(inputTensor);
    return prediction.dataSync();
  } catch (error) {
    console.error('Error al realizar la predicción:', error);
    return null;
  }
}

module.exports = {
  loadModel,
  predict,
};
