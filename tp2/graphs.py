import json, ast
from pprint import pprint
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

plotly.tools.set_credentials_file(username='rkapobel', api_key='iae8tklvy560VS2TRQnW')

with open('www.stanford.edu.json') as data_file:    
    data = json.load(data_file)

#pprint(data)

rtts = []

for hop in data:
    if hop["ip_address"] != None:
        rtts.append(hop["rtt"])

rttDifs = [abs(x - rtts[i - 1]) for i, x in enumerate(rtts) if i > 0]

trace0 = Scatter(
    x=range(0, len(rttDifs)),
    y=rttDifs
)

data = Data([trace0])

py.plot(data, filename = 'basic-line')

