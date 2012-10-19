import pickle
import xml.etree.ElementTree as ET

class Person:
  def __init__(self, member_id, congress, chamber):
    self.id = member_id
    self.congress = congress
    self.chamber = chamber
    memberPath = 'data/'+self.chamber+'/'+self.congress+'/members/'+self.id+'/bio.xml'
    self.bio = ET.parse(memberPath).getroot().find('results').find('member')
    self.firstname = self.bio.find('first_name').text
    self.lastname = self.bio.find('last_name').text
    self.party = self.bio.find('current_party').text
    self.state = self.bio.find('roles').find('role').find('state').text
  def pretty(self):
    return self.firstname+' '+self.lastname+', '+self.party+' of '+self.state
  def partyColor(self):
    colordict = {'D':'b','R':'r','I':'g'}
    return colordict[self.party]