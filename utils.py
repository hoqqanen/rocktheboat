##Utilities for read/write files, as well as some other random shit that should go elsewhere (e.g. object getter methods)
import pickle
import xml.etree.ElementTree as ET
import os
from dataClasses import Person

def checkpath(folderPath):
  if not os.path.exists(folderPath):
    os.makedirs(folderPath)

def writeDict(D,filename): #This should be folderpath,filename if it gets bigger
  f = open('data/processed/'+filename+'.txt', 'w')
  pickle.dump(D,f)
  f.close()
  return 1

def readDict(filename):
  f = open('data/processed/'+filename+'.txt', 'r')
  voteData = pickle.load(f)
  f.close()
  return voteData

def getPeople(member_ids, congress, chamber):
  return map(lambda i: Person(member_ids[i],congress,chamber), range(len(member_ids)))

def degree_distribution (G):
  degs = {}
  for n in G.nodes():
    deg = G.degree(n)
    if deg not in degs:
      degs[deg] = 0
    degs[deg] += 1
  return sorted(degs.items())

