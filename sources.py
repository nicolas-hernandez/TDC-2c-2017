from scapy.all import *
from helpers import expand
from collections import Counter
from math import log
from helpers import Ei

class Source1():

    def __init__(self, pcap):
        source = []
        self.nUnicastMessages = 0
        self.nBrodcastMessages = 0

        for packet in pcap:
            protocol = packet.payload.name
            if packet.dst == "ff:ff:ff:ff:ff:ff":
                destKind = "broadcast"
                self.nBrodcastMessages += 1
            else:
                destKind = "unicast"
                self.nUnicastMessages += 1

            source.append(str((destKind, protocol)).replace("'", ""))

        self.sourceCount = Counter(source)
        self.entropy = reduce((lambda x, v: x + Ei(v, len(pcap))), self.sourceCount.itervalues(), 0)
        self.maxEntropy = log(len(self.sourceCount.keys()), 2) 
    
    def name(self):
        return "Fuente 1"

'''
Source2 tiene que aportar la suficiente informacion como para poder distingir hosts a traves de los paquetes ARP: 
Los paquetes ARP pueden ser de operacion who-has o is-at, siendo la segunda la respuesta de la primera. Se tomara como supuesto
que el nodo cuya IP va a ser mas solicitada por who-has va a tener que ser la del default-gateway, ya que las redes analizadas mayormente
se usan para el acceso a internet (minimizamos totalmente los mensajes ARP entre hosts de la misma red)

Distinguir simbolos:
La metadata se guarda en forma de tupla (ipsrc , ipdst) del mensaje who-has, pero cada simbolo es solamente ipdst ya que estamos tratando de distinguir al router
para asi distinguir a los hosts
'''
class Source2():

	def __init__(self, pcap):
		self.metadata = []
		S2 = []
		arpPackets = pcap[ARP]
		for packet in arpPackets:
			self.metadata.append((packet.psrc, packet.pdst))
			S2.append(packet.pdst)

		self.sourceCount = Counter(S2)
		self.entropy = reduce((lambda x, v: x + Ei(v, len(arpPackets))), self.sourceCount.itervalues(), 0)
		self.maxEntropy = log(len(self.sourceCount.keys()), 2) 

	def name(self):
		return "Fuente 2"
