# tdc2c2017
Se entregan 3 scripts escritos en Python2. tp1.py, scapy_graph.py y grapher.py.

tp1.py: Herramienta pedida por enunciado.
Para usarla se la invoca pasando como argumento una captura en formato pcap.
Por ejemplo:
	python2 tp1,py pcap/TAM_wifi.pcap

El output de este script es una tabla en formato csv para cada fuente que se guardan en la carpeta "tables". Tiene para cada simbolo su información y probabilidad y al final la entropia y entropia máxima de la fuente.

grapher.py: script que genera un mapa de red a partir de una captura

Por ejemplo:
    python2 grapher,py pcap/TAM_wifi.pcap

scapy_graph.py: Genera los demás graficos vistos en el informe (para cada fuente: información y probabilidad. Ademas para S1, proporcion entre broadcast y unicast). Los guarda en la carpeta "graficos".

Por ejemplo:
    python2 scapy_graph,py pcap/TAM_wifi.pcap
