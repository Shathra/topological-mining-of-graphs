#!/usr/bin/env python
import os
import sys
import numpy as np
import networkx as nx
from helper import plotlyDumpJson, readGraph

args = sys.argv[1:]
if len(args) == 0:
    print('Missing args')
    sys.exit(1)


fpath = args[0]
G = readGraph(fpath)

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

def calculateLocalCoef(G):
    for node in G.nodes():
        neigh = list(nx.all_neighbors(G, node))
        cnt = 0
        print(neigh)
        for n1 in neigh:
            for n2 in neigh:
                print(n1, n2)
                if G.has_edge(n1, n2):
                    cnt += 1
        print(node, cnt)
        # sys.exit(0)

calculateLocalCoef(G)
sys.exit(0)
data = [go.Scatter(x=[v[1] for v in G.degree()], y=list(hist))]
layout = go.Layout(
    title=os.path.basename(fpath),
    xaxis=dict(
        title='Degree',
        type='log',
        mode = 'markers',
        autorange=True
    ),
    yaxis=dict(
        title='Freq',
        type='log',
        mode = 'markers',
        autorange=True
    )
)
fig = go.Figure(data=data, layout=layout)
#plot(fig)

plotlyDumpJson(fig, fpath + ' Local Clustering Coef.')
