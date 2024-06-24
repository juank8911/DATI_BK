const crypto = require('crypto');
const { Console } = require('console')
const fs = require('fs'); // Importar el módulo fs para trabajar con archivos
const config = require('../../config'); // Importar el archivo de configuración
const { CMFutures, UMFutures} = require("@binance/futures-connector");
const { UMStream } = require('@binance/futures-connector'); 

const { Spot } = require('@binance/connector')



const cmFuturesClient = new CMFutures("","", {
  baseURL: config.BINACM_API_URL
})

const UMFuturesClient = new UMFutures("","",{
    baseURL: config.BINAFM_API_URL
})







/**
 * Asynchronous function to ping the UMFuturesClient.
 * @async
 * @function testConectionServ
 * @returns {Promise} A promise that resolves with the ping response.
 */
async function testConectionServ() {
  return await UMFuturesClient.ping();
}

// main function (Index.js)




async function getExchangeInfo() {
  return await UMFuturesClient.getExchangeInfo() // Directly return the resolved data
}


async function getCandles(datas) {

  const candles = [];

  const end = Date.now();
  const size = 240; // Número de velas que deseas recuperar
  const now = Date.now(); // Get the current timestamp in milliseconds
  const interval = "1m";
  // Define the number of hours to subtract
  const hoursToSubtract = 3; // Replace with the desired number of hours
  // Convert hours to milliseconds
  const hoursInMilliseconds = hoursToSubtract * 3600000; // 1 hour = 3600 seconds * 1000 milliseconds/second
  // Calculate the start timestamp
  const start = now - hoursInMilliseconds;
  // for(let symbol of await datas)
  //   {
  //     console.log(symbol.name,interval,start,end,size)
  //     let velasSymbl = await UMFuturesClient.getKlines(symbol.name, interval, start, end, size)
  //     // console.log( await velasSymbl)
  //     candles.push({ symbol, data: await velasSymbl });
  //     console.log(datas.length())
  //   }
  // await Promise.all(datas.map(async (symbol) => {
  //   try {
  //     let velasSymbl = await UMFuturesClient.getKlines(symbol.name, interval, start, end, size);
  //     // console.log(velasSymbl.data)
  //      sumaPo = 0;
  //      tamaño = Object.keys(velasSymbl.data).length
  //      logro = 0
  //     console.log(tamaño)
  //     let modifiedCandles = await velasSymbl.data.map((vela) => {
  //       porcambio = ((vela[4] - vela[1]) / vela[1] * 100);
  //       if(porcambio>=0.5){logro++}
  //       sumaPo += porcambio
  //       // console.log(sumaPo,'%')
  //       // return [...vela, porcambio]; // Create a new array with the percentage change
  //     });
  //     promed = sumaPo / tamaño
  //     console.log(promed, '   -  ', logro)
  //     symbol.promedio= promed;
  //     symbol.logro = logro;
  //     candles.push({ symbol, data: modifiedCandles });
  //   } catch (error) {
  //     console.error(`Error fetching candles for symbol ${symbol.name}:`, error);
  //   }
  // }));
  tamñoDat = Object.keys(datas).length;
  i=0
  // mapeo symbols|
  await Promise.all(datas.map(async (symbol) => {
    try {
      let velasSymbl = await UMFuturesClient.getKlines(symbol.name, interval, start, end, size);
  
      let sumaPo = 1;
      let tamaño = Object.keys(velasSymbl.data).length;
      let logro = 0;
      let precioMaximo3h = velasSymbl.data[0][1];
      let precioMinimo3h = velasSymbl.data[0][4];
      EMA3 = 0; // Inicializar la EMA3
      let porcentajeFluctuacion3h = 0;
      SMA3_vela = 0.00;
      let a = 0.05;
          j=1;
          // #mapeo velas
      let modifiedCandles = await velasSymbl.data.map((vela) => {    
        let porcambio = ((vela[4] - vela[1]) / vela[1]) * 100;
        if (porcambio >= 0.5 || porcambio<=-0.5) {
          logro++;
        }
        sumaPo += porcambio;
  
        // Cálculo de EMA3
        EMA3 = a * vela[4] + (1 - a) * EMA3;
  
        // Cálculo de porcentaje de fluctuación de 3 horas
        precioMaximo3h = Math.max(precioMaximo3h, vela[1]);
        precioMinimo3h = Math.min(precioMinimo3h, vela[4]);
        porcentajeFluctuacion3h = ((precioMaximo3h - precioMinimo3h) / precioMinimo3h) * 100;
  
        // Cálculo de SMA3
          SMA3_vela += parseFloat(vela[4]);
          // console.log(SMA3_vela);
        // Agregar indicadores a la vela modificada
        console.log(tamaño, '- ',j, '/',tamñoDat,'-',i)
        j++
        return vela;
      });
  
      // REVISAR FORMULAS (sumValMinTot - SumValMaxTot)*100
      let promed = sumaPo / tamaño;
      // console.log(promed.toFixed(3), "   -  ", logro);
  
      // Agregar indicadores al símbolo
      symbol.promedio =  promed.toFixed(3)+'%'
      symbol.logro = logro;
      symbol.ema = EMA3.toFixed(3); // Valor final de EMA3
      symbol.pft = porcentajeFluctuacion3h.toFixed(3); // Valor final del porcentaje de fluctuación de 3 horas
      symbol.SMA = (SMA3_vela/tamaño).toFixed(3); // Valor final de SMA3
      symbol.data =modifiedCandles
      candles.push({ symbol});
      console.log(tamñoDat, ' - ', i)
      i++
    } catch (error) {
      console.error(`Error fetching candles for symbol ${symbol.name}:`, error);
    }
  }));
  console.log('listo')
  return await candles


}



module.exports = 
{
    getExchangeInfo,
    getCandles,
    testConectionServ,
}


