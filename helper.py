import os
import sys
import json
import numpy as np
import networkx as nx
from plotly.utils import PlotlyJSONEncoder

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

def readGraph(path):
    if 'ungraph' in path:
        return nx.read_adjlist(path, nodetype=int)
    return nx.read_adjlist(path, nodetype=int, create_using=nx.DiGraph())

def pathToTitle(path):
    return os.path.basename(path).replace('.txt', '').replace('.ungraph', ' undirected')
