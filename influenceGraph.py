##Helper functions for constructing influence graphs
import networkx as nx
import numpy as np
from dataClasses import *

def getInfluenceList(simMatrix,use_zscore=True,bottom=0,top=0):
  influenceList = []
  if use_zscore:
    for s in simMatrix:
      mu = round(np.mean(s))
      st = round(np.std(s))
      zscores = map(lambda e: (e-mu)/st, s)
      sortscores = zscores
      sortscores.sort()
      topTail = sortscores[len(sortscores)-5] #1.5
      bottomTail = sortscores[4] #-1.5
      posinfluence = filter(lambda i: zscores[i]>topTail, range(len(zscores)))
      neginfluence = filter(lambda i: zscores[i]<bottomTail, range(len(zscores)))
      influenceList.append({'pos':posinfluence, 'neg':neginfluence})
  else:
    for s in simMatrix:
      posinfluence = filter(lambda i: s[i]>top, range(len(s)))
      neginfluence = filter(lambda i: s[i]<bottom, range(len(s)))  
      influenceList.append({'pos':posinfluence, 'neg':neginfluence})
  return influenceList

def createGraph(influenceList,weight=False,similarity_matrix=[],weight_lamda=lambda x:x):
  influenceGraph = nx.Graph()
  for i in xrange(len(influenceList)):
    if weight:
      map(lambda p: influenceGraph.add_edge(i,p,weight=weight_lamda(similarity_matrix[i][p])), influenceList[i]['pos']+influenceList[i]['neg'])
    else:
      map(lambda p: influenceGraph.add_edge(i,p), influenceList[i]['pos']+influenceList[i]['neg'])
  return influenceGraph

