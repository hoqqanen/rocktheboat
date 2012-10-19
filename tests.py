##Checking out what we've done so far
import networkx as nx
from utils import readDict, getPeople
import numpy as np
from dataClasses import *
from influenceGraph import getInfluenceList, createGraph
import matplotlib.pyplot as plt

congress = '112'
chamber = 'senate'

dat = readDict('similarities-'+congress+chamber)
sims = dat['sims']
member_ids = dat['people']

print len(member_ids)

influenceList = getInfluenceList(sims,False,40,70)
fullPeople = getPeople(member_ids,congress,chamber)
influenceGraph = createGraph(influenceList,True,sims,lambda w: w/100.0)
partyColors = map(lambda x: x.partyColor(), fullPeople)
labels = dict(zip(range(len(fullPeople)), map(lambda x: x.pretty(), fullPeople)))
ecolors = map(lambda e: e[2]['weight'], influenceGraph.edges(data=True))
pos=nx.spring_layout(influenceGraph)
nx.draw(influenceGraph,pos,node_color=partyColors,node_size=80,edge_color=ecolors,with_labels=False)#,labels=labels)
plt.savefig('pos_influence_graph.png')
plt.show()
