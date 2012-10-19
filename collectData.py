##Gather raw data from NYTimes developer
import urllib2
import os
import time
import itertools #For cartesian product *lists
import xml.etree.ElementTree as ET
from utils import checkpath
import apikey

api_key = apikey.getKey()

searches = [[111],['house','senate']]

for search in itertools.product(*searches): #Get the past 5 sessions of both house/senate
  congress = str(search[0])
  chamber = search[1]
  #Get members and committees
  time.sleep(1)
  members = urllib2.urlopen('http://api.nytimes.com/svc/politics/v3/us/legislative/congress/'+congress+'/'+chamber+'/members.xml?api-key='+api_key).read()
  committees = urllib2.urlopen('http://api.nytimes.com/svc/politics/v3/us/legislative/congress/'+congress+'/'+chamber+'/committees.xml?api-key='+api_key).read()
  folderPath = 'data/raw/'+chamber+'/'+congress
  checkpath(folderPath)
  file(folderPath+'/members.xml','w').write(members)
  file(folderPath+'/committees.xml','w').write(committees)
  
  bleep = """
  time.sleep(1)
  #Get committee members
  print 'Getting committee members'
  committeeList = ET.fromstring(committees).find('results').find('committees')
  for c in committeeList.findall('committee'):
    time.sleep(.5)
    committeeId = c.find('id').text
    committeeData = urllib2.urlopen('http://api.nytimes.com/svc/politics/v3/us/legislative/congress/'+congress+'/'+chamber+'/committees/'+committeeId+'.xml?api-key='+api_key).read()
    folderPath = 'data/raw/'+chamber+'/'+congress+'/committees'
    checkpath(folderPath)
    file(folderPath+'/'+committeeId+'.xml','w').write(committeeData)
  """

  #Get votes by member
  time.sleep(2)
  print 'Getting votes and bios per member'
  memberTree = ET.fromstring(members)
  for m in memberTree.find('results').find('members').findall('member'):

    memberId = m.find('id').text
    if memberId[0]>'L':
      time.sleep(.5)
      print memberId
      voteHistory = urllib2.urlopen('http://api.nytimes.com/svc/politics/v3/us/legislative/congress/members/'+memberId+'/votes.xml?api-key='+api_key).read()
      time.sleep(.5)
      memberBio = urllib2.urlopen('http://api.nytimes.com/svc/politics/v3/us/legislative/congress/members/'+memberId+'.xml?api-key='+api_key).read()
      folderPath = 'data/raw/'+chamber+'/'+congress+'/members/'+memberId
      checkpath(folderPath)
      file(folderPath+'/votes.xml','w').write(voteHistory)
      file(folderPath+'/bio.xml','w').write(memberBio)

  print "Getting votes by bill"
  time.sleep(2)
  #Get votes by bill
  for session in ['1','2']:
    folderPath = 'data/raw/'+chamber+'/'+congress+'/'+session+'/rollcall'
    checkpath(folderPath)
    flag = True
    i = 0
    while flag == True: #Go for all records, catch 404 to escape
      i += 1
      time.sleep(.5) #Limit 2 calls/sec
      bill = str(i)
      print [session,bill]
      query = 'http://api.nytimes.com/svc/politics/v3/us/legislative/congress/'+congress+'/'+chamber+'/sessions/'+session+'/votes/'+bill+'.xml?api-key='+api_key
      try:
        response = urllib2.urlopen(query)
        voteData = response.read()
        file(folderPath+'/'+bill+'.xml','w').write(voteData)
      except urllib2.HTTPError:
        flag = False