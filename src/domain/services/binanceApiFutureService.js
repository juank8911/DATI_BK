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
  tamñoDat = Object.keys(datas).length;

  // mapeo symbols|
  i = 0;
  await Promise.all(
    datas.map(async (symbol) => {
      try {
        let modifiedCandles = [];
        let velasSymbl = await UMFuturesClient.getKlines(
          symbol.name,
          interval,
          start,
          end,
          size
        );
        let sumaPo = 1;

        let tamaño = Object.keys(velasSymbl.data).length;
        let logro = 0;
        let precioMaximo3h = velasSymbl.data[0][1];
        let precioMinimo3h = velasSymbl.data[0][4];
        EMA3 = 0; // Inicializar la EMA3
        let porcentajeFluctuacion3h = 0;
        SMA3_vela = 0.00;
        let a = 0.05;
        j = 1;
        // #mapeo velas

        velaN = {}; // Initialize velaN as an object outside the loop

        await velasSymbl.data.map(async (vela) => {
          let porcambio = ((vela[4] - vela[1]) / vela[1]) * 100;
          if (porcambio >= 0.5 || porcambio <= -0.5) {
            logro++;
          }
          sumaPo += porcambio;

          // Cálculo de EMA3
          EMA3 = a * vela[4] + (1 - a) * EMA3;

          // Cálculo de porcentaje de fluctuación de 3 horas
          precioMaximo3h = Math.max(precioMaximo3h, vela[1]);
          precioMinimo3h = Math.min(precioMinimo3h, vela[4]);
          porcentajeFluctuacion3h =
            ((precioMaximo3h - precioMinimo3h) / precioMinimo3h) * 100;

          // Cálculo de SMA3
          SMA3_vela += parseFloat(vela[4]);

          // Assign values to velaN object
          velaN.timestamp_apertura = vela[0]; // Assuming timestamp is in milliseconds
          velaN.precio_apertura = vela[1];
          velaN.precio_maximo = vela[2];
          velaN.precio_minimo = vela[3];
          velaN.precio_cierre = vela[4];
          velaN.volumen = vela[5];
          velaN.timestamp_cierre = vela[6]; // Assuming timestamp is in milliseconds
          velaN.volumen_activo_cotizacion = vela[7];
          velaN.numero_operaciones = vela[8];
          velaN.precio_promedio = vela[9];
          velaN.volumen_cotizacion_promedio = vela[10];
          console.log(await porcambio)
          velaN.fluctua = porcambio;

          // Agregar indicadores a la vela modificada
          // if(i==170){console.log(velaN)}
          console.log(tamaño, "- ", j, "/", tamñoDat, "-", i);
          j++;

          modifiedCandles.push(velaN);
        });

        // REVISAR FORMULAS (sumValMinTot - SumValMaxTot)*100
        let promed = sumaPo / tamaño;
        // console.log(promed.toFixed(3), "   -  ", logro);
        // console.log(modifiedCandles);
        // Agregar indicadores al símbolo
        symbol.promedio = promed.toFixed(3) + "%";
        symbol.logro = logro;
        symbol.ema = EMA3.toFixed(3); // Valor final de EMA3
        symbol.pft = porcentajeFluctuacion3h.toFixed(3); // Valor final del porcentaje de fluctuación de 3 horas
        symbol.SMA = (SMA3_vela / tamaño).toFixed(3); // Valor final de SMA3
        symbol.data = modifiedCandles;
        candles.push({ symbol });
        console.log(tamñoDat, " - ", i);
        i++;
      } catch (error) {
        console.error(
          `Error fetching candles for symbol ${symbol.name}:`,
          error
        );
      }
    })
  );
  console.log("listo");
  return candles;
}




module.exports = 
{
    getExchangeInfo,
    getCandles,
    testConectionServ,
}


