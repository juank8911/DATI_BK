// src/infrastructure/training/evaluateTrinityModel.js

const trinityModel = require('../models/trinityModel');
const tf = require('@tensorflow/tfjs-node');

// Carga los datos de prueba
const testData = require('../datasets/test.json');
const { inputs, labels } = tf.tidy(() => {
    const inputsTensor = tf.tensor2d(testData.inputs);
    const labelsTensor = tf.tensor2d(testData.labels);
    return { inputs: inputsTensor, labels: labelsTensor };
});

// Evalúa el modelo con los datos de prueba
trinityModel.evaluate(inputs, labels)
    .then(result => {
        console.log('Evaluación del modelo:', result.dataSync());
    })
    .catch(error => {
        console.error('Error durante la evaluación del modelo:', error);
    });
