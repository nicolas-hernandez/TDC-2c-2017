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
