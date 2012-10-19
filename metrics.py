##Helper functions to create features from raw data

def similarity(p1,p2):
  sims = {True:1.0,False:0.0}
  return sum(map(lambda x,y: sims[x==y], p1, p2))#/(max(min(len(p1),len(p2)),1)+0.0)

def similarityMatrix(voteData): #Percentage similarity
  similarities = []
  nVotes = 0
  people = []
  for person1 in voteData:
    people.append(person1)
    tempsim = []
    for person2 in voteData:
      nVotes = max(min(len(voteData[person1]),len(voteData[person2])),1)
      percentSim = round(100.0*similarity(voteData[person1],voteData[person2])/nVotes)
      tempsim.append(percentSim)
    similarities.append(tempsim)
  return similarities