##Take separate raw files and extract votes in a condensed format
import xml.etree.ElementTree as ET
import os
import itertools
import csv
import utils
import pickle


lookup = {'Yes':2, 'No':1, 'Not Voting':0, 'Present':3, 'Speaker':4}
voteData = {}


searches = [[112],['house','senate']]

for search in itertools.product(*searches):
  voteData = {}
  congress = str(search[0])
  chamber = search[1]
  memberPath = 'data/raw/'+chamber+'/'+congress+'/members.xml'
  members = ET.parse(memberPath).getroot().find('results').find('members').findall('member')
  #Init empty list for each member
  for member in members:
    voteData[member.find('id').text] = []
  #Go through each rollcall of each session and record votes
  for session in ['1','2']:
    rollcallPath = 'data/raw/'+chamber+'/'+congress+'/'+session+'/rollcall'
    for fileList in os.walk(rollcallPath):
        for rollCall in fileList[2]:
            votes = ET.parse(rollcallPath+'/'+rollCall).getroot().find('results').find('votes').find('vote').find('positions').findall('position')
            for vote in votes:
              position = vote.find('vote_position').text
              memberId = vote.find('member_id').text
              if lookup.has_key(position):
                voteData[memberId].append(lookup[position])
              else:
                voteData[memberId].append(-1)
  utils.writeDict(voteData,'votes-'+congress+chamber)

last100 = """
for search in itertools.product(*searches):
  voteData = {}
  congress = str(search[0])
  chamber = search[1]
  rootPath = 'data/'+chamber+'/'+congress
  members = ET.parse(rootPath+'/members.xml').getroot().find('results').find('members').findall('member')
  for member in members:
    member_id = member.find('id').text
    print member_id
    votes = ET.parse(rootPath+'/members/'+member_id+'/votes.xml').getroot().find('results').find('votes').findall('vote')
    voteList = map(lambda v: lookup[v.find('position').text], votes)
    voteData[member_id] = voteList
  utils.writeDict(voteData,'votes-'+congress+chamber)

print voteData['A000069']
print len(voteData['A000069'])

"""


