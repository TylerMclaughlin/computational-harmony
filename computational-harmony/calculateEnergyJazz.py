## TO DO:
## 1) make all chords for a given root (not just C)  DONE
## 2) implement multiple key names per dictionary (may be over-optimization)  DONE
## 3) be able to recursively traverse network  DONE
## 4) build contact matrix with all scales x all scales  DONE
## 5) see if numbers ever contradict... they shouldn't
####### i.e., make sure only change are None -> int J and not (int J -> int K != J)
## 6) print which scale degree (3rd, 4th, 9th, 11th, etc) ?
## 7) make scale dict class?
## 8) come up with class that identifies multiple names to single canonical name
###### i.e., accept 'Bb' and 'A sharp' and 'B flat', but always map to 'B flat'
## 9) make more scale functions with self and other, like find common tones.
## 10)  Incorporate scale type into exported CSV



#import itertools as it

import csv
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

    def getTupleName(self):
        tuple_name = (self.root, self.type)
        return tuple_name

    def asDict(self):
        output_dict = {}
        output_dict[self.getTupleName()] = self.notes
        return output_dict

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
BB_AUGMENTED = Scale("B flat", "Augmented", [1, 2, 5, 6, 9, 10])

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

def convertToCanonicalName(note_name):
    """

    :param note_name: string
    :return:  string
     >>> convertToCanonicalName('G flat')
     Out: 'F sharp'
    """
    pitch_int = REVERSE_NOTE_DICT[note_name]

    return NOTE_DICT[pitch_int]



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

def getAllScales():
    """

    :return: scale dict
    """
    allScales = getAsymmetricJazzScales()
    symScales = getSymmetricJazzScales()
    allScales.update(symScales)

    return allScales

ALL_JAZZ_SCALES = getAllScales()


def getMajorScales():
    """returns a dictionary of scales, with one key for every major scale
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
    """Determine how many scales a chord can belong to.
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


def allScalesGivenRoot(scale_root):
    """

    :param scale_root: string
    :return: scale dict
    """

    scale_root = convertToCanonicalName(scale_root)

    # first add all asymmetric scales
    allScales = getAllScales()
    all_rooted_scales = {k: allScales[k] for k in ( (scale_root, 'Major'),(scale_root, 'Altered'), (scale_root, 'Harmonic Minor'), (scale_root, 'Harmonic Major') )}
    pitch_int = REVERSE_NOTE_DICT[scale_root] # integer of the scale_root
    # augmented scales
    if pitch_int % 4 == 0:
        all_rooted_scales.update(C_AUGMENTED.asDict())
    elif pitch_int % 4 == 1:
        all_rooted_scales.update(F_AUGMENTED.asDict())
    elif pitch_int % 4 == 2:
        all_rooted_scales.update(BB_AUGMENTED.asDict())
    else:
        all_rooted_scales.update(G_AUGMENTED.asDict())
    # octatonic scales
    if pitch_int % 3 == 0:
        all_rooted_scales.update(C_OCTATONIC.asDict())
    elif pitch_int % 3 == 1:
        all_rooted_scales.update(G_OCTATONIC.asDict())
    else:
        all_rooted_scales.update(F_OCTATONIC.asDict())
    # whole tone scales
    if pitch_int % 2 == 0:
        all_rooted_scales.update(C_WHOLETONE.asDict())
    else:
        all_rooted_scales.update(F_WHOLETONE.asDict())


    return all_rooted_scales


def printLOL(list_of_lists,min_common_tones = 0):
    for i in range(len(list_of_lists)):
        if list_of_lists[i][3] >= min_common_tones:
            print list_of_lists[i]

def nextScaleAsDict(scales_list):
    """
    will take one list from list of lists result and convert it to a dict
    :param scales_list:  list.  First element is scale tuple.  Second element is Scale tuple.
    Third element is list of notes, last element is number of common tones.
    :return: Simple Dict with one key/value pair.
    """
    scale_dict = {}
    scale_dict[scales_list[1]] = ALL_JAZZ_SCALES[scales_list[1]]
    return scale_dict

