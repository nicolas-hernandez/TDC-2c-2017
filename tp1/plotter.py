import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='nicoh22', api_key='ZCBvY2IQs9nlGOgid8Ua')
from scapy.all import *
from helpers import *
class Plotter():
    def __init__(self, source):
        self.source = source
    def probabilityPlot(self):
        
        keys = self.source.sourceCount.keys()
        values = self.source.sourceCount.values() 
        probs = [P(amount, sum(values)) for amount in values]
        trace = go.Bar(x = keys, y = probs)
        data = [trace]
        layout = go.Layout(
                title=self.source.name()+': Probabilidad de cada simbolo',
                width=1280,
                height=720,
                xaxis={'title':'Simbolo'},
                yaxis={'title':'Probabilidad (en escala logaritmica)','type':'log','autorange':True}, 
                margin=go.Margin(
		    l=50,
		    r=50,
		    b=100,
		    t=50,
		    pad=4))
        fig = go.Figure(data=data, layout=layout)
        return ProbaFigure(fig)
    
    def distributionPlot(self):
       
        labels = ['Unicast', 'Broadcast']
        values = [self.source.nUnicastMessages, self.source.nBrodcastMessages]
        trace = go.Pie(labels=labels, values=values)

        data = [trace]
        layout = go.Layout(
                title=self.source.name()+': Distribucion entre unicast y broadcast',
                width=1280,
                height=720)
        fig = go.Figure(data=data, layout=layout)
        return DistroFigure(fig)

    def informationPlot(self):
        keys = self.source.sourceCount.keys()
        values = self.source.sourceCount.values()
        #Calculating each symbol's information
        probs = [I(P(amount,sum(values))) for amount in values]
        informationTrace = go.Bar(name="Informacion x simbolo",x = keys, y = probs)
        #Magic to show a constant for the entropy
        entropyTrace = go.Scatter(name="Entropia",x = [keys[0],keys[len(keys)-1]], y = [self.source.entropy, self.source.entropy])
        maxEntropyTrace = go.Scatter(name="Entropia Maxima",x = [keys[0],keys[len(keys)-1]], y = [self.source.maxEntropy, self.source.maxEntropy])
        data = [informationTrace, entropyTrace, maxEntropyTrace]
        layout = go.Layout(
                title=self.source.name()+': Informacion de cada simbolo',
                width=1280,
                height=720,
                xaxis={'title':'Simbolo'},
                yaxis={'title':'Informacion'})
        fig = go.Figure(data=data, layout=layout)
        return InfoFigure(fig)


class InfoFigure():
    def __init__(self, plotly_figure):
        self.figure = plotly_figure
    def name(self):
        return "information"

class DistroFigure():
    def __init__(self, plotly_figure):
        self.figure = plotly_figure
    def name(self):
        return "distribution"

class ProbaFigure():
    def __init__(self, plotly_figure):
        self.figure = plotly_figure
    def name(self):
        return "probability"
