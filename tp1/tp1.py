#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-


import argparse 
from helpers import * 
from sources import * 
from scapy.all import rdpcap                                              
from scapy.all import *

from sets import Set
from collections import Counter
import math
import csv
import os
from sources import *

conf.verb = 0

class CsvPrinter():
    def __init__(self, source, nPackets):
        self.source = source
        self.packetCount = nPackets
        self.sourceRows = list(map(lambda(protocol, count):
            (protocol, P(count, self.packetCount), I(P(count, self.packetCount))),
            self.source.sourceCount.iteritems()))
         
    def createCSV(self, pcapFilename):
		directory = "tables/"

		if not os.path.exists(directory):
			os.makedirs(os.path.dirname(directory))	

		folders = pcapFilename.split('/')
		input_file_name = folders[len(folders) - 1]
		fileName = directory + input_file_name.split('.')[0] + "_" + self.source.name().replace(" ", "") + ".csv"
		with open(fileName, 'wb') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow(('Simbolo', 'Probabilidad', 'Informacion'))
			for item in self.sourceRows:
				wr.writerow(item)
			wr.writerow(('Entropia de la fuente', self.source.entropy))
			wr.writerow(('Entropia Máxima', self.source.maxEntropy))


        
if __name__ == "__main__":
    #Parse command line arguments
	parser = argparse.ArgumentParser(description='Script for analizing network packets.')
	parser.add_argument("file", help="Pcap formatted capture")            
	args = parser.parse_args()                                            
            
	pcap = rdpcap(args.file)

	S1 = Source1(pcap)
	csv1 = CsvPrinter(S1, len(pcap))
	csv1.createCSV(args.file)

	S2 = Source2(pcap)
	csv2 = CsvPrinter(S2, len(pcap))
	csv2.createCSV(args.file)
