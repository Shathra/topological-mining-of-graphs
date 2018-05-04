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
        figData['name'] = path.replace('.txt', '')
        path = os.path.join('./plotter/src/plots/', path) + '.json'
    plotJson = json.dumps(figData)
    if path is not None:
        with open(path, 'w') as r:
            r.write(plotJson)
    return plotJson

def readGraph(path):
    # if 'ungraph' in path:
    return nx.read_adjlist(path, nodetype=int)
    # return nx.read_adjlist(path, nodetype=int, create_using=nx.DiGraph())

def pathToTitle(path):
    return os.path.basename(path).replace('.txt', '').replace('.ungraph', ' undirected')

# Generating Random Graphs

def generate_random(G):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    p = 2 * m / (n * (n - 1))
    # retval = nx.generators.gnp_random_graph(n, p)
    retval = nx.generators.fast_gnp_random_graph(n, p)
    return retval

def generate_power_law(G):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    m = m // n
    retval = nx.generators.random_graphs.barabasi_albert_graph(n, m)
    return retval

def generate_permuted(G):
    degree_sequence=list(dict(nx.degree(G)).values())
    retval = nx.generators.configuration_model(degree_sequence) # This is not preferential attachment
    retval = nx.Graph(retval) # Resulting degree_seq is not same, but hopefully similar
    return retval
