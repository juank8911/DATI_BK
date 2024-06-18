// src/index.js

// Importa los módulos necesarios
const express = require('express');
const { getFuturesTokens } = require('./src/infrastructure/adapters/binanceApiAdapter');
const {initializeTrinityModel} = require('./src/infrastructure/adapters/models/trinityModel')
//importar TensorFlow para node     
// Crea una instancia de Express
const app = express();
const port = 3000;

// Ruta de prueba
app.get('/', (req, res) => {
  res.send('¡Bienvenido a la aplicación DATI!');
});

// Función para probar la conexión con Binance al iniciar la aplicación
async function testBinanceConnection() {
    try {
        const futuresTokens = await getFuturesTokens();
        if (futuresTokens) {
            console.log('Conexión exitosa con Binance. Lista de tokens futuros:');
            console.log(futuresTokens);
        } else {
            console.error('Error: No se pudo obtener la lista de tokens futuros de Binance.');
            process.exit(1); // Cierra la aplicación con código de error
        }
    } catch (error) {
        console.error('Error al probar la conexión con Binance:', error);
        process.exit(1); // Cierra la aplicación con código de error
    }
}

// Inicia el servidor y prueba la conexión con Binance
app.listen(port, async () => {
    console.log(`La aplicación DATI está corriendo en http://localhost:${port}`);
    await testBinanceConnection();
});
