
from scapy.all import *
from sets import Set
from collections import Counter
import math
import csv
import os
import argparse
import plotly.plotly as py
import plotly.graph_objs as go

#Wat do
import plotly
plotly.tools.set_credentials_file(username='nicoh22', api_key='ZCBvY2IQs9nlGOgid8Ua')

conf.verb = 0
def expand(x):
    yield x.name
    while x.payload:
        x = x.payload
        yield x.name

class Source1():

    def __init__(self, pcap):
        source = []
        self.nUnicastMessages = 0
        self.nBrodcastMessages = 0

        for packet in pcap:
            protocols = list(expand(packet))
            for pr in protocols:
                if not pr in ['Ethernet', 'IP', 'IPv6']:
                    if packet.dst == "ff:ff:ff:ff:ff:ff":
                        destKind = "broadcast"
                        self.nBrodcastMessages += 1
                    else:
                        destKind = "unicast"
                        self.nUnicastMessages += 1
                    source.append(str((destKind, pr)).replace("'", ""))
                    break
        self.sourceCount = Counter(source)
        self.entropy = reduce((lambda x, v: x + Ei(v, len(pcap))), self.sourceCount.itervalues(), 0)
        self.maxEntropy = math.log(len(self.sourceCount.keys()), 2) 

        

    def probabilityPlot(self):
        
        keys = self.sourceCount.keys()
        values = self.sourceCount.values() 
        probs = [P(amount, sum(values)) for amount in values]
        trace = go.Bar(x = keys, y = probs)
        data = [trace]
        layout = go.Layout(
                title='Fuente S1: Probabilidad de cada simbolo',
                width=1280,
                height=720,
                xaxis={'title':'Simbolo'},
                yaxis={'title':'Probabilidad','type':'log','autorange':True})
        fig = go.Figure(data=data, layout=layout)
        return fig
    
    def distributionPlot(self):
       
        labels = ['Unicast', 'Broadcast']
        values = [self.nUnicastMessages, self.nBrodcastMessages]
        trace = go.Pie(labels=labels, values=values)

        data = [trace]
        layout = go.Layout(
                title='Fuente S1: Distribucion entre unicast y broadcast',
                width=1280,
                height=720)
        fig = go.Figure(data=data, layout=layout)
        return fig

    def informationPlot(self):
        keys = self.sourceCount.keys()
        values = self.sourceCount.values()
        #Calculating each symbol's information
        probs = [I(P(amount,sum(values))) for amount in values]
        informationTrace = go.Bar(name="Informacion x simbolo",x = keys, y = probs)
        #Magic to show a constant for the entropy
        entropyTrace = go.Scatter(name="Entropia",x = [keys[0],keys[len(keys)-1]], y = [self.entropy, self.entropy])
        maxEntropyTrace = go.Scatter(name="Entropia M\'axima",x = [keys[0],keys[len(keys)-1]], y = [self.maxEntropy, self.maxEntropy])
        data = [informationTrace, entropyTrace, maxEntropyTrace]
        layout = go.Layout(
                title='Fuente S1: Informacion de cada simbolo',
                width=1280,
                height=720,
                xaxis={'title':'Simbolo'},
                yaxis={'title':'Informacion'})
        fig = go.Figure(data=data, layout=layout)
        return fig
'''
Encapsulation of division for clarification
'''
def P(x, total):
	return x/float(total)

'''
Given a probability of a symbol returns the information of the symbol 
'''
def I(p):
	return -math.log(p, 2)

'''
Symbol entropy
'''
def Ei(x, total):
	pi = P(x, total)
	return pi*I(pi)

'''
Plots figure into the file named <plot_name>_<input_file_name> 
'''
def plot_n_save(figure, plot_name, input_file_name):
    name = plot_name+"_" + input_file_name.replace('pcap', 'png') 
    py.image.save_as(figure, filename=name)

if __name__ == "__main__":
    #Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for analizing network packets.')
    parser.add_argument("file", help="Pcap formatted capture")
    args = parser.parse_args()

    pcap = rdpcap(args.file)
    S1 = Source1(pcap)
    
    plot_n_save(S1.probabilityPlot(), "probability",args.file)
    plot_n_save(S1.informationPlot(), "information",args.file)
    plot_n_save(S1.distributionPlot(), "distribution",args.file)
    #Source2(pcap) sale alta superclase aca
