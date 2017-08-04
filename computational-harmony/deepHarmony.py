# import chordEnergyJazz/calculateEnergy

cMajor = Scale("C","Major",[0,2,4,5,7,9,11])
cAltered = Scale("C","Altered", [0,1,3,4,6,8,10])
cHarmonic = Scale("C","Harmonic Minor", [0,2,3,5,7,8,11])
cHarmonicMaj = Scale("C","Harmonic Major", [0,2,4,5,7,8,11])

def modz(chord,z=12):
     return [x % z for x in chord]

def isSameChordClass(chord1,chord2,z = 12):
    # chord "species"
    # like pitch class, but with chords.
    myBool = False
    # make sure chord is valid
    chord2 = modz(chord2,z=z)
    for i in range(0,z):
        transposedChord1 = [(x + i) % z for x in chord1]
        if set(chord2) == set(transposedChord1):
            myBool = True

    return myBool


def calculateChordFrequencyInScale(chord,scale):
    # how many major triads in C Major?
    # calculateChordFrequencyInScale([0,2,4],cMajor.getNotes() )
    # returns frequency "3" because CEG, FAC, and GBD are the three major scales
    chord = mod12(chord)
    scale = set(mod12(scale))
    frequency = 0
    for i in range(0,12):
        trialChord = [(x+i)%12 for x in chord]
        trialSet = set(trialChord)
        if trialSet.issubset(scale):
            frequency += 1
    return frequency

cMajorPowerSet = powerset(cMajor.getNotes())


def isDeep(scale,s = 12):
    # s is "subdivisions" (positive integer).  12 for chromatic scale (harmony)
    # may want to do s = 16 or s = 32 for rhythms
    # Returns True if and only if no repeating values, which is the definition of "deep "
    # only looking at intervals not chords
    frequencyList = []
    for x in range(0,int(round(s/2))):  #  rounds up.  yields the range (0,6) for chromatic harmony
        trialInterval = [0, x]
        frequency = 0
        for i in range(0,s):
            transposedInterval = [(y + i) % s for y in trialInterval]
            if set(transposedInterval).issubset(set(scale)):
                frequency += 1
        frequencyList.append(frequency)

    return len(set(frequencyList)) == len(frequencyList) # cardinality == length implies no repeating values



def findDeepSubScales(scale,s=12):
    ps = powerset(scale)
    listOfDeepSubScales = []
    for chord in ps:
        if isDeep(chord,s = s):
            isUnique = True
            for i in listOfDeepSubScales:
                if isSameChordClass(chord,i,z=s):
                    isUnique = False
            if isUnique:
                listOfDeepSubScales.append(chord)
    return listOfDeepSubScales



chromatic = Scale("C","Chromatic",[0,1,2,3,4,5,6,7,8,9,10,11])
findDeepSubScales(chromatic.getNotes())