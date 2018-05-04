#!/usr/bin/env python
import os
import sys
import numpy as np
import networkx as nx
from helper import plotlyDumpJson, pathToTitle, readGraph, generate_random

args = sys.argv[1:]
if len(args) == 0:
    print('Missing args')
    sys.exit(1)


fpath = args[0]
G = readGraph(fpath)

bins = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]

colorscale = [
    [0, 'rgb(250, 250, 250)'],        #0
    [1./10000, 'rgb(200, 200, 200)'], #10
    [1./1000, 'rgb(150, 150, 150)'],  #100
    [1./100, 'rgb(100, 100, 100)'],   #1000
    [1./10, 'rgb(50, 50, 50)'],       #10000
    [1., 'rgb(0, 0, 0)'],             #100000
]

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

deg = nx.degree(G)
coef = nx.clustering(G)
x = [deg[v] for v in G.nodes()]
y = [coef[v] for v in G.nodes()]

# rG = generate_random(G)
# rdeg = nx.degree(rG)
# rcoef = nx.clustering(rG)
# rx = [rdeg[v] for v in rG.nodes()]
# ry = [rcoef[v] for v in rG.nodes()]
mx = max(x)
print('maxx', mx)
mx = max(max(y), mx)
print('maxx', mx)
bins = [v for v in bins if v <= mx]
H, bx, by = np.histogram2d(x=x, y=y, bins=[bins, 10])
zmax = np.amax(H)

data = [
    # go.Scatter(x=bx, y=by, color=H, mode='markers'),
    go.Heatmap(x=bx, y=by, z=H, colorscale=colorscale, zauto=False, zmax=zmax),
]

# data = [go.Scatter(x=x, y=y, mode='markers'), go.Scatter(x=rx, y=ry, mode='markers')]
layout = go.Layout(
    title=pathToTitle(fpath) + '-clustering-coef',
    xaxis=dict(
        title='Degree',
        type='log',
        autorange=True
    ),
    yaxis=dict(
        title='Clustering Coef.',
        # type='log',
        autorange=True
    ),
    autosize=False,
    height=550,
    width=550,
    hovermode='closest',
)
fig = go.Figure(data=data, layout=layout)
#plot(fig)

plotlyDumpJson(fig, fpath + '-clustering-coef')
