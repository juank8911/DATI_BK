// src/infrastructure/adapters/binanceApiAdapter.js

// src/infrastructure/adapters/binanceApiAdapter.js

const axios = require('axios');
const crypto = require('crypto');
const fs = require('fs'); // Importar el módulo fs para trabajar con archivos
const config = require('../../config'); // Importar el archivo de configuración


// Función para obtener las velas de los tokens futuros y guardarlas en un archivo JSON
async function getFuturesCandlesticksData() {
  try {
    const futuresTokens = await getFuturesTokens();
    const candlesticksData = [];

    for (const token of futuresTokens) {
      const symbol = token.symbol;
      const candlesticks = await getFutureCandlesticks(symbol, '30s', 120); // 30 segundos, 3 horas atrás (120 velas)
      candlesticksData.push({
        nombre: symbol,
        data: candlesticks,
      });
    }

    // Guardar el JSON en el archivo training.json
    const filePath = './infrastructure/datasets/training.json';
    fs.writeFileSync(filePath, JSON.stringify(candlesticksData, null, 2)); // Guardar con formato

    console.log('Datos de velas de tokens futuros guardados en:', filePath);
    return candlesticksData;
  } catch (error) {
    console.error('Error al obtener las velas de los tokens futuros:', error);
    return null;
  }
}


// Función para obtener la lista de tokens futuros
async function getFuturesTokens() {
  try {
    const response = await axios.get(`${config.BINANCE_API_URL}exchangeInfo`, {
      headers: {
        'X-MBX-APIKEY': config.API_KEY,
      },
    });
    return response.data.symbols.filter((symbol) => symbol.contractType === 'PERPETUAL');
  } catch (error) {
    console.error('Error al obtener la lista de tokens futuros:', error);
    return null;
  }
}

// Función para obtener datos históricos de velas de un token futuro
async function getFutureCandlesticks(symbol, interval, limit) {
  try {
    const response = await axios.get(
      `${config.BINANCE_API_URL}klines?symbol=${symbol}&interval=${interval}&limit=${limit}`,
      {
        headers: {
          'X-MBX-APIKEY': config.API_KEY,
        },
      },
    );
    return response.data;
  } catch (error) {
    console.error('Error al obtener datos históricos de velas del token futuro:', error);
    return null;
  }
}

// Función para obtener el precio actual de un símbolo
async function getCurrentPrice(symbol) {
  try {
    const response = await axios.get(`${config.BINANCE_API_URL}ticker/price?symbol=${symbol}`, {
      headers: {
        'X-MBX-APIKEY': config.API_KEY,
      },
    });
    return parseFloat(response.data.price);
  } catch (error) {
    console.error('Error al obtener el precio actual del símbolo:', error);
    return null;
  }
}

// Función para obtener la información de un símbolo
async function getSymbolInfo(symbol) {
  try {
    const response = await axios.get(`${config.BINANCE_API_URL}exchangeInfo`, {
      headers: {
        'X-MBX-APIKEY': config.API_KEY,
      },
    });
    return response.data.symbols.find((s) => s.symbol === symbol);
  } catch (error) {
    console.error('Error al obtener la información del símbolo:', error);
    return null;
  }
}

// Función para obtener el balance de la cuenta
async function getWalletBalance() {
  try {
    const timestamp = Date.now();
    const signature = generateSignature('GET', '/fapi/v1/account', timestamp, '');

    const response = await axios.get(`${config.BINANCE_API_URL}account`, {
      headers: {
        'X-MBX-APIKEY': config.API_KEY,
        'X-MBX-TIMESTAMP': timestamp,
        'X-MBX-SIGNATURE': signature,
      },
    });
    return response.data.assets;
  } catch (error) {
    console.error('Error al obtener el balance de la cuenta:', error);
    return null;
  }
}

// Función para realizar una operación de compra
async function buyOrder(symbol, leverage, price) {
  try {
    const timestamp = Date.now();
    const signature = generateSignature(
      'POST',
      '/fapi/v1/orders',
      timestamp,
      `symbol=${symbol}&side=BUY&type=MARKET&quantity=1&leverage=${leverage}&price=${price}`,
    );

    const response = await axios.post(
      `${config.BINANCE_API_URL}orders`,
      {
        symbol,
        side: 'BUY',
        type: 'MARKET',
        quantity: 1,
        leverage,
        price,
      },
      {
        headers: {
          'X-MBX-APIKEY': config.API_KEY,
          'X-MBX-TIMESTAMP': timestamp,
          'X-MBX-SIGNATURE': signature,
        },
      },
    );
    return response.data;
  } catch (error) {
    console.error('Error al realizar la operación de compra:', error);
    return null;
  }
}

// Función para realizar una operación de venta
async function sellOrder(symbol, leverage, price) {
  try {
    const timestamp = Date.now();
    const signature = generateSignature(
      'POST',
      '/fapi/v1/orders',
      timestamp,
      `symbol=${symbol}&side=SELL&type=MARKET&quantity=1&leverage=${leverage}&price=${price}`,
    );

    const response = await axios.post(
      `${config.BINANCE_API_URL}orders`,
      {
        symbol,
        side: 'SELL',
        type: 'MARKET',
        quantity: 1,
        leverage,
        price,
      },
      {
        headers: {
          'X-MBX-APIKEY': config.API_KEY,
          'X-MBX-TIMESTAMP': timestamp,
          'X-MBX-SIGNATURE': signature,
        },
      },
    );
    return response.data;
  } catch (error) {
    console.error('Error al realizar la operación de venta:', error);
    return null;
  }
}

// Función para generar la firma de la solicitud
function generateSignature(method, path, timestamp, query) {
  const signature = crypto
    .createHmac('sha256', config.SECRET_KEY)
    .update(`${method}\n${path}\n${timestamp}\n${query}`)
    .digest('hex');
  return signature;
}

module.exports = {
  getFuturesCandlesticksData,
  getFuturesTokens,
  getFutureCandlesticks,
  getCurrentPrice,
  getSymbolInfo,
  getWalletBalance,
  buyOrder,
  sellOrder,
};

