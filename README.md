# tdc2c2017

1.- sacpy_tests.py NO está modularizado. Pero seria sencillo hacerlo.
<br />
2.- se corre como se corre habitualmente un py. Hay que ingresar el nombre del archivo pcap (con su formato)
<br />
3.- Hay 3 archivos. Los de 60k paquetes son los que valen. Hay uno con menos paquetes para hacer tests de prueba.
<br />
4.- Las tablas se guardan en tables/
<br />
5.- Formato csv Fuente S1:<br />
	a.- (unicast/broadcast, Layer Protocol) | probabilidad<br />
	b.- Entropia
<br />
6.- Formato csv Fuente S2:<br />
	a.- (IP source, IP dest) | probabilidad<br />
	b.- Entropia