def appendUniquePairs(running_list,list_of_lists):
    for i in list_of_lists:
        current_pair = (i[0],i[1])
        running_list.append(current_pair)


def pairIsNew(running_list,list_from_lol):
    curr_tuple = (list_from_lol[0],list_from_lol[1])
    if  curr_tuple in set(running_list):
        return False
    else:
        return True

def testFullCovering(unique_pairs):
    """
    Looks to see if all scales have been incorporated into the network.
    :param unique_pairs: list of tuples of tuples.  first variable output by recursive function below
    Prints the percent coverage of the network.
    """
    all_lol = scalesOrderedByOverlap(ALL_JAZZ_SCALES, ALL_JAZZ_SCALES)
    lal = len(all_lol)
    count = lal
    for list in all_lol:
        if (list[0],list[1]) not in unique_pairs:
            count -= 1
            print (list[0],list[1])
    print "total graph coverage is " + str(count / float(lal) * 100) + "%"




def recursivelyExploreScaleSpace(starting_scale, allScales, depth, min_common_tones, unique_pairs,output):
    """

    :param starting_scale: scale dict
    :param allScales:  scale dict (all scales you want to consider in exploration)
    :param depth: int.   number of searches
    :param unique_pairs = [].  list of unique pairs of jazz scales.  Avoids redundant recursion.
    :param output = []
    :return: None
    """

    current_nbhd = scalesOrderedByOverlap(starting_scale,allScales) # list of lists, "scale neighborhood"
    current_nbhd = [x for x in current_nbhd if x[3] >= min_common_tones]
    #printLOL(current_nbhd)
    #print "unique pairs ", unique_pairs
    #print "depth ", depth
    if depth != 0:                  # stops recursion when depth gets to 0
        #print len(current_nbhd)
        for neighboring_scale in current_nbhd:
            if neighboring_scale[3] >= min_common_tones:
                #print "sufficient common tones"
                if pairIsNew(unique_pairs,neighboring_scale):    # make sure we only explore new edges
                    output.append(neighboring_scale)
                    ###print neighboring_scale
                    #print "and pair is new"
                    unique_pairs.append((neighboring_scale[0],neighboring_scale[1]))  # add all scale-scale edges to current_nbhd
                    ns_dict = nextScaleAsDict(neighboring_scale)
                    recursivelyExploreScaleSpace(ns_dict, allScales, depth-1, min_common_tones,unique_pairs,output)
                #else:
                    #print "but pair is NOT new"
    return unique_pairs, output



def main():



    majorScales = getMajorScales()


    #Cmin7 = [0, 3, 7, 10]
    # print energy(Cmin7,allScales)
    # print energy([0,4,7,11],allScales)


    allChords = makeAllChords(rootNote = 0)


    energyListOfLists = [0] * len(allChords)
    i = 0
    for chord in allChords:
        myEnergy, myKeyList = energy(chord, ALL_JAZZ_SCALES)
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


    # let's see a glimpse of the local topology, starting at scales that start with C
    # all scales with C as a root
    allCScales = allScalesGivenRoot('C')
    ordered_c_scales_overlap = scalesOrderedByOverlap(allCScales, ALL_JAZZ_SCALES)
    #printLOL(ordered_c_scales_overlap)
    a,b = recursivelyExploreScaleSpace(C_MAJOR.asDict(), getMajorScales(), depth=5, min_common_tones=1, unique_pairs=[],output = [])


    c, d = recursivelyExploreScaleSpace(C_MAJOR.asDict(), ALL_JAZZ_SCALES, depth=7, min_common_tones=1,
                                        unique_pairs=[], output=[])
    testFullCovering(c)

    with open('edgetable.csv','wb') as csvfile:
        my_writer = csv.writer(csvfile,delimiter=',')
        for row in d:
            from_name = ' '.join(map(str, row[0]))
            to_name = ' '.join(map(str, row[1]))
            from_root = row[0][0]
            from_scale_type = row[0][1]
            to_root = row[1][0]
            to_scale_type = row[1][1]
            my_writer.writerow([from_name,to_name,row[3],row[2],from_root,from_scale_type,to_root,to_scale_type])


if __name__ == '__main__':
    main()