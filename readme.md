Towards a Topological Graph Theory of Jazz Scales
================
R Tyler McLaughlin
8/22/2017

Table of Contents
-----------------

1.  [Motivation](#motivation)
2.  [Data wrangling in R](#wrangling)
3.  [The Jazz Scale Network Adjacency Matrix](#matrix)
4.  [Python classes and functions for studying musical scales](#classes)
5.  [Method for Building Network of Jazz Scales](#method)

Motivation<a name="motivation" />
---------------------------------

After reading about unsupervised machine learning algorithms, particularly manifold learning, I became very interested in the shapes of data. I wanted to Some reading, I learned how the feature space of natural images is embedded on a Klein bottle, the manifold that is locally 2-dimensional. (Carlsson et al. 2008)

A published in *Science* voice-leading space, chords of N pitches exist on a manifold that is the N-dimensional analog to the 1-D Moebius strip (cite Tymoczko). To explain Chopin's

Data Wrangling<a name="wrangling" />
------------------------------------

### R Libraries

``` r
library(ggplot2)
library(data.table)
```

### Importing the Edge Table Data

``` r
edge_list_raw <- data.table(read.csv('./edgetable.csv',header = FALSE))
setnames(edge_list_raw,'V1','from')
setnames(edge_list_raw,'V2','to')
setnames(edge_list_raw,'V3','distance')
setnames(edge_list_raw,'V4','common.tones')
setnames(edge_list_raw,'V5','from.root')
setnames(edge_list_raw,'V6','from.scale.type')
setnames(edge_list_raw,'V7','to.root')
setnames(edge_list_raw,'V8','to.scale.type')
```

We see that the data is 3186 rows. This means 3186 edges in the graph, which is equal to 57 \* 57 - 57 - 2\*(2 + 1) = 3186

Sorting the Edge List for Plotting
==================================

We want to group all the scales by their type. Within a scale type, we want to order the root notes in a way that makes sense. Let's choose the circle of fifths because this will put neighboring major scales in proximity. This will see what this looks like for the Altered scales, Harmonic Minor scales, etc.

``` r
# safe way to copy a data.table
els <- copy(edge_list_raw)
# set the custom order of the levels of the scale types
els$to.scale.type <- factor(els$to.scale.type,levels=c('Major','Altered','Harmonic Minor','Harmonic Major','Octatonic','Wholetone'))
# set the order of the levels by circle of fifths
els$to.root <- factor(els$to.root,levels=c('C','F','B flat','E flat','G sharp','C sharp','F sharp','B','E','A','D','G'))
# do the same for the "from" levels;
# these will be plotted on the y #axis
els$from.scale.type <- factor(els$from.scale.type,levels=c('Major','Altered','Harmonic Minor','Harmonic Major','Octatonic','Wholetone'))
els$from.root <- factor(els$from.root,levels=c('C','F','B flat','E flat','G sharp','C sharp','F sharp','B','E','A','D','G'))

# order by levels.
els <- els[order(els$to.scale.type,els$to.root)]
els <- els[order(els$to.scale.type,els$to.root)]
```

Plotting the Adjacency Matrix<a name="matrix" />
------------------------------------------------

``` r
plot <- ggplot(els) + geom_raster(aes(x=factor(from),y=factor(to),fill=factor(distance)))   
plot + scale_x_discrete(limits=(els$from)[order(els$from.scale.type,els$from.root)]) + 
  scale_y_discrete(limits=(els$to)[order(els$to.scale.type,els$to.root)]) +
  theme(axis.text.x=element_text(angle=90)) + scale_fill_brewer()
```

![](readme_files/figure-markdown_github/plotting-1.png)

Python classes and functions for studying musical scales<a name="classes" />
----------------------------------------------------------------------------

Created a Scale class to facilitate accessing the non-network properties of a musical scale, like the list of notes, scale type, and the root. Using a class also made easy converting the name and the notes to other data structures, like tuples and dictionaries on the fly.

``` python
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
        
# here are some asymmetrical scales
C_MAJOR = Scale("C", "Major", [0, 2, 4, 5, 7, 9, 11])
C_ALTERED = Scale("C", "Altered", [0, 1, 3, 4, 6, 8, 10])
C_HARMONIC_MAJOR = Scale("C", "Harmonic Major", [0, 2, 4, 5, 7, 8, 11])
C_HARMONIC_MINOR = Scale("C", "Harmonic Minor", [0, 2, 3, 5, 7, 8, 11])
```

Method for Building Network of Jazz Scales<a name="method" />
-------------------------------------------------------------

An adjacency matrix is a common way to represent edges between nodes on a graph.

A list of all edges is sufficient for building an adjacency matrix.

The python code here uses recursion to generate an adjacency matrix for jazz scales. First it starts at C Major, and looks for all scales that share N = 6 common tones with C Major. These scales are: F Major, G Major, C Harmonic Major, C\# Altered, B Altered, and A Harmonic Minor. All of these scales are printed in edgetable.csv, along with N and the set of common tones (for C Major and F Major, this set is \[0, 2, 4, 5, 7, 9\]). Then it looks for all scales that share N = 5 common tones with C Major, including D Major, B flat Major, F octatonic, and ten more scales. It continues to look for the scales relative to C Major, decrementing N until we get to scales that share only two notes with C Major, namely the scales F\# Major, C Altered, and several others.

We are done with the initial step of the recursive algorithm. Next, we actually recurse, and for each the neighboring scales found above, we find its neighbors for integers N less than or equal to 6.

The recursive implementation here was not necessary but was done because it felt very *intuitive* for me as a piano player and composer.
Given C Major, to which scales can we modulate without sounding too avant garde or "Out to Lunch"? B altered sounds great, but Bb altered sounds terrible. Instead of recursion, we could say, for each jazz scale, merely iterate over all other jazz scales and record the number of common tones. This would be implemented with a much simpler nested for loop. You could then sort afterwards. This algorithm would be slightly more efficient (you wouldn't have to check to avoid repeating pairs of scales), but efficiency wasn't really an issue for such a small data set of 57 scales.

References
==========

Carlsson, Gunnar, Tigran Ishkhanov, Vin De Silva, and Afra Zomorodian. 2008. “On the Local Behavior of Spaces of Natural Images.” *International Journal of Computer Vision* 76 (1). Springer: 1–12.