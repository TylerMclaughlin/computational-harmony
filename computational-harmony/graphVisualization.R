# graph theoretical exploration of jazz scale harmony
# kudos to: Ognyanova, K. (2017) Network visualization with R. Retrieved from http://kateto.net/network-visualization
# also, to https://matthewlincoln.net/2014/12/20/adjacency-matrix-plots-with-r-and-ggplot2.html

library(igraph)
library(ggplot2)
library(data.table)
library(dplyr)


edge_list_raw <- data.table(read.csv('../edgetable.csv',header = FALSE))
setnames(edge_list_raw,'V1','from')
setnames(edge_list_raw,'V2','to')
setnames(edge_list_raw,'V3','distance')
setnames(edge_list_raw,'V4','common.tones')
setnames(edge_list_raw,'V5','from.root')
setnames(edge_list_raw,'V6','from.scale.type')
setnames(edge_list_raw,'V7','to.root')
setnames(edge_list_raw,'V8','to.scale.type')

edge_list_SIX <- edge_list_raw[distance>5]

graph <- graph.data.frame(edge_list_raw, directed = FALSE)

# Calculate various network properties, adding them as attributes
# to each vertex/node
V(graph)$comm <- membership(optimal.community(graph))
V(graph)$degree <- degree(graph)
V(graph)$closeness <- centralization.closeness(graph)$res
V(graph)$betweenness <- centralization.betweenness(graph)$res
V(graph)$eigen <- centralization.evcent(graph)$vector


# Re-generate dataframes for both vertices and edges, now containing
# calculated network attributes
vertex_list <- get.data.frame(graph, what = "vertices")

# Determine a community for each edge. If two vertices belong to the
# same community, label the edge with that community. If not,
# the edge community value is 'NA'
edge_list <- get.data.frame(graph, what = "edges")
  #%>%
  # inner_join(vertex_list %>% select(name, comm), by = c("from" = "name")) %>%
  # inner_join(vertex_list %>% select(name, comm), by = c("to" = "name")) %>%
  # mutate(group = ifelse(comm.x == comm.y, comm.x, NA) %>% factor())

# Create a character vector containing every vertex name
all_vertices <- sort(vertex_list$name)

# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of vertex names
plot_data <- edge_list %>% mutate(
  to = factor(to, levels = all_vertices),
  from = factor(from, levels = all_vertices))

# Create the adjacency matrix plot
dt <- data.table(plot_data)
unique(dt)
dt[to=='F sharp Major']

ggplot(edge_list_raw) + geom_raster(aes(x=from,y=to,fill=factor(distance)))

edge_list_raw_sort1 <- copy(edge_list_raw)

# Custom sorting
# explain with https://stackoverflow.com/questions/23995285/custom-sorting-in-r
edge_list_raw_sort1$to.scale.type <- factor(edge_list_raw_sort1$to.scale.type,levels=c('Major','Altered','Harmonic Minor','Harmonic Major','Octatonic','Wholetone'))
edge_list_raw_sort1$to.root <- factor(edge_list_raw_sort1$to.root,levels=c('B','E','A','D','G','C','F','B flat','E flat','G sharp','C sharp','F sharp'))
# order first by scale type then scale root
els.1 <- edge_list_raw_sort1[order(edge_list_raw_sort1$to.scale.type,edge_list_raw_sort1$to.root)]


## SUCCESS
plot <- ggplot(els.1) + geom_raster(aes(x=factor(from),y=factor(to),fill=factor(distance)))   
plot + scale_x_discrete(limits=(els.1$from)[order(els.1$from.scale.type,els.1$from.root)]) + scale_y_discrete(limits=(els.1$to)[order(els.1$to.scale.type,els.1$to.root)])

plot <- ggplot(els.1[distance>5]) + geom_raster(aes(x=factor(from),y=factor(to),fill=factor(distance)))   
plot + scale_x_discrete(limits=(els.1$from)[order(els.1$from.scale.type,els.1$from.root)]) + scale_y_discrete(limits=(els.1$to)[order(els.1$to.scale.type,els.1$to.root)])


# making C the root note

els.2 <- copy(edge_list_raw)
els.2$to.scale.type <- factor(els.2$to.scale.type,levels=c('Major','Altered','Harmonic Minor','Harmonic Major','Octatonic','Wholetone'))
els.2$to.root <- factor(els.2$to.root,levels=c('C','F','B flat','E flat','G sharp','C sharp','F sharp','B','E','A','D','G'))
els.2 <- els.2[order(els.2$to.scale.type,els.2$to.root)]

plot <- ggplot(els.2) + geom_raster(aes(x=factor(from),y=factor(to),fill=factor(distance)))   
plot + scale_x_discrete(limits=(els.2$from)[order(els.2$from.scale.type,els.2$from.root)]) + 
  scale_y_discrete(limits=(els.2$to)[order(els.2$to.scale.type,els.2$to.root)]) +
  theme(axis.text.x=element_text(angle=90))
els.2$from.scale.type <- factor(els.2$from.scale.type,levels=c('Major','Altered','Harmonic Minor','Harmonic Major','Octatonic','Wholetone'))
els.2$from.root <- factor(els.2$from.root,levels=c('C','F','B flat','E flat','G sharp','C sharp','F sharp','B','E','A','D','G'))




ggplot(els.1) + geom_raster(aes(x=to.scale.type,y=from.scale.type,fill=factor(distance)))


net <- graph.data.frame(d = edge_list_raw,directed=FALSE)
net4 <- graph.data.frame(d = edge_list_raw[distance>3],directed=FALSE)
net5 <- graph.data.frame(d = edge_list_raw[distance>4],directed=FALSE)
net6 <- graph.data.frame(d = edge_list_raw[distance>5],directed=FALSE)
plot(net6)
plot(net6, edge.arrow.size=.2, edge.color="orange",
     vertex.color="orange", vertex.frame.color="#ffffff",vertex.label=NA) 

plot(net6, edge.arrow.size=.2, edge.color="orange",
     vertex.color=E(net6)$distance, vertex.frame.color="#ffffff",vertex.label=NA) 

plot(net5, edge.arrow.size=.2, edge.color=E(net5)$distance,
     vertex.color="orange", vertex.frame.color="#ffffff",
     vertex.label=NA,layout=layout_randomly) 

ggplot(E(net5)) + geom_raster(aes(x=from,y=to))

ggplot(edge_list_raw[distance>4]) + geom_raster(aes(x=from,y=to,fill=factor(distance)))

make_graph(franklin)

# 
#   theme(
#     # Rotate the x-axis lables so they are legible
#     axis.text.x = element_text(angle = 270, hjust = 0),
#     # Force the plot into a square aspect ratio
#     aspect.ratio = 1,
#     # Hide the legend (optional)
#     legend.position = "none")
# 
