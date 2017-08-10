# graph theoretical exploration of jazz scale harmony
# kudos to https://matthewlincoln.net/2014/12/20/adjacency-matrix-plots-with-r-and-ggplot2.html
 

library(igraph)
library(ggplot2)
library(data.table)
library(dplyr)


edge_list_raw <- data.table(read.csv('../edgetable.csv',header = FALSE))
setnames(edge_list_raw,'V1','from')
setnames(edge_list_raw,'V2','to')
setnames(edge_list_raw,'V3','distance')
setnames(edge_list_raw,'V4','common.tones')

edge_list_SIX <- edge_list_raw[distance>5]

graph <- graph.data.frame(edge_list_raw, directed = FALSE)

# Calculate various network properties, adding them as attributes
# to each node/vertex
V(graph)$comm <- membership(optimal.community(graph))
V(graph)$degree <- degree(graph)
V(graph)$closeness <- centralization.closeness(graph)$res
V(graph)$betweenness <- centralization.betweenness(graph)$res
V(graph)$eigen <- centralization.evcent(graph)$vector


# Re-generate dataframes for both nodes and edges, now containing
# calculated network attributes
node_list <- get.data.frame(graph, what = "vertices")

# Determine a community for each edge. If two nodes belong to the
# same community, label the edge with that community. If not,
# the edge community value is 'NA'
edge_list <- get.data.frame(graph, what = "edges") %>%
  # inner_join(node_list %>% select(name, comm), by = c("from" = "name")) %>%
  # inner_join(node_list %>% select(name, comm), by = c("to" = "name")) %>%
  # mutate(group = ifelse(comm.x == comm.y, comm.x, NA) %>% factor())

# Create a character vector containing every node name
all_nodes <- sort(node_list$name)

# Adjust the 'to' and 'from' factor levels so they are equal
# to this complete list of node names
plot_data <- edge_list %>% mutate(
  to = factor(to, levels = all_nodes),
  from = factor(from, levels = all_nodes))

# Create the adjacency matrix plot
dt <- data.table(plot_data)
unique(dt)
dt[to=='F sharp Major']

ggplot(edge_list_raw) + geom_raster(aes(x=from,y=to,fill=factor(distance)))

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
