import sys
from pylab import *
from sets import Set
import matplotlib.pyplot as plt
import networkx as nx
import collections

'''
Summoned script extension
Input file:
 
Edges from where nodes are deduced
Example:

 Edges
 IP1 IP4
 IP3 IP1 
 
'''


def getNextIndex():
    global index
    index = index + 1
    return index

def getIndex(ip):
    global G, nodes
    if ip not in ipMap.keys():
        i = getNextIndex()
        ipMap[ip] = i
        labels[i]=ip
        nodes.append(i)

    return ipMap[ip]


def printEdge(edge):
    global edgesCount
    global edges
    ip1 = edge[0]
    ip2 = edge[1]
    ip1I = getIndex(ip1)
    ip2I = getIndex(ip2)
    count = edgesCount[(ip1,ip2)]
    edges.append((ip1I,ip2I, count))
  

ipMap = {}
index = -1
edges = []
edgesCount = None
nodes = []
labels = {}
lines = [line.rstrip('\n') for line in open(sys.argv[1])]

setEd = Set([])
arrEd = []
#Parse ips
for line in lines:   
   newIps = line.split(" ",2)
   setEd.add((newIps[0],newIps[1]))
   arrEd.append((newIps[0],newIps[1]))

edgesCount = collections.Counter(arrEd)


for package in setEd:
    printEdge(package)



G = nx.MultiGraph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)
G.degree(weight='weight')
pos = nx.spring_layout(G)



#nx.draw_networkx_nodes(G,pos,node_color='r',node_size=500,alpha=0.8)
#nx.draw_networkx_edges(G,pos,width=8,alpha=0.5,edge_color='r')

nx.draw(G,node_size=500, with_labels=True,labels=labels,width=edgesCount.values())
plt.show()
