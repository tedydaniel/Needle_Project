#  Name: 
#  Author: rotem.tal
#  Description:
#

import networkx as nx
from matplotlib.pyplot import *
g = nx.read_adjlist("tfid")
nx.draw(g, with_labels=True)
show()