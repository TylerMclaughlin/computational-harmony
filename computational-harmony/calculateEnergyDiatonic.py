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
   keyList = []
   for key in myScalesDict:
      if set(myScalesDict[key]) & set(chord) == set(chord):
         #print key
         keyList.append(key)
         counter += 1
         
   return counter,keyList


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return it.chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

chromaticNoC = [1,2,3,4,5,6,7,8,9,10,11]


#get all chords that start with C and are contained in another set of notes.
# setOfPitches must lack 0.
def makeAllChords(setOfPitches):
   myPS = powerset(setOfPitches)
   #print myPS
   listOfChords = []
   for listX in myPS:
      listX.append(0)
      listX = list(set(listX))  # remove duplicates
      listX.sort()
      #print listX
      listOfChords.append(listX)
   return listOfChords

def powerset(myList):
    return reduce(lambda result, x: result + [subset + [x] for subset in result], myList, [[]])

def toBinary(list):
   " [1,2,7] -> 000010000110 "
   output = 0
   for i in list:
      output = output | 2<<(i-1)
   return output
   #binaryOutput = bin(output)
   #return binaryOutput
     
myInteger = toBinary([1,2,7])

def leftRotate(myInt,maxBits,rotatedBits=1):
    return (myInt << rotatedBits%maxBits) & (2**maxBits-1) | \
    ((myInt & (2**maxBits-1)) >> (maxBits-(rotatedBits%maxBits)))
    

print format(myInteger,'#014b')
#myInteger = 0b1001
fdsa = leftRotate(myInteger,12)
print format(fdsa,'#014b')

allChords = makeAllChords(chromaticNoC)

energyListOfLists = [0]*len(allChords)
i = 0
for chord in allChords:
   myEnergy,myKeyList = energy(chord,majorScales)
   myProduct = myEnergy*len(chord)
   energyListOfLists[i] = [chord,myEnergy,myProduct,myKeyList] 
   i = i+1

orderedEnergies = sorted(energyListOfLists, key=itemgetter(2))

# test energy calculation
#for i in range(len(orderedEnergies)):
#   print orderedEnergies[i]
#test = energy(Cmin7,majorScales)
#print test

#print majorScales[x] 
