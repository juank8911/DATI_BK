const { iterateSync } = require('glob');
const binanceApiFutureService = require('../../domain/services/binanceApiFutureService');
const { spawn } = require('child_process');
const fs = require('fs'); 
const { Console } = require('console')
const logger = new Console({ stdout: process.stdout, stderr: process.stderr })
const { UMStream } = require('@binance/futures-connector');



async function getExchangeMiddleware(req, res, next) {
  try {
    let tks=[];
    const data = await binanceApiFutureService.getExchangeInfo(); // Await the promise
    // console.log(data); // Now account will have the exchange information
    let symbols = await data.data
    
    // // Filter symbols based on quoteAsset
    // let filteredSymbols = symbols.symbols.filter(symbol => symbol.quoteAsset === "USDT");
       // Iterate over the symbols array
       for (const symbol of await symbols.symbols) {
        // console.log(symbol); // Access each symbol object
        // Do something with the symbol object, e.g.,
        if (symbol.contractType === 'PERPETUAL')
          {
        // console.log(await symbol.symbol); // Access the symbol name
        // console.log(symbol.quoteAsset); // Access the quote asset
        // console.log(symbol.liquidationFee)
        // console.log(symbol.contractType)

        dts ={name:await symbol.symbol,
              par: symbol.quoteAsset,
              liquidationFee: symbol.liquidationFee,
              contractType: symbol.contractType
        }
        tks.push(await dts)
      }
      }
      // console.log(symbols.symbol)
    let datas = {
      exchangeInfo: await tks,
      staus: 200
    }
    // console.log(datas)
        // Execute the Python script
    return datas // Send the new object
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ message: 'Internal Server Error' });
  }
}

/**
 * Asynchronous middleware function to test the connection status and send the result as JSON.
 * @async
 * @function testConectionMiddleware
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @param {Function} next - The next function in the middleware chain.
 */
async function testConectionMiddleware() {
  try {
    let conn = await binanceApiFutureService.testConectionServ();
    return await conn
}catch(err)
{throw err}
}


async function CreateTFR()
{
  try {
    const pythonProcess = spawn('python', ['./src/trinity_ai/datasets/datasets.py', 'create_TFRecords']);

    // Handle Python script output (optional)
    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python script output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python script error: ${data}`);
    });

    // Wait for the Python script to finish (optional)
    pythonProcess.on('close', (code) => {
      console.log(`Python script exited with code ${code}`);
    });
  } catch (error) {
    
  }
}



async function getCandelsUMFutMiddleware(req,res,next)
{
  // let symbols = await req.data;
  // console.log(req.datas)
  let datas = await req.body
  // console.log(datas)
  // console.log("datas")
const candles = await binanceApiFutureService.getCandles(await datas)
// for(let candel of await candles ){
//   // console.log(candel)
// }
//  console.log(await candles)
  // Path to the JSON file
 

return candles

}

module.exports = {
getExchangeMiddleware,
getCandelsUMFutMiddleware,
testConectionMiddleware,
CreateTFR,
}