// src/infrastructure/adapters/binanceApiAdapter.js

const BinanceApiService = require('../../domain/services/binanceApiService');

// Middleware para obtener datos de velas de tokens futuros
async function getFuturesCandlesticksDataMiddleware(req, res, next) {
  try {
    const candlesticksData = await BinanceApiService.getFuturesCandlesticksData();
    res.json(candlesticksData);
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al obtener datos de velas' });
  }
}

// Middleware para obtener la lista de tokens futuros
async function getFuturesTokensMiddleware(req, res, next) {
  try {
    const futuresTokens = await BinanceApiService.getFuturesTokens();
    res.json(futuresTokens);
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al obtener la lista de tokens futuros' });
  }
}

// Middleware para obtener datos históricos de velas de un token futuro
async function getFutureCandlesticksMiddleware(req, res, next) {
  try {
    const { symbol, interval, limit } = req.query;
    const candlesticks = await BinanceApiService.getFutureCandlesticks(symbol, interval, limit);
    res.json(candlesticks);
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al obtener datos históricos de velas' });
  }
}

// Middleware para obtener el precio actual de un símbolo
async function getCurrentPriceMiddleware(req, res, next) {
  try {
    const { symbol } = req.query;
    const price = await BinanceApiService.getCurrentPrice(symbol);
    res.json({ price });
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al obtener el precio actual' });
  }
}

// Middleware para obtener la información de un símbolo
async function getSymbolInfoMiddleware(req, res, next) {
  try {
    const { symbol } = req.query;
    const symbolInfo = await BinanceApiService.getSymbolInfo(symbol);
    res.json(symbolInfo);
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al obtener la información del símbolo' });
  }
}

// Middleware para obtener el balance de la cuenta
async function getWalletBalanceMiddleware(req, res, next) {
  try {
    const balance = await BinanceApiService.getWalletBalance();
    res.json(balance);
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al obtener el balance de la cuenta' });
  }
}

// Middleware para realizar una operación de compra
async function buyOrderMiddleware(req, res, next) {
  try {
    const { symbol, leverage, price } = req.body;
    const order = await BinanceApiService.buyOrder(symbol, leverage, price);
    res.json(order);
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al realizar la operación de compra' });
  }
}

// Middleware para realizar una operación de venta
async function sellOrderMiddleware(req, res, next) {
  try {
    const { symbol, leverage, price } = req.body;
    const order = await BinanceApiService.sellOrder(symbol, leverage, price);
    res.json(order);
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ error: 'Error al realizar la operación de venta' });
  }

}

async function getFuturesTokenprMiddleware(req, res, next) {
  try {
    const info = await BinanceApiService.getFuturesTokenpr();
    // console.log(info.data);
    res.json(info); // Send the info as JSON response
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Error al obtener lista de futuros' });
  }
}



module.exports = {
  getFuturesCandlesticksDataMiddleware,
  getFuturesTokensMiddleware,
  getFuturesTokenprMiddleware,
  getFutureCandlesticksMiddleware,
  getCurrentPriceMiddleware,
  getSymbolInfoMiddleware,
  getWalletBalanceMiddleware,
  buyOrderMiddleware,
  sellOrderMiddleware,
};

