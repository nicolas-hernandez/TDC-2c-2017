import json, ast
from pprint import pprint
import plotly
import plotly.plotly as py
import scipy.stats as stats
import numpy as np
from plotly.graph_objs import *

university = "www.stanford.edu"
#university = "www.unc.edu.ar"
#university = "www.imperial.ac.uk"
#university = "www.uzh.ch"

plotly.tools.set_credentials_file(username='rkapobel', api_key='GTJLAtLjDpoZ4TRBvCKO')

with open(university+'.json') as data_file:    
    data = json.load(data_file)

#pprint(data)

rtts = [hop["rtt"] if hop["ip_address"] != None else 0 for hop in data]

mean = np.mean(rtts)

rtts = [rtt if rtt > 0 else mean for rtt in rtts]

#print(rtts)

ips = [hop["ip_address"] if hop["ip_address"] != None else i+1 for i, hop in enumerate(data)]
rttDifs = [abs(x - rtts[i - 1]) if i > 0 else 0 for i, x in enumerate(rtts)]

#print(ips)
#print(rttDifs)

Xp = np.mean(rttDifs)
S = np.std(rttDifs)

stats = [abs(x - Xp)/S for x in rttDifs]

trace0 = Scatter(
    x=ips,#range(0, len(rttDifs))
    y=rttDifs
)

trace1 = Scatter(
    x=ips,#range(0, len(rttDifs))
    y=stats
)

data0 = Data([trace0])
data1 = Data([trace1])

py.plot(data0, filename = university+"1")
py.plot(data1, filename = university+"2")

