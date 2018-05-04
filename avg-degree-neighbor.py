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
bins = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
colorscale = ['#7A4579', '#D56073', 'rgb(236,158,105)', (1, 1, 0.2), (0.98,0.98,0.98)]

colorscale = [
        ['rgb(250, 250, 250)', 0],        #0
        ['rgb(200, 200, 200)', 1./256], #10
        ['rgb(150, 150, 150)', 1./128],  #100
        ['rgb(100, 100, 100)', 1./64],   #1000
        ['rgb(50, 50, 50)', 1./32],       #10000
        ['rgb(25, 25, 25)', 1./16],       #10000
        ['rgb(10, 10, 10)', 1./8],       #10000
        ['rgb(0, 0, 0)', 1.],             #100000
    ]
colorscale = [
    [0, 'rgb(250, 250, 250)'],        #0
    [1./10000, 'rgb(200, 200, 200)'], #10
    [1./1000, 'rgb(150, 150, 150)'],  #100
    [1./100, 'rgb(100, 100, 100)'],   #1000
    [1./10, 'rgb(50, 50, 50)'],       #10000
    [1., 'rgb(0, 0, 0)'],             #100000
]
'''
colorscale = [
    ['rgb(165,0,38)', 0.0],
    ['rgb(215,48,39)', 0.1111111111111111],
    ['rgb(244,109,67)', 0.2222222222222222],
    ['rgb(253,174,97)', 0.3333333333333333],
    ['rgb(254,224,144)', 0.4444444444444444],
    ['rgb(224,243,248)', 0.5555555555555556],
    ['rgb(171,217,233)', 0.6666666666666666],
    ['rgb(116,173,209)', 0.7777777777777778],
    ['rgb(69,117,180)', 0.8888888888888888],
    ['rgb(49,54,149)', 1.0],
]
'''
# colorscale = [[0, "rgb(8, 29, 88)"], [0.125, "rgb(37, 52, 148)"], [0.25, "rgb(34, 94, 168)"], [0.375, "rgb(29, 145, 192)"], [0.5, "rgb(65, 182, 196)"], [0.625, "rgb(127, 205, 187)"], [0.75, "rgb(199, 233, 180)"], [0.875, "rgb(237, 248, 217)"], [1, "rgb(255, 255, 217)"]]
x=[deg[v] for v in nodes]
y=[avgs[v] for v in nodes]
mx = max(x)
print('maxx', mx)
mx = max(max(y), mx)
print('maxx', mx)
bins = [v for v in bins if v <= mx]
H, bx, by = np.histogram2d(x=x, y=y, bins=bins)
zmax = np.amax(H)

data = [
    # go.Scatter(x=bx, y=by, color=H, mode='markers'),
    go.Heatmap(x=bx, y=by, z=H, colorscale=colorscale, zauto=False, zmax=zmax),
#     go.Histogram2d(
#     x=x,
#     y=y,
#     # colorscale=colorscale,
#     zmax=90,
#     nbinsx=20,
#     nbinsy=20,
#     zauto=False,
# ),
]
# Create a figure
'''
fig = create_2d_density(
    x=x, y=y, colorscale=colorscale,
    hist_color='rgb(37, 52, 148)', point_size=3)
'''
layout = go.Layout(
    title=os.path.basename(fpath + '-avg-neighbor-degree').replace('.txt', ''),
    xaxis=dict( title='Degree', type='log', ticks='', showgrid=False, zeroline=False, autorange=True),
    yaxis=dict( title='Avg. Neighbor Degree', type='log', ticks='', showgrid=False, zeroline=False, autorange=True),
    autosize=False,
    height=550,
    width=550,
    hovermode='closest',
)
# fig.layout.xaxis.update({'title': 'Degree'})
# fig.layout.yaxis.update({'title': 'Avg. Neighbor Degree'})
fig = go.Figure(data=data, layout=layout)
# plot(fig, filename='/tmp/plot.html')

plotlyDumpJson(fig, fpath + '-avg-neighbor-degree')
