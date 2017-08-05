## TO DO:
## 1) make all chords for a given root (not just C)
## 2) implement multiple key names per dictionary (may be over-optimization)
## 3) be able to traverse network
## 4) build contact matrix with all scales x all scales
## 5) see if numbers ever contradict... they shouldn't
####### i.e., make sure only change are None -> int J and not (int J -> int K != J)

#import itertools as it

from operator import itemgetter


class Scale(object):
    """
    Represents a single scale, which is defined as a collection of pitch classes.
    root: string
    type: string
    notes: list of ints; each int should be between 0 and 11.
    >>> myScale = Scale('E flat', 'Major Pentatonic',[3,5,7,10,0])
    """

    def __init__(self, root, type, notes):
        self.root = root
        self.type = type
        self.notes = notes

    def getRoot(self):
        return (self.root)

    def getType(self):
        return (self.type)

    def getName(self):
        name = self.root + " " + self.type
        return name

    def testScale(self):
        message1 = "test scale is " + self.getName()
        message2 = " with notes " + str(self.notes)
        print message1 + message2


# asymmetrical scales
C_MAJOR = Scale("C", "Major", [0, 2, 4, 5, 7, 9, 11])
C_ALTERED = Scale("C", "Altered", [0, 1, 3, 4, 6, 8, 10])
C_HARMONIC_MAJOR = Scale("C", "Harmonic Major", [0, 2, 4, 5, 7, 8, 11])
C_HARMONIC_MINOR = Scale("C", "Harmonic Minor", [0, 2, 3, 5, 7, 8, 11])

#######################cMajor.testScale()

# symmetric scales
# only two unique wholetone scales
C_WHOLETONE = Scale("C", "Wholetone", [0, 2, 4, 6, 8, 10])
F_WHOLETONE = Scale("F", "Wholetone", [1, 3, 5, 7, 9, 11])

# four unique augmented scales
C_AUGMENTED = Scale("C", "Augmented", [0, 3, 4, 7, 8, 11])
F_AUGMENTED = Scale("F", "Augmented", [0, 1, 4, 5, 8, 9])
G_AUGMENTED = Scale("G", "Augmented", [2, 3, 6, 7, 10, 11])
BB_AUGMENTED = Scale("Bb", "Augmented", [1, 2, 5, 6, 9, 10])

# three unique octatonic scales (a.k.a. half/whole diminished scale)
C_OCTATONIC = Scale("C", "Octatonic", [0, 1, 3, 4, 6, 7, 9, 10])
F_OCTATONIC = Scale("F", "Octatonic", [0, 2, 3, 5, 6, 8, 9, 11])
G_OCTATONIC = Scale("G", "Octatonic", [1, 2, 4, 5, 7, 8, 10, 11])

