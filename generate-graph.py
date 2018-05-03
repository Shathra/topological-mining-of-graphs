#!/usr/bin/env python
import os
import sys
import json
import numpy as np
import networkx as nx

args = sys.argv[1:]
if len(args) < 1:
    print('Missing args')
    sys.exit(1)
if len(args) > 2:
    print('Wrong number of arguments: 2 for probabilistic 1 for preferential attachemnt')
    sys.exit(1)

gtype = 'pref'
N = int(args[0], 10)
p = 0
if len(args) == 1:
    gtype = 'prob'
    p = int(args[1], 10)

fpath = gtype + '-' + '-'.join(args)

def generateProbabilistic(N, p):
    G = nx.Graph()
    return G
