<div>
api lque se llamara ATI para manejar de manera eficienate una AI que se llamara trinity de tensor flow que debera contener la AI  configurada para entrenamiento, test y dev, y cumplira las siguientes funciones a traves de la API
- obtener listado historico de 1 dia en especifico a travez de la api de Binance y almacenarlo en un una tabla en mongo db -> ../api/bn/addata - GET
- obtener los datos historicos de criptomonedas almacenados en la base de datos, darles formato para que la AI pueda iniciar el entrenamiento e iniciar el entrenamiento de la AI ->  .../api/trini/treaninig -> GET ( Metodo asincrono que devuelve un mensaje de el inicio del entrenamiento )
- obtener las dispercion de la AI en el entrenamiento para mostrarlo graficamente, esta informacion debe mostrarce en vivo actualizando constantenmente en una pagina web realizada en JADE .../api/trini/disp  -> GET 
- iniciar el despliege de la AI se debe debolver el mensaje de despliege exitoso o fallido, solo se debe permitir desplegar si el test cumple mas de un 85% de fiabilidad.
- iniciar el test del entrenamiento de la AI debe ser sincronico devolvover la dispercion de la AI en vivo hasta terminar el test  ->  .../api/trini/test - POST
- se debe configurar la AI crear el entrenamiento, test y despliege, para las funciones que realizara la AI que son las siguientes: 
- la funcion principal de la AI es tomar "x USDT" que no podra ser mayor al 70% de los fondos en la wallet de binance, y debera realizar el poroceso de  ->  encontrar N divisas en conjunto que al  realizar la convercion llegando al final a nuevamente a USDT deje una ganancia minimiqa de 2% teniendo en cuenta que cada transaccion que se realize tendra una comosion de 0.005% que se reduce al momento de realizar la convercion, 
ejemplo: 
         1 BTC -> 70000 USDT     entonces  100 USDT =  0,00142857 BTC 
 16000   Y    ->         1 BTC       entonces   0,00142857 BTC =    22, 85712 Y
          1   y   =>   5 USDT         entonces   22, 85712  y    =     114,2856 USDT  

en este EJEMPLO  la ganancia seria de 14%  aprox  pero es solo un ejemplo la AI debera Buscar convinaciones entre divisas que generen la mayor ganancia posible en ese momento, obteniendo el valor actual de las divisas, realizar la comparacion, decidir cual es la mejor convinacion, pero antes de realizar la transaccion debera verificar el precio nuevamente unicamente de las divisas que entran en la convinacion y en caso de que alguna transaccion ya no sea rentable debra descrtarla hasta que sea viable para obtener ganancias, en caso de que si sea viable debera realizar la transaccion a travez de la api de binance, en caso de que en la mitad de la operacion el cambio de precio afecte la AI debera mantener la pocicion de esa divisa hasta que sea nuevamente rentable, y poder continuar,  se debe crear el algoritmo para el proceso de seleccion de la divisa, el modelo de entrenamiento el test y el despliege. 

esta es la primera operacion que realizara la AI en conjunto con la api todo debe ser en python debe manejar una arquitectura hexagonal
</div>