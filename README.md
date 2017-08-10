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
