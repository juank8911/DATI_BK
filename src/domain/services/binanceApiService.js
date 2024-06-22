// src/infrastructure/adapters/binanceApiAdapter.js

// src/infrastructure/adapters/binanceApiAdapter.js

const axios = require('axios');
const crypto = require('crypto');
const { Console } = require('console')
const fs = require('fs'); // Importar el módulo fs para trabajar con archivos
const config = require('../../config'); // Importar el archivo de configuración
const { CMFutures, CMStream} = require("@binance/futures-connector");
const { Spot } = require('@binance/connector')
const logger = new Console({ stdout: process.stdout, stderr: process.stderr })

// Función para obtener las velas de los tokens futuros y guardarlas en un archivo JSON
async function getFuturesCandlesticksData() {
  let i = 0;
  try {
     futuresTokens = await getFuturesTokenpr();
    candlesticksData = [];
    console.log(futuresTokensnode);
    futuresTokens = futuresTokens.data
    for (let token of futuresTokens) {
      let {symbol} = token;
      let candlesticks = await getFutureCandlesticks(symbol, '1m', 240,'2024-06-18T18:00:00','2024-06-18T22:00:00'); // 30 segundos, 3 horas atrás (120 velas)
      // console.log(candlesticks)
      candlesticksData.push({
        nombre: symbol,
        data: candlesticks,
      });
      console.log(i +' de '+ futuresTokens.length);
      i++;
    }

    // // Guardar el JSON en el archivo training.json
    const filePath = './src/trinity_ai/datasets/training1.json';
    // if (fs.existsSync(filePath)) {
    //   // Si existe, borrar el archivo
    //   fs.unlinkSync(filePath);
    //   console.log('Archivo training.json existente borrado.');
    // }
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
    const response = await axios.get(`${config.BINANCE_API_URL1}exchangeInfo`, {
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
async function getFutureCandlesticks(symbol, interval, limit,Fstart,Fend) {
  try {
    Sdate = await dateToEpochMilliseconds(Fstart)
    Fdate = await dateToEpochMilliseconds(Fend)
    // console.log(config.BINANCE_API_URL1)

    const response = await axios.get(
      `${config.BINANCE_API_URL1}klines?symbol=${symbol}&interval=${interval}&startTime=${Sdate}&endTime=${Fdate}&timeZone=-5&limit=${limit}`,
    );
    return response
  } catch (error) {
    throw('Error al obtener datos históricos de velas del token futuro:', error);
    // return null;
  }
}

async function dateToEpochMilliseconds(dateString) {
  // 1. Create a Date object from the input string
  const date = new Date(dateString);

  // 2. Get the number of milliseconds since the Unix epoch
  return date.getTime();
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
  return crypto
      .createHmac('sha256', config.SECRET_KEY)
      .update(`${method}\n${path}\n${timestamp}\n${query}`)
      .digest('hex');
}


async function getFuturesTokenpr() {
  const cmFuturesClient = new CMFutures('', '', {
    baseURL: config.BINANCE_API_URL
  });

  try {
    return await cmFuturesClient.getExchangeInfo(); // Return the result
  } catch (err) {
    throw err; // Re-throw the error
  }
}

async function getAllMarcketTickets()
{
  const callbacks = {
    open: () => logger.debug('Connected with Websocket server'),
    close: () => logger.debug('Disconnected with Websocket server'),
    message: (data) => logger.info(data)
  }
  
  const websocketStreamClient = new CMStream({ logger, callbacks })
  
  websocketStreamClient.allMarketTickersStreams()
  
  setTimeout(() => websocketStreamClient.disconnect(), 6000)
}

async function getBalance()
{
  const cmFuturesClient = new CMFutures(config.API_KEY, config.SECRET_KEY, {
    baseURL: config.BINANCE_API_URL
  })
  
  cmFuturesClient
    .getFuturesAccountBalance()
    .then((response) => {console.log(response); return response.data})
    .catch(console.error)
}

async function getAccountStatus()
{
const apiKey = config.API_KEY
const apiSecret = config.API_KEY
const client = new Spot(apiKey, apiSecret)

client.accountStatus()
  .then(response => {client.logger.log(response.data); return response})
  .catch(error => client.logger.error(error))
}


  
  // cmFuturesClient
  //   .getMarkPriceKlines('BTCUSD_PERP', '1m')
  //   .then((response) => console.log(response))
  //   .catch(console.error)



module.exports = {
  getFuturesCandlesticksData,
  getFuturesTokens,
  getFuturesTokenpr,
  getFutureCandlesticks,
  getCurrentPrice,
  getAllMarcketTickets,
  getSymbolInfo,
  getAccountStatus,
  getWalletBalance,
  buyOrder,
  sellOrder,
  getBalance,
};

