#tp2

Se entregan 3 scripts escritos en Python3. tp2.py, geo.py y graphs.py.
tp2.py: Herramienta pedida por enunciado.
Para usarla se la invoca pasando como argumento una direccion ip o url.
Se requieren permisos de administrador para correrla.
Por ejemplo:
	python3 tp2,py www.google.com

El script devuelve por salida estandar el resultado de nuestra implementacion de traceroute en formato json.


geo.py: script que genera un mapa de la  ruta a partir de un archivo con la descripcion de la misma. Se puede guardar el output de tp2.py en un archivo y usarlo como input de este.

Por ejemplo:
    python3 geo,py google.json

graphs.py: Genera los demás graficos vistos en el informe. Toma de argumento un archivo igual al del script anterior. Usa la API de plotly.
Por ejemplo:
    python2 graphs,py google.json
