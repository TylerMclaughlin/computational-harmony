import itertools as it

from operator import itemgetter

class Scale:
    ' for all jazz scales' 
    def __init__(self, root, type, notes):
        self.root = root
        self.type = type 
        self.notes = notes

    def getRoot(self):
        return(self.root)

    def getType(self):
        return(self.type)

    def getNotes(self):
        return self.notes

    def getName(self):
        name = self.root + " " + self.type
        return name

    def testScale(self):
        message1 = "test scale is " + self.getName() 
        message2 = " with notes " + str(self.getNotes())
        print message1 + message2



# asymmetrical scales
cMajor = Scale("C","Major",[0,2,4,5,7,9,11])
cAltered = Scale("C","Altered", [0,1,3,4,6,8,10])
cHarmonic = Scale("C","Harmonic Minor", [0,2,3,5,7,8,11])

#######################cMajor.testScale()

# symmetric scales
cWholetone = Scale("C","Wholetone", [0,2,4,6,8,10])
fWholetone = Scale("F","Wholetone", [1,3,5,7,9,11])

cAugmented = Scale("C","Augmented", [0,3,4,7,8,11])
fAugmented = Scale("F","Augmented", [0,1,4,5,8,9])
gAugmented = Scale("G","Augmented", [2,3,6,7,10,11])
bbAugmented = Scale("Bb","Augmented", [1,2,5,6,9,10])

cOctatonic = Scale("C", "Octatonic", [0,1,3,4,6,7,9,10])
fOctatonic = Scale("F", "Octatonic", [0,2,3,5,6,8,9,11])
gOctatonic = Scale("G", "Octatonic", [1,2,4,5,7,8,10,11])

chromatic = Scale("C","Chromatic",[0,1,2,3,4,5,6,7,8,9,10,11])

noteDict = {} 
for i, v in enumerate (['C natural', 'C sharp', 'D natural', 'E flat','E natural','F natural','F sharp','G natural', 'G sharp','A natural', 'B flat','B natural']):
  noteDict[i] = v


def getAsymmetricJazzScales():
    asymmetricJazzScalesDict = {}
    for x in chromatic.getNotes():
        for type in ["Major", "Altered","Harmonic Minor"]: 
            if type == "Major":
                thisScale = [(note + x)%12 for note in cMajor.getNotes()]
            if type == "Altered":
                thisScale = [(note + x)%12 for note in cAltered.getNotes()]
            if type == "Harmonic Minor":
                thisScale = [(note + x)%12 for note in cHarmonic.getNotes()]
            asymmetricJazzScalesDict[(noteDict[x],type)] = thisScale
    return asymmetricJazzScalesDict

def getSymmetricJazzScales():
    symmetricScalesDict = {}
    for scale in [cWholetone,fWholetone,cOctatonic,fOctatonic,gOctatonic,cAugmented,fAugmented,gAugmented,bbAugmented]:
        #scale.testScale()
        symmetricScalesDict[(scale.getRoot(),scale.getType())] = scale.getNotes()
    return symmetricScalesDict



allScales = getAsymmetricJazzScales() 
symScales = getSymmetricJazzScales()
#print symScales
allScales.update(symScales) 
#print allScales

def getMajorScales():
   majorScalesDict = {}
   for x in chromatic.getNotes():
       myTemp = [(asdf + x)%12 for asdf in cMajor.getNotes()]
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

#print energy(Cmin7,allScales)
#print energy([0,4,7,11],allScales)

def chordIntersection(chord1, chord2):
    return list(set(chord1) & set(chord2))

#print chordIntersection([0,4,7,11],[4,8,11,3])

# used for making all chords
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
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    return reduce(lambda result, x: result + [subset + [x] for subset in result], myList, [[]])


allChords = makeAllChords(chromaticNoC)

energyListOfLists = [0]*len(allChords)
i = 0
for chord in allChords:
   myEnergy,myKeyList = energy(chord,allScales)
   myProduct = myEnergy*len(chord)
   energyListOfLists[i] = [chord,myEnergy,myProduct,myKeyList] 
   i = i+1

filtered = energyListOfLists[:]
for l in energyListOfLists:
    if len(l[0]) < 4: 
        filtered.remove(l)

#orderedEnergies = sorted(energyListOfLists, key=itemgetter(2))
orderedEnergies = sorted(filtered, key=itemgetter(2))

#test energy calculation
#for i in range(len(orderedEnergies)):
#   print orderedEnergies[i]

#print allScales

# all scales that start with C (no loss of generality)
allCScales = {k: allScales[k] for k in (('C natural','Altered'),('C natural','Harmonic Minor'),('C','Wholetone'),('C natural','Major'),('C','Augmented'),('C','Octatonic')) }
#print allCScales
#print len(allScales)

def scalesOrderedByOverlap(scaleDict1,scaleDict2):
    intersectionListOfLists = [0]*(len(scaleDict1)*len(scaleDict2))
    i = 0
    for scale1 in scaleDict1:
        for scale2 in scaleDict2:
            if scale1 != scale2:
                currScale1 = scaleDict1[scale1]
                currScale2 = scaleDict2[scale2]
                overlap = chordIntersection(currScale1,currScale2)
                intersectionListOfLists[i] = [scale1,scale2,overlap,len(overlap)]
            else:
                intersectionListOfLists[i] = ["Duplicate","Duplicate",[0],0]
            i = i + 1
    orderedIntersection = sorted(intersectionListOfLists, key = itemgetter(3))
    return orderedIntersection

orderedOverlap = scalesOrderedByOverlap(allCScales,allScales)

for i in range(len(orderedOverlap)):
    print orderedOverlap[i]
## Then pipe this into text file.
