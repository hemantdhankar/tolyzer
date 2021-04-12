import networkx as nx
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network
from bokeh.plotting import show

import hvplot.networkx as hvnx
import holoviews as hv
from holoviews import opts

def test():
    print("Test Successfull")
    
    
def handle_uploaded_file(f):  
    print("hi")
    with open('dashboard/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)

def read_network(filename):
    print("ok",filename.name[-3:])
    if(filename.name[-3:]=="csv"):
        df = pd.read_csv(filename)
        Graphtype = nx.Graph()
        G = nx.from_pandas_edgelist(df, edge_attr='weight', create_using=Graphtype)
        return G
    elif(filename.name[-3:]=="gml"):
        try:
            G = nx.read_gml(filename)
        except:
            G = nx.read_gml(filename,label="id")
        return G

def get_holo_plot(G, task_id):
    hv.extension('bokeh')
    defaults = dict(width=800, height=800,bgcolor='rgba(0,0,0,0)',xaxis=None,yaxis=None,show_frame=False)
    hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))
    padding = dict(x=(-1.1, 1.1), y=(-1.1, 1.1))
    plot_holo=hv.Graph.from_networkx(G, nx.layout.fruchterman_reingold_layout, k=1).opts(tools=['hover','tap'],
                                                                            node_size=10,
                                                                            edge_line_color="#1d92fd",
                                                                            edge_line_width=0.65,
                                                                            toolbar=None,
                                                                            )
    hv.save(plot_holo,"./static/results/"+str(task_id)+"graph.html")


def get_pyvis_plot(G, task_id):
    g=Network(height=1000,width=1000,notebook=False,bgcolor="#AARRGGBB",font_color='white')
    g.barnes_hut()
    g.from_nx(G)
    g.save_graph("./static/results/"+str(task_id)+"graph.html")