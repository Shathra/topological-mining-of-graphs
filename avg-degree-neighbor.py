#!/usr/bin/env python
import os
import sys
import numpy as np
import networkx as nx
from helper import plotlyDumpJson, readGraph
from plotly.figure_factory import create_2d_density

args = sys.argv[1:]
if len(args) == 0:
    print('Missing args')
    sys.exit(1)


fpath = args[0]
G = readGraph(fpath)

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

nodes = G.nodes()
avgs = nx.average_neighbor_degree(G)
deg = G.degree()

# Create custom colorscale
colorscale = ['#7A4579', '#D56073', 'rgb(236,158,105)',
              (1, 1, 0.2), (0.98,0.98,0.98)]

[go.Scatter(x=[deg[v] for v in nodes], y=[avgs[v] for v in nodes], mode='markers')]
# Create a figure
fig = create_2d_density(
    x=[deg[v] for v in nodes], y=[avgs[v] for v in nodes], colorscale=colorscale,
    hist_color='rgb(255, 237, 222)', point_size=3)

# data =
layout = go.Layout(
    title=os.path.basename(fpath),
    xaxis=dict(
        title='Degree',
        autorange=True
    ),
    yaxis=dict(
        title='Avg. Neighbor Degree',
        autorange=True
    )
)
# fig = go.Figure(data=data, layout=layout)
#plot(fig)

plotlyDumpJson(fig, fpath + ' Avg. Degree Neighbor')
