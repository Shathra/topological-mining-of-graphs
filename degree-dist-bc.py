#!/usr/bin/env python
import os
import sys
import json
import numpy as np
from plotly.utils import PlotlyJSONEncoder

args = sys.argv[1:]
if len(args) == 0:
    print('Missing args')
    sys.exit(1)


def plotlyDumpJson(fig, path=None):
    redata = json.loads(json.dumps(fig.data, cls=PlotlyJSONEncoder))
    relayout = json.loads(json.dumps(fig.layout, cls=PlotlyJSONEncoder))

    figData = {'data': redata,'layout': relayout}
    if path is not None:
        path = os.path.basename(path);
        figData['name'] = path
        path = os.path.join('./plotter/src/plots/', path) + '.json'
    plotJson = json.dumps(figData)
    if path is not None:
        with open(path, 'w') as r:
            r.write(plotJson)
    return plotJson

fpath = args[0]
data = [[int(x, 10) for x in line.strip().split('\t')] for line in open(fpath) if line[0] != '#']
degrees = dict()
maxf = 0
maxv = 0
def add_degree(f, t):
    global maxv, maxf, degrees
    if f not in degrees:
        degrees[f] = 1
    else:
        degrees[f] += 1
    if degrees[f] > maxv:
        maxv = degrees[f]
        maxf = f

for e in data:
    add_degree(e[0], e[1])
    add_degree(e[1], e[0])
print(maxf, maxv)

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

bins = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
hist, bin_edges = np.histogram(list(degrees.values()), bins=bins) #550)
print(hist, len(bins), len(hist))
data = [go.Scatter(x=list(bin_edges), y=list(hist))]
layout = go.Layout(
    title=os.path.basename(fpath),
    xaxis=dict(
        type='log',
        autorange=True
    ),
    yaxis=dict(
        type='log',
        autorange=True
    )
)
fig = go.Figure(data=data, layout=layout)
#plot(fig)

plotlyDumpJson(fig, fpath)
