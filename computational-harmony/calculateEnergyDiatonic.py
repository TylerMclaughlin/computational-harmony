import itertools as it

from operator import itemgetter

cMajor =  [0,2,4,5,7,9,11]
chromatic = [0,1,2,3,4,5,6,7,8,9,10,11]


noteDict = {} 
for i, v in enumerate (['C natural', 'C sharp', 'D natural', 'E flat','E natural','F natural','F sharp','G natural', 'G sharp','A natural', 'B flat','B natural']):
  #print i,v
  noteDict[i] = v
#print noteDict

def getMajorScales():
   majorScalesDict = {}
   for x in chromatic:
       myTemp = [(asdf + x)%12 for asdf in cMajor]
       majorScalesDict[noteDict[x]] = myTemp
   return majorScalesDict

majorScales = getMajorScales()

Cmin7 = [0,3,7,10]

def energy(chord,myScalesDict):
   counter = 0

