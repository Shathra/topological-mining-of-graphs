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
colorscale = ['#7A4579', '#D56073', 'rgb(236,158,105)', (1, 1, 0.2), (0.98,0.98,0.98)]
# colorscale = [[0, "rgb(8, 29, 88)"], [0.125, "rgb(37, 52, 148)"], [0.25, "rgb(34, 94, 168)"], [0.375, "rgb(29, 145, 192)"], [0.5, "rgb(65, 182, 196)"], [0.625, "rgb(127, 205, 187)"], [0.75, "rgb(199, 233, 180)"], [0.875, "rgb(237, 248, 217)"], [1, "rgb(255, 255, 217)"]]

data = [
    go.Scatter(x=[deg[v] for v in nodes], y=[avgs[v] for v in nodes], mode='markers'),
    go.Histogram2d(
    x=[deg[v] for v in nodes],
    y=[avgs[v] for v in nodes],
    colorscale='YIGnBu',
    zmax=50,
    nbinsx=20,
    nbinsy=20,
    zauto=False,
),
]
# Create a figure
'''
fig = create_2d_density(
    x=[deg[v] for v in nodes], y=[avgs[v] for v in nodes], colorscale=colorscale,
    hist_color='rgb(37, 52, 148)', point_size=3)
'''

layout = go.Layout(
    title=os.path.basename(fpath),
    xaxis=dict( title='Degree', type='log', ticks='', showgrid=False, zeroline=False, nticks=20 ),
    yaxis=dict( title='Avg. Neighbor Degree', type='log', ticks='', showgrid=False, zeroline=False, nticks=20 ),
    autosize=False,
    height=550,
    width=550,
    hovermode='closest',
)
# fig.layout.xaxis.update({'title': 'Degree'})
# fig.layout.yaxis.update({'title': 'Avg. Neighbor Degree'})
fig = go.Figure(data=data, layout=layout)
plot(fig, filename='/tmp/plot.html')

plotlyDumpJson(fig, fpath + '-avg-neighbor-degree')