CHROMATIC = Scale("C", "Chromatic", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

def getNoteDictionary():
    noteDict = {}
    for i, v in enumerate(
            ['C', 'C sharp', 'D', 'E flat', 'E', 'F', 'F sharp', 'G', 'G sharp',
             'A', 'B flat', 'B']):
        noteDict[i] = v

    return noteDict

NOTE_DICT = getNoteDictionary()


def getAsymmetricJazzScales():
    """

    scaleType can be thought of as generators for all transpositions of scaleType
    :return:
    """
    asymmetricJazzScalesDict = {}
    for x in CHROMATIC.notes:
        for scaleType in ["Major", "Altered", "Harmonic Minor", "Harmonic Major"]:
            if scaleType == "Major":
                thisScale = [(note + x) % 12 for note in C_MAJOR.notes]
            if scaleType == "Altered":
                thisScale = [(note + x) % 12 for note in C_ALTERED.notes]
            if scaleType == "Harmonic Minor":
                thisScale = [(note + x) % 12 for note in C_HARMONIC_MINOR.notes]
            elif scaleType == "Harmonic Major":
                thisScale = [(note + x) % 12 for note in C_HARMONIC_MAJOR.notes]
            asymmetricJazzScalesDict[(NOTE_DICT[x], scaleType)] = thisScale
    return asymmetricJazzScalesDict


def getSymmetricJazzScales():
    """

    :return:
    """
    symmetricScalesDict = {}
    for scale in [C_WHOLETONE, F_WHOLETONE, C_OCTATONIC, F_OCTATONIC, G_OCTATONIC, C_AUGMENTED, F_AUGMENTED, G_AUGMENTED,
                  BB_AUGMENTED]:
        # scale.testScale()
        symmetricScalesDict[(scale.getRoot(), scale.getType())] = scale.notes
    return symmetricScalesDict



def getMajorScales():
    majorScalesDict = {}
    for x in CHROMATIC.notes:
        myTemp = [(asdf + x) % 12 for asdf in C_MAJOR.notes]
        majorScalesDict[NOTE_DICT[x]] = myTemp
    return majorScalesDict





def energy(chord, myScalesDict):
    counter = 0
    keyList = []
    for key in myScalesDict:
        if set(myScalesDict[key]) & set(chord) == set(chord):
            # print key
            keyList.append(key)
            counter += 1

    return counter, keyList



def chordIntersection(chord1, chord2):
    return list(set(chord1) & set(chord2))





# get all chords that start with C and are contained in another set of notes.
# setOfPitches must lack 0.
def makeAllChords(setOfPitches = CHROMATIC.notes, rootNote = 'C'):


    if isinstance(rootNote, str):
        firstNote = NOTE_DICT.keys()[NOTE_DICT.values().index(rootNote)]
    else:  # is an int
        firstNote = rootNote
    # make the set of all subsets missing the root
    setMinusRoot = set(setOfPitches) - set([firstNote])
    myPS = powerset(setMinusRoot)
    # print myPS

    listOfChords = []
    for listX in myPS:
        listX.append(firstNote)
        listX = list(set(listX))  # remove duplicates
        listX.sort()
        # print listX
        listOfChords.append(listX)

    return listOfChords


def powerset(myList):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    return reduce(lambda result, x: result + [subset + [x] for subset in result], myList, [[]])




def scalesOrderedByOverlap(scaleDict1, scaleDict2):
    intersectionListOfLists = [0] * (len(scaleDict1) * len(scaleDict2))
    i = 0
    for scale1 in scaleDict1:
        for scale2 in scaleDict2:
            if scale1 != scale2:
                currScale1 = scaleDict1[scale1]
                currScale2 = scaleDict2[scale2]
                overlap = chordIntersection(currScale1, currScale2)
                intersectionListOfLists[i] = [scale1, scale2, overlap, len(overlap)]
            else:
                intersectionListOfLists[i] = ["Duplicate", "Duplicate", [0], 0]
            i = i + 1
    orderedIntersection = sorted(intersectionListOfLists, key=itemgetter(3))
    return orderedIntersection




def main():

    allScales = getAsymmetricJazzScales()
    symScales = getSymmetricJazzScales()
    # print symScales
    allScales.update(symScales)

    # print allScales
    majorScales = getMajorScales()

    Cmin7 = [0, 3, 7, 10]

    # print energy(Cmin7,allScales)
    # print energy([0,4,7,11],allScales)

    allChords = makeAllChords()

    energyListOfLists = [0] * len(allChords)
    i = 0
    for chord in allChords:
        myEnergy, myKeyList = energy(chord, allScales)
        myProduct = myEnergy * len(chord)
        energyListOfLists[i] = [chord, myEnergy, myProduct, myKeyList]
        i = i + 1

    filtered = energyListOfLists[:]
    for l in energyListOfLists:
        if len(l[0]) < 4:
            filtered.remove(l)

    # orderedEnergies = sorted(energyListOfLists, key=itemgetter(2))
    orderedEnergies = sorted(filtered, key=itemgetter(2))

    # test energy calculation
    # for i in range(len(orderedEnergies)):
    #   print orderedEnergies[i]

    # print allScales


    # all scales that start with C (no loss of generality)
    allCScales = {k: allScales[k] for k in (
        ('C', 'Altered'), ('C', 'Harmonic Minor'), ('C', 'Harmonic Major'), ('C', 'Wholetone'),
        ('C', 'Major'), ('C', 'Augmented'), ('C', 'Octatonic'))}


    # print allCScales
    # print len(allScales)

    orderedOverlap = scalesOrderedByOverlap(allCScales, allScales)



    for i in range(len(orderedOverlap)):
        print orderedOverlap[i]
    ## Then pipe this into text file.

if __name__ == '__main__':
    main()