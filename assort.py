import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import seaborn

import plotly.plotly as py


seaborn.set()

# Notebook Variables
dataset_name = "ca-GrQc"
dataset_filepath = "%s.txt" % (dataset_name)
dataset_address = "https://snap.stanford.edu/data/ca-GrQc.txt.gz"

# Download and Extract Dataset

import urllib.request
import gzip
import shutil
import os

filename, header = urllib.request.urlretrieve(dataset_address)

with gzip.open(filename, "rb") as f_in:
    with open(dataset_filepath, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(filename)

# Import Dataset
#G=nx.read_edgelist(dataset_filepath, nodetype=int)
# to import as directed graph
G=nx.read_edgelist(dataset_filepath, nodetype=int, create_using=nx.DiGraph())
print(G.number_of_nodes())
print(G.number_of_edges())

# Generating Random Graphs
n = G.number_of_nodes()
m = G.number_of_edges()

our_Assort = nx.degree_pearson_correlation_coefficient(G)

random_Assort=[]
permuted_Assort = []

for x in range(0, 200):

    p = 2 * m / (n * (n - 1))
    G_random = nx.generators.gnp_random_graph(n, p)

    degree_sequence=list(dict(nx.degree(G)).values())
    G_permute = nx.generators.configuration_model(degree_sequence) # This is not preferential attachment
    G_permute = nx.Graph(G_permute) # Resulting degree_seq is not same, but hopefully similar

    #random_Assort.append(nx.degree_pearson_correlation_coefficient(G_random))
    permuted_Assort.append(nx.degree_pearson_correlation_coefficient(G_permute))

plt.hist(permuted_Assort)
plt.title("Permuted Assortivity Histogram")
plt.xlabel("Assortivity")
plt.ylabel("Frequency")
plt.axvline(x=our_Assort, color='r')
plt._show()