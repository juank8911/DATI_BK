const { iterateSync } = require('glob');
const binanceApiFutureService = require('../../domain/services/binanceApiFutureService');
const fs = require('fs'); 



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
    return datas // Send the new object
  } catch (error) {
    console.error('Error en el middleware:', error);
    res.status(500).json({ message: 'Internal Server Error' });
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
//  console.log(await candles)
  // Path to the JSON file
  const dataFutFilePath = 'src\\trinity_ai\\models\\dataFut.json';

  // Overwrite the file with the new candles data
  fs.writeFileSync(dataFutFilePath, JSON.stringify(await candles), 'utf8');

  console.log('dataFut.json file created successfully!');

return candles

}

module.exports = {
getExchangeMiddleware,
getCandelsUMFutMiddleware,
}