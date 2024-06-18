// src/infrastructure/adapters/config.js

const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
  API_KEY: 'uUWodyz9ciDyqZwTSkHPTjuazT5p4lzAKGwsEmLpTGwav3ixI0eJ6v6HKe9voY2J',
  SECRET_KEY: 'UYAX5ECm6EvU7wJ3zPGDYN5VecqpHC7TMHn25ciM505FgrXmD1BpUFBZO2ur23nc', // Reemplaza con tu clave secreta de Binance
  BINANCE_API_URL1:'https://api.binance.com',
  BINANCE_API_URL: isProduction
    ? 'https://fapi.binance.com' // Red real de Binance
    : 'https://testnet.binancefuture.com', // Red de pruebas de Binance
};