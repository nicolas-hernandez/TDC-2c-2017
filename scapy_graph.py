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
        self.capture = pcap

    def sourceCount(self):
        source = []
        unicast = 0
        brodcast = 0
        for packet in self.capture:
            protocols = list(expand(packet))
            for pr in protocols:
                if not pr in ['Ethernet', 'IP', 'IPv6']:
                    if packet.dst == "ff:ff:ff:ff:ff:ff":
                        destKind = "broadcast"
                        brodcast += 1
                    else:
                        destKind = "unicast"
                        unicast += 1
                    source.append(str((destKind, pr)).replace("'", ""))
                    break
        count = Counter(source)
 
        return count, unicast, brodcast

    def percentagePlot(self):
        counter, unicast, brodcast = self.sourceCount()
        keys = counter.keys()
        values = counter.values()
        total = sum(values)
        percentages = [amount*100/total for amount in values]
        trace = go.Bar(x = keys, y = percentages)
        data = [trace]
        layout = go.Layout(
                title='Fuente S1: Porcentaje de cada simbolo',
                width=1280,
                height=720,
                xaxis={'title':'Simbolos'},
                yaxis={'title':'Porcentaje'})
        fig = go.Figure(data=data, layout=layout)
        return fig
    
    def infoPlot(self):
        counter, unicast, brodcast = self.sourceCount()
        keys = counter.keys()
        values = counter.values()
        total = sum(values)
        percentages = [amount*100/total for amount in values]
        trace = go.Bar(x = keys, y = percentages)

        labels = ['Unicast', 'Brodcast']
        values = [unicast, brodcast]
        trace2 = go.Pie(labels=labels, values=values)

        data = [trace, trace2]
        layout = go.Layout(
                title='Fuente S1: Porcentaje de cada simbolo',
                width=1280,
                height=720,
                xaxis={'title':'Simbolos'},
                yaxis={'title':'Porcentaje'})
        fig = go.Figure(data=data, layout=layout)
        return fig
    





if __name__ == "__main__":
    #Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for analizing network packets.')
    parser.add_argument("file", help="Pcap formatted capture")
    args = parser.parse_args()

    pcap = rdpcap(args.file)
    S1 = Source1(pcap)
    figS1 = S1.percentagePlot()
    S1filename = args.file.replace('pcap', 'png')
    py.image.save_as(figS1, filename=S1filename)
    #Source2(pcap) sale alta superclase aca
