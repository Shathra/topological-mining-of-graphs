#!/usr/bin/env python
import os
import sys
import numpy as np
import networkx as nx
from helper import plotlyDumpJson, readGraph, pathToTitle

args = sys.argv[1:]
if len(args) == 0:
    print('Missing args')
    sys.exit(1)


fpath = args[0]
G = readGraph(fpath)

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

bins = [0, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
hist, bin_edges = np.histogram([v[1] for v in G.degree()], bins=bins) #550)
print(hist, len(bins), len(hist))
data = [go.Scatter(x=list(bin_edges), y=list(hist), name='Directed')]
layout = go.Layout(
    title=pathToTitle(fpath),
    xaxis=dict(
        title='Degree',
        type='log',
        autorange=True
    ),
    yaxis=dict(
        title='Freq',
        type='log',
        autorange=True
    )
)
fig = go.Figure(data=data, layout=layout)
#plot(fig)

plotlyDumpJson(fig, fpath)
