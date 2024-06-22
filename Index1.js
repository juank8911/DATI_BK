const express = require('express');
const ws = require('express-ws'); // Replace with your actual implementation

const logger = console; // Replace with your preferred logging library (e.g., pino)

const wsURL = 'wss://fstream.binance.com'; // Main endpoint
// const wss = new ws.Server({ server: app })

const app = express();
ws(app)
function getAllMarkPrices() {
  const websocket = new ws(wsURL);

  websocket.on('open', () => {
    logger.debug('Connected to Binance Futures WebSocket');

    // Subscribe to markPrice stream for ALL markets
    const subscription = {
      method: 'SUBSCRIBE',
      params: ['!markPrice@arr@1s'], // Combined subscription for mark price data every second
    };
    websocket.send(JSON.stringify(subscription));
  });

  websocket.on('message', (data) => {
    try {
      const parsedData = JSON.parse(data);

      if (parsedData.stream === '!markPrice@arr') {
        const markPrices = parsedData.data;
        console
        markPrices.forEach((markPriceData) => {
          const symbol = markPriceData.s;
          const markPrice = markPriceData.p;
          const fundingRate = markPriceData.r;
          const nextFundingTime = markPriceData.T;

          logger.info(`Mark Price Update for ${symbol}:`);
          logger.info(`  Mark Price: ${markPrice}`);
          logger.info(`  Funding Rate: ${fundingRate}`);
          logger.info(`  Next Funding Time: ${nextFundingTime}`);

          // You can process the mark price data further for your application needs
        });
      } else {
        logger.debug('Received non-relevant message:', data);
      }
    } catch (error) {
      logger.error('Error parsing data:', error);
    }
  });

  websocket.on('error', (error) => {
    logger.error('WebSocket connection error:', error);
    // Handle connection errors (optional: reconnect logic)
  });

  websocket.on('close', () => {
    logger.debug('Disconnected from Binance Futures WebSocket');
  });
}


app.ws('/ws', () => {
  getAllMarkPrices();
});

// Serve static files (replace with your actual path)
app.use(express.static(__dirname + '/public'));

const port = 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
