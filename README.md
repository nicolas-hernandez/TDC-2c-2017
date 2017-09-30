# tdc2c2017

1.- sacpy_tests.py NO está modularizado. Pero seria sencillo hacerlo.
2.- se corre como se corre habitualmente un py. Hay que ingresar el nombre del archivo pcap (con su formato)
3.- Hay 3 archivos. Los de 60k paquetes son los que valen. Hay uno con menos paquetes para hacer tests de prueba.
4.- Las tablas se guardan en tables/
5.- Formato csv Fuente S1:
	a.- (unicast/broadcast, Layer Protocol) | probabilidad
	b.- Entropia
6.- Formato csv Fuente S2:
	a.- (IP source, IP dest) | probabilidad
	b.- Entropia
