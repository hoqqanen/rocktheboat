##Take raw data and extract higher level features using functions in metrics
import utils
import itertools
from metrics import similarityMatrix

searches = [[112],['house','senate']]

for search in itertools.product(*searches):
  congress = str(search[0])
  chamber = search[1]
  voteData = utils.readDict('votes-'+congress+chamber)
  similarities = similarityMatrix(voteData)
  utils.writeDict({'sims':similarities,'people':people},'similarities-'+congress+chamber)