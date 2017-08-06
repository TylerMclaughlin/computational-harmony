## TO DO:
## 1) make all chords for a given root (not just C)
## 2) implement multiple key names per dictionary (may be over-optimization)
## 3) be able to traverse network
## 4) build contact matrix with all scales x all scales
## 5) see if numbers ever contradict... they shouldn't
####### i.e., make sure only change are None -> int J and not (int J -> int K != J)
## 6) print which scale degree (3rd, 4th, 9th, 11th, etc) ?
## 7) make scale dict class?
## 8) come up with class that identifies multiple names to single canonical name
###### i.e., accept 'Bb' and 'A sharp' and 'B flat', but always map to 'B flat'
## 9) make more scale functions with self and other, like find common tones.

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

def getCanonicalNoteDictionary():
    noteDict = {}
    for i, v in enumerate(
            ['C', 'C sharp', 'D', 'E flat', 'E', 'F', 'F sharp', 'G', 'G sharp',
             'A', 'B flat', 'B']):
        noteDict[i] = v

    return noteDict


NOTE_DICT = getCanonicalNoteDictionary()

# allow for multiple enharmonic equivalents pointing to same integer
REVERSE_NOTE_DICT = { 'C':0,'C natural':0,'B sharp':0, 'B#':0,'C sharp':1, 'D flat':1, 'C#':1,'Db':1,
                'D':2,'D natural':2,'E flat':3,'D sharp':3,'Eb':3,'D#':3,
                'E natural':4,'F flat':4, 'Fb':4,'F':5,'F natural':5,'E sharp':5, 'E#':5,
                'F sharp':6, 'G flat':6, 'F#':6,'Gb':6,'G':7,'G natural':7,'G sharp':8,'A flat':8,'G#':8,'Ab':8,
                'A':9,'A natural':9,'B flat':10,'A sharp':10, 'Bb':10,'A#':10,
                'B':11,'B natural':11,'C flat':11, 'Cb':11}



def getAsymmetricJazzScales():
    """
    use scales with c as root  (e.g., C_ALTERED and C_MAJOR)to generate all other scales
    with different roots via transposition

    :return: scale dict
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

    :return: scale dict
    """
    symmetricScalesDict = {}
    for scale in [C_WHOLETONE, F_WHOLETONE, C_OCTATONIC, F_OCTATONIC, G_OCTATONIC, C_AUGMENTED, F_AUGMENTED, G_AUGMENTED,
                  BB_AUGMENTED]:
        # scale.testScale()
        symmetricScalesDict[(scale.getRoot(), scale.getType())] = scale.notes
    return symmetricScalesDict



def getMajorScales():
    """

    :return:  scale dict
    """
    majorScalesDict = {}
    for x in CHROMATIC.notes:
        myTemp = [(asdf + x) % 12 for asdf in C_MAJOR.notes]
        majorScalesDict[(NOTE_DICT[x],C_MAJOR.type)] = myTemp
    return majorScalesDict

def getAlteredScales():
    """

    :return: scale dict
    """
    alteredScalesDict = {}
    for x in CHROMATIC.notes:
        myTemp = [(asdf + x) % 12 for asdf in C_ALTERED.notes]
        alteredScalesDict[(NOTE_DICT[x],C_ALTERED.type)] = myTemp
    return alteredScalesDict



def energy(chord, myScalesDict):
    """
    Determine how many scales a chord can belong to.
    This is the "energy" or "entropy"
    :param chord:  list of ints
    :param myScalesDict:  a scales dict
    :return: tuple of int, list of scales
    >>> myEnergy = energy([0,4,7], getAlteredScales())
    """

    counter = 0
    keyList = []
    for key in myScalesDict:
        if set(myScalesDict[key]) & set(chord) == set(chord):
            keyList.append(key)
            counter += 1

    return counter, keyList


def chordListToScaleDict(listOfChords):
    chordDict = {}

    for i in range(0,len(listOfChords)):
        chordDict['scale' + str(i)] = listOfChords[i]

    return chordDict


def chordIntersection(chord1, chord2):
    return list(set(chord1) & set(chord2))



def makeAllChords(setOfPitches = CHROMATIC.notes, rootNote = 'C'):
    """

    :param setOfPitches: list.  Building blocks for chords
    :param rootNote:  str or int.  Root note will be present in all derived chords
    :return:
    """

    if isinstance(rootNote, str):
        firstNote = REVERSE_NOTE_DICT[rootNote]
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
        listOfChords.append(listX)

    return listOfChords


def powerset(myList):
    """"
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    return reduce(lambda result, x: result + [subset + [x] for subset in result], myList, [[]])




def scalesOrderedByOverlap(scaleDict1, scaleDict2):
    """

    :param scaleDict1:
    :param scaleDict2:
    :return: list .  First elements is scale i.  second is scale j.  Third element is list of common tones.
    Fourth element is number of common tones
    >>> myOrderedScales = scalesOrderedByOverlap(getAlteredScales(),getMajorScales())
    """
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
    # sort by column number 3
    orderedIntersection = sorted(intersectionListOfLists, key=itemgetter(3))
    return orderedIntersection




def main():

    allScales = getAsymmetricJazzScales()
    symScales = getSymmetricJazzScales()
    allScales.update(symScales)

    # print allScales
    majorScales = getMajorScales()


    #Cmin7 = [0, 3, 7, 10]
    # print energy(Cmin7,allScales)
    # print energy([0,4,7,11],allScales)

    #allChords = makeAllChords()

    allChords = makeAllChords(rootNote = 0)
    print allChords

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