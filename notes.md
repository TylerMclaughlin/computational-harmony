# computational-harmony

Goals:

1)  What does the network of jazz scales look like when plotted as an adjacency matrix?  How do we permute the rows to best visualize its organization?

2)  What are the properties of the graph?
    a) Is the graph planar?    I.e., can it be embedded in 2 dimensions with no crossing edges?
    b) Are subgraphs planar?
    b) For supergraphs that are not planar, what is the general topology?

# Application to music

Mathematical tools for studying musical scales and chords to benefit the composer, jazz musician, producer, and music theorist.  One can examine which neighboring scales.  Alternatively, the improviser can determine the shortest path to get from F Major to the C whole tone scale, for example.  

# Application to data science

Network theory is ubiquitous in data science.   Less represented, yet perhaps equally important, is is topolical theory of manifolds.  Topology is especially useful to the data scientist when the dataset is large and high dimensional (Lum, P. Y., et al. "Extracting insights from the shape of complex data using topology." Scientific reports 3 (2013): 1236.). 

Applied topology has found use in robotics and data science with the self-organizing map.



### Planarity

A graph is planar if it can be drawn in the plane.  (reference Richard Trudeau)

One can easily see that the graph of Major scales plus altered scales is planar.

Addition of the set of Harmonic major scales violates planarity.


# notes on network

Euler's second formula:  If G is a connected graph then 

![](https://latex.codecogs.com/svg.latex?V&space;-&space;E&space;&plus;&space;F&space;=&space;2&space;-&space;2*G) 

v - e + f = 2 - 2*g

theorem 21 (Trudeau text):  If G is connected with v >= 3 and genus g then

![](https://latex.codecogs.com/svg.latex?G&space;\geq&space;\frac{1}{6}*E&space;-&space;\frac{1}{2}(V-2))


For the <b>full</b> jazz scale network of the 57 unique scales, the number of edges 

![](https://latex.codecogs.com/svg.latex?E&space;=&space;\frac&space;{57&space;*&space;57&space;-&space;57}{2}&space;=&space;1596)

Old calculation to get R data-table length:  
e =  (57 * 57  - 2 - 4) / 2 - 57.


We are subtracting 57 because we want to exclude self-interactions, like C Major to C Major.  We subtract 2 because we wish to discard C wholetone -> F wholetone and its reverse, F wholetone -> C wholetone.  Distinct wholetone scales do not have common tones.  Subtracting 4 because there are two pairs of augmented scales with no common tones:  C augmented <-> B flat augmented and F augmented <-> G augmented.  Lastly, we divide the first term by two to consider only half of the off-diagonal matrix.  

inspecting the number of rows in the data.table in R yields 3186 rows. This is derived from 57 * 57 - 57 - 4 - 2.

Divide by two to get 1593 edges.

g >= 1593/6 - 55/2 = 238.  The genus of the graph is at least 238.  238 tori glued together.  It could potentially be a lot larger.

Let's consider the network of neighboring scales.

els.2[distance>5] 
>>> 288

There are no diagonal elements, so we are safe to divide this by two to get the number of edges, e = 144.

Applying the theorem, with e = 144 and v = 57,

g >= 1/6*(144) - (1/2)*(v-2) = -3.5.

We know from inspection, that the genus is > 0, so this formula does not help.

If we extend the to network to include edges that share 5 or 6 common tones, we have e = 468 (treating edges the same, ignoring the difference in common tones).  v does not change, yielding g >= 1/6*468 - 1/2*(57-2) = 50.5















