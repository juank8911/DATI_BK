// src/infrastructure/training/trainTrinityModel.js

const trinityModel = require('../models/trinityModel');
const tf = require('@tensorflow/tfjs-node');

// Carga los datos de entrenamiento
const trainingData = require('../datasets/training.json');
const { inputs, labels } = tf.tidy(() => {
    const inputsTensor = tf.tensor2d(trainingData.inputs);
    const labelsTensor = tf.tensor2d(trainingData.labels);
    return { inputs: inputsTensor, labels: labelsTensor };
});

// Entrena el modelo
trinityModel.fit(inputs, labels, { epochs: 50 })
    .then(() => {
        console.log('Entrenamiento completado.');
    })
    .catch(error => {
        console.error('Error durante el entrenamiento:', error);
    });
