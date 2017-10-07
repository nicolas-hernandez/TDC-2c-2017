from helpers import expand
from collections import Counter
from math import log
from helpers import Ei
class Source1():

    def __init__(self, pcap):
        source = []
        self.nUnicastMessages = 0
        self.nBrodcastMessages = 0
        self.abreviations = {
                'ICMPv6 Neighbor Discovery - Router Advertisement':'ICMPv6 RA',
				'ICMPv6 Neighbor Discovery - Neighbor Advertisement':'ICMPv6 NA', 
                'ICMPv6 Neighbor Discovery - Router Solicitation':'ICMPv6 RS',
                'ICMPv6 Neighbor Discovery - Neighbor Solicitation':'ICMPv6 NS',
                'IPv6 Extension Header - Hop-by-Hop Options Header':'IPv6 EH'
                }
        for packet in pcap:
            protocol = packet.payload.name
            if packet.dst == "ff:ff:ff:ff:ff:ff":
                destKind = "broadcast"
                self.nBrodcastMessages += 1
            else:
                destKind = "unicast"
                self.nUnicastMessages += 1
            pr = self.shortenProtocol(protocol)
            source.append(str((destKind, pr)).replace("'", ""))
        self.sourceCount = Counter(source)
        self.entropy = reduce((lambda x, v: x + Ei(v, len(pcap))), self.sourceCount.itervalues(), 0)
        self.maxEntropy = log(len(self.sourceCount.keys()), 2) 

    def shortenProtocol(self, protocol):
        try:
            shortProtocol = self.abreviations[protocol]
            return shortProtocol
        except KeyError:
            return protocol
    
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
		for packet in pcap:
			if packet.payload.name != "ARP" or packet.payload.op!="who-has":
				continue

			ls(packet.payload)
			self.metadata.append(packet.payload.src, packet.payload.dst) 
        	S2.append(packet.payload.dst)

		self.sourceCount = Counter(S2)
		self.entropy = reduce((lambda x, v: x + Ei(v, len(pcap))), self.sourceCount.itervalues(), 0)
		self.maxEntropy = log(len(self.sourceCount.keys()), 2) 

	def name(self):
		return "Fuente 2"
