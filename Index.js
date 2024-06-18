// src/index.js

// Importa los módulos necesarios
const express = require('express');
const bodyParser = require('body-parser')
const { spawn } = require('child_process');
const { getFuturesTokenprMiddleware, getFuturesCandlesticksDataMiddleware } = require('./src/infrastructure/adapters/binanceApiAdapter');
//importar TensorFlow para node     
// Crea una instancia de Express
const app = express();  
const port = 3000;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));
// Ruta de prueba
app.get('/', (req, res) => {

  res.send('¡Bienvenido a la aplicación DATI!'); 
});

app.get('/trainData', async (req, res) => {
    try {
      // Llama al middleware para obtener datos de velas y crear archivos de entrenamiento
      await getFuturesCandlesticksDataMiddleware(req, res, () => {}); 
  
      // Responde al cliente con un mensaje de éxito
      res.json({ message: 'Datos de entrenamiento creados correctamente.' });
    } catch (error) {
      console.error('Error al crear datos de entrenamiento:', error);
      res.status(500).json({ error: 'Error al crear datos de entrenamiento.' });
    }
  });

// Función para probar la conexión con Binance al iniciar la aplicación
async function testBinanceConnection() {
    try {
      // Create a mock request and response object
      const req = {}; // Empty object for the request
      const res = {
        json: (data) => {
          console.log('Conexión exitosa con Binance. Lista de tokens futuros:');
          console.log(data.data.symbols[0]);
        },
        status: (code) => {
          return {
            json: (error) => {
              console.error('Error al probar la conexión con Binance:', error);
              process.exit(1); // Cierra la aplicación con código de error
            }
          };
        }
      };
      const next = () => {}; // Empty function for next
  
      // Call the middleware function
      await getFuturesTokenprMiddleware(req, res, next);
    } catch (error) {
      console.error('Error al probar la conexión con Binance:', error);
      process.exit(1); // Cierra la aplicación con código de error
    }
  }

  // Función para inicializar la AI de Python
async function initializeAI() {
    try {
      // Ejecutar el script de Python para inicializar la AI
      const pythonProcess = spawn('python', ['./src/run_trinity_model.py']);
      // Manejar la salida del script de Python
             // Handle output from the Python script
             pythonProcess.stdout.on('data', (data) => {
              console.log(`Salida del script de Python: ${data}`);
          });
  
          // Handle errors from the Python script
          pythonProcess.stderr.on('data', (data) => {
              console.error(`Error en el script de Python: ${data}`);
              // You can choose to handle the error differently here, 
              // for example, by logging it to a file or sending an alert.
              // process.exit(1); // Exit with an error code
          });
  
          // Wait for the Python script to finish
          await new Promise((resolve) => pythonProcess.on('close', resolve));
          
      pythonProcess.stderr.on('data', (data) => {
        console.error(`Error en el script de Python: ${data}`);
        process.exit(1);
      });
  
      // Esperar a que el script de Python termine
      await new Promise((resolve) => pythonProcess.on('close', resolve));
  
      console.log('AI de Python inicializada correctamente.');
    } catch (error) {
      console.error('Error al inicializar la AI de Python:', error);
      process.exit(1); // Cierra la aplicación con código de error
    }
  }

// Inicia el servidor y prueba la conexión con Binance
app.listen(port, async () => {
    // await initializeAI();
    await testBinanceConnection();
    console.log(`La aplicación DATI está corriendo en http://localhost:${port}`);
});
