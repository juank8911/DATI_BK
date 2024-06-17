// src/trainTrinityModel.js

const { Trinity } = require('@tensorflow/tfjs-node');
const { getFuturesTokens, getFutureCandlesticks, getCurrentPrice, getWalletBalance, buyOrder, sellOrder, getFuturesCandlesticksData } = require('./infrastructure/adapters/binanceApiAdapter');
const { prepareData, createModel } = require('./models/trinityModel');
const fs = require('fs'); // Importar el módulo fs para trabajar con archivos

// Función principal para entrenar el modelo de Trinity
async function trainTrinityModel() {
  try {
    // 1. obtener los datos del archivo training.json
    const trainingData = JSON.parse(fs.readFileSync('./infrastructure/datasets/training.json', 'utf8'));

    // 2. reacorrer la lista de tokens
    const profitableTokens = [];
    for (const tokenData of trainingData) {
      const symbol = tokenData.nombre;
      const candlesticks = tokenData.data;

      // 3. evaluar las velas de cada token para encontrar un patron o encontar los
      //    tokens que tengan un cambio de valor de 5% o mayor cada minuto, debera como
      //    las velas son de 30 segundo, ver cuantas veses el token cambia de precio cambiando 
      //    un 5% ya sea de subida o bajada, ver cuantas veces ocurre esto a travez de el tiempo 
      //    y obtener estadisticamente la probabilidad de que esto ocurra nuevamente y en cuanto tiempo 
      //    el porcentaje es mayor al 80% debera agregarlos al archivo
      //    cada que se corra la apliacacion debera solicitar la lista de tokens con vela de dos horas y evaluar
      //    el procentaje de probabiloidad 
      let previousClose = null;
      let significantChanges = 0;
      let totalCandlesticks = 0;
      for (const candlestick of candlesticks) {
        const closePrice = parseFloat(candlestick[4]);
        if (previousClose !== null) {
          const priceChangePercentage = ((closePrice - previousClose) / previousClose) * 100;
          if (Math.abs(priceChangePercentage) >= 5) { // Cambio de valor de 5% o mayor
            significantChanges++;
          }
        }
        previousClose = closePrice;
        totalCandlesticks++;
      }

      // Calcular la probabilidad de cambio significativo
      const probability = (significantChanges / totalCandlesticks) * 100;

      // Agregar el token a la lista de tokens rentables si la probabilidad es mayor al 80%
      if (probability >= 80) {
        profitableTokens.push({
          symbol: symbol,
          probability: probability,
        });
      }
    }

    // 4.  los que cumplan esta caracteristica debe agragr el nombre del simbolo y el porcentaje a una lista
    // 5. guardar la lista en un archivo json con el nombre el valor y la probabiludad en % de que el cambio ocurra
    const profitableTokensFilePath = './infrastructure/datasets/profitableTokens.json';
    fs.writeFileSync(profitableTokensFilePath, JSON.stringify(profitableTokens, null, 2));

    // Obtener el balance de la cuenta
    const balance = await getWalletBalance();
    console.log('Balance de la cuenta:', balance);

    // Inicializar el registro de transacciones
    const transactions = [];

    // Bucle principal para monitorear los tokens y realizar operaciones
    while (true) {
      // Obtener los tokens rentables del archivo JSON
      const profitableTokens = JSON.parse(fs.readFileSync('./infrastructure/datasets/profitableTokens.json', 'utf8'));

      // Evaluar cada token de forma asíncrona
      const operations = profitableTokens.map(async (token) => {
        const symbol = token.symbol;

        // Obtener el precio actual del token
        const currentPrice = await getCurrentPrice(symbol);

        // Evaluar si el token cumple con las condiciones para realizar una operación
        // si tiene certeza de que el precio bajara y generara una ganancia superior al 5% 
        // en futuros puedeo abrir una operacion en corto o si el precio va a subir podra realiar la
        // operacion en largo.
        let shouldShort = false;
        let shouldLong = false;
        // LOGICA DETERMINAR SI REALIZAR OPREAZION EN LARGO O EN CORTO:
        // SEGUN EL JSON profitableTokens el token tiene un valor de probabilidad si este es mayo al 80% y el token 
        // cambia de precio sigiendo un patron en ese momento se debera realizar la operacion
        // si el precio sube la operacion sera en largo, si baja sera en corto 
        const lastCandlesticks = await getFutureCandlesticks(symbol, '1m', 10); // Obtener las últimas 10 velas de 1 minuto
        let previousClose = null;
        let priceChange = 0;
        for (const candlestick of lastCandlesticks) {
          const closePrice = parseFloat(candlestick[4]);
          if (previousClose !== null) {
            priceChange += ((closePrice - previousClose) / previousClose) * 100;
          }
          previousClose = closePrice;
        }
        if (priceChange > 5 && token.probability >= 80) {
          shouldLong = true;
        } else if (priceChange < -5 && token.probability >= 80) {
          shouldShort = true;
        }

        // realizar la operacion en largo o en corto del token y empear a observar su cambio constemente
        // si el precio cambia y se cumple la condicion de ganancia minima estipulada debera cerarr la operacion
        // y guardar el registro de la transaccion y segun el reuñtado cambiar el valor de propabilidad del otro json
        // Registrar la transacción en un json de transacciones y agregar la transaccion a la probabiloidad en el archivo profitableTokens
        if (shouldShort) {
          // Realizar una operación en corto
          // const order = await sellOrder(symbol, 0.7, currentPrice); // Apalancamiento del 70%
          // Simulación de la operación en corto
          transactions.push({
            symbol: symbol,
            type: 'short',
            entryPrice: currentPrice,
            leverage: 0.7,
            timestamp: Date.now(),
            status: 'open',
          });
        } else if (shouldLong) {
          // Realizar una operación en largo
          // const order = await buyOrder(symbol, 0.7, currentPrice); // Apalancamiento del 70%
          // Simulación de la operación en largo
          transactions.push({
            symbol: symbol,
            type: 'long',
            entryPrice: currentPrice,
            leverage: 0.7,
            timestamp: Date.now(),
            status: 'open',
          });
        }

        // Esperar 2 segundos antes de volver a evaluar el token
        await new Promise((resolve) => setTimeout(resolve, 2000));
      }

      // Ejecutar las operaciones de forma asíncrona
      await Promise.all(operations);

      // Evaluar la lista de tokens cada 5 minutos para verificar si el porcentaje de acertividad es superior al 80% en el archivo 
      // profitableTokens Si no es así, volver a evaluar la lista de tokens con velas y regenerar el archivo profitableTokens.json
      // ... (lógica para evaluar la lista de tokens y regenerar el archivo si es necesario) - como cuando se realiza una operacion la 
      // probabiladad se debe agrear al archivo profitableTokens entonses solo debera revisar la probabiladad de los tokens 
      const successfulTransactions = transactions.filter(transaction => transaction.status === 'closed' && transaction.gain > 0);
      const totalTransactions = transactions.length;
      const accuracyPercentage = (successfulTransactions.length / totalTransactions) * 100;
      if (accuracyPercentage < 80) {
        console.log('Porcentaje de acertividad inferior al 80%. Regenerando la lista de tokens...');
        // Regenerar la lista de tokens rentables
        const newProfitableTokens = [];
        for (const tokenData of trainingData) {
          const symbol = tokenData.nombre;
          const candlesticks = tokenData.data;

          // Evaluar las velas de cada token para encontrar un patron o encontar los
          //    tokens que tengan un cambio de valor de 0 5% o mayor cada minuto, 
          let previousClose = null;
          let significantChanges = 0;
          let totalCandlesticks = 0;
          for (const candlestick of candlesticks) {
            const closePrice = parseFloat(candlestick[4]);
            if (previousClose !== null) {
              const priceChangePercentage = ((closePrice - previousClose) / previousClose) * 100;
              if (Math.abs(priceChangePercentage) >= 5) { // Cambio de valor de 5% o mayor
                significantChanges++;
              }
            }
            previousClose = closePrice;
            totalCandlesticks++;
          }

          // Calcular la probabilidad de cambio significativo
          const probability = (significantChanges / totalCandlesticks) * 100;

          // Agregar el token a la lista de tokens rentables si la probabilidad es mayor al 80%
          if (probability >= 80) {
            newProfitableTokens.push({
              symbol: symbol,
              probability: probability,
            });
          }
        }

        // Guardar la nueva lista de tokens en el archivo profitableTokens.json
        fs.writeFileSync(profitableTokensFilePath, JSON.stringify(newProfitableTokens, null, 2));
      }

      // Esperar 5 minutos antes de volver a monitorear los tokens
      await new Promise((resolve) => setTimeout(resolve, 300000));
    }
  } catch (error) {
    console.error('Error al entrenar el modelo de Trinity:', error);
  }
}

// Ejecutar la función principal
trainTrinityModel();

