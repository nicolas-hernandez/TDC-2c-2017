from scapy.all import *
from sets import Set
from collections import Counter
import math
import csv
import os

conf.verb = 0

def createCSVFromPCAPNameFontNumberProbsAndEntropy(name, fontNumber, data1, data2):
	directory = "tables/"

	if not os.path.exists(directory):
		os.makedirs(os.path.dirname(directory))	

	fileName = name.split('.')[0] + str(fontNumber)	+ ".csv"
	
	with open(directory + fileName, 'wb') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		for key, value in data1.iteritems():
			wr.writerow((key, value))
		
		wr.writerow(["entropy", data2])

#--------------------------------#
#--------------------------------#
#--------------------------------#
'''
print "TCP Fields: \n"
ls(TCP)
print "\nIP Fields: \n"
ls(IP)
print "\nEthernet Fields: \n"
ls(Ether)
print "\nARP Fields: \n"
ls(ARP)
'''
#--------------------------------#
#--------------------------------#
#--------------------------------#

print "\nPCAP Test summary: \n"

'''
pcap1 = "Rivera_4370_Sabado_11_50_Dia_lluvioso.pcap"
pcap2 = "Rivera_4370_Viernes_23_45_Dia_despejado.pcap"
'''

pcap = raw_input("Enter pcap name: ")

pcap_p = rdpcap(pcap)

npkts = len(pcap_p)

#--------------------------------#
#-----------MAP REDUCE-----------#
#--------------------------------#

'''
Reduce pcap protocols to a dictionary of font S1 and apparitions count
font is <unicast/broadcast, layer three protocol>
count is the number of apparitions in the pcap
'''

def expand(x):
	yield x.name
	while x.payload:
		x = x.payload
		yield x.name

def countFontS1(pcap_p):
	S1 = []

	for p in pcap_p:
		#print p.summary()
		protocols = list(expand(p))
		#print protocols
		for x in protocols:
			if not x in ['Ethernet', 'IP', 'IPv6']:
				destKind = "unicast"
				if p.dst == "ff:ff:ff:ff:ff:ff":
					destKind = "broadcast"
				S1.append(str((destKind, x)).replace("'", ""))
				break
	
		#print "\n End packet \n"

	S1Count = Counter(S1)

	return S1Count

'''
Reduce pcap protocols to a dictionary of font S2 and apparitions count
font is <IP Source, IP Dest>
count is the number of apparitions in the pcap
'''

def countFontS2(pcap_p):
	'''
	for p in pcap_p[ARP]:
		S2.append(str((p.psrc, p.dst)))
	'''

	S2 = [str((p.psrc, p.pdst)).replace("'", "") for p in pcap_p[ARP]]

	S2Count = Counter(S2)

	return S2Count

#--------------------------------#
#----------E(S) and I(S)---------#
#--------------------------------#

def P(x, total):
	return x/float(total)

def I(p):
	return -math.log(p, 2)

def Ei(x, total):
	pi = P(x, total)
	return pi*I(pi)

def calculateProbabilitiesToSourceCount(SCount, npkts):
	'''
	Map to calculate the probability of every element in the font
	'''

	sourceProb = dict(map(lambda (k,v): (k, P(v, npkts)), SCount.iteritems()))

	print sourceProb

	return sourceProb

def calculateEntropyToSourceCount(SCount, npkts):
	'''
	Reduce to calculate the font entropy
	'''
	
	entropy = reduce((lambda x, v: x + Ei(v, npkts)), SCount.itervalues(), 0)

	print entropy

	return entropy

S1Count = countFontS1(pcap_p)
S1Prob = calculateProbabilitiesToSourceCount(S1Count, npkts)
S1Entropy = calculateEntropyToSourceCount(S1Count, npkts)

createCSVFromPCAPNameFontNumberProbsAndEntropy(pcap, 1, S1Prob, S1Entropy)

S2Count = countFontS2(pcap_p)
S2Prob = calculateProbabilitiesToSourceCount(S2Count, npkts)
S2Entropy = calculateEntropyToSourceCount(S2Count, npkts)

createCSVFromPCAPNameFontNumberProbsAndEntropy(pcap, 2, S2Prob, S2Entropy)

