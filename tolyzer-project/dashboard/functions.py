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
import matplotlib.path as mpath
import operator
from operator import itemgetter
import itertools

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
    defaults = dict(width=700, height=700,bgcolor='rgba(0,0,0,0)',show_frame=False)
    hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))
    padding = dict(x=(0, 0), y=(0, 0))
    plot_holo=hv.Graph.from_networkx(G, nx.layout.fruchterman_reingold_layout, k=1).opts(tools=['hover','tap'],
                                                                            node_size=10,
                                                                            edge_line_color="#1d92fd",
                                                                            edge_line_width=0.65,
                                                                            
                                                                            )
    hv.save(plot_holo,"./static/results/"+str(task_id)+"graph.html")


def get_pyvis_plot(G, task_id):
    g=Network(height=700,width=900,notebook=False,bgcolor="#AARRGGBB",font_color='white')
    g.barnes_hut()
    g.from_nx(G)
    g.inherit_edge_colors(True)
    g.set_options(''' var options={"edges":{"width":10}} ''')
    g.save_graph("./static/results/"+str(task_id)+"graph.html")
    
    
def failure_graph(graph_object,percentage_of_nodes_of_failure):
    total_nodes=graph_object.number_of_nodes()
    number_of_nodes_to_delete=int((percentage_of_nodes_of_failure*total_nodes)/100)
    nodes=list(graph_object.nodes)
    deleted_nodes=0
    plot_x=[]
    plot_y_pl=[] 
    plot_y_lc=[]
    plot_y_aic=[]
    invl=(total_nodes*(percentage_of_nodes_of_failure/100))//20
    if(invl==0):
        for i in range(number_of_nodes_to_delete):
            print(deleted_nodes)
            node_to_delete=random.choice(nodes)
            nodes.remove(node_to_delete)
            graph_object.remove_node(node_to_delete)
            deleted_nodes+=1
            plot_x.append(deleted_nodes/total_nodes)
            #average path length
            apl=[]
            compo=[]
            nxcss=nx.connected_components(graph_object)
            for C in (graph_object.subgraph(c).copy() for c in nxcss):
                compo.append(list(C.nodes()))
                apl.append(nx.average_shortest_path_length(C))
            plot_y_pl.append(max(apl))
            #relative size of largest Cluster
            largest_cc = max(compo, key=len)
            plot_y_lc.append(len(largest_cc)/graph_object.number_of_nodes())
            #average size of isolated Clusters
            icl=[]
            for clu in compo:
                icl.append(len(clu))
            plot_y_aic.append(np.mean(icl))
        return plot_x,plot_y_pl,plot_y_lc,plot_y_aic
    else:
        for i in range(number_of_nodes_to_delete):
            print(deleted_nodes)
            node_to_delete=random.choice(nodes)
            nodes.remove(node_to_delete)
            graph_object.remove_node(node_to_delete)
            deleted_nodes+=1
            if(deleted_nodes%invl==0):
                plot_x.append(deleted_nodes/total_nodes)
                #average path length
                apl=[]
                compo=[]
                nxcss=nx.connected_components(graph_object)
                for C in (graph_object.subgraph(c).copy() for c in nxcss):
                    compo.append(list(C.nodes()))
                    apl.append(nx.average_shortest_path_length(C))
                plot_y_pl.append(max(apl))
                #relative size of largest Cluster
                largest_cc = max(compo, key=len)
                plot_y_lc.append(len(largest_cc)/graph_object.number_of_nodes())
                #average size of isolated Clusters
                icl=[]
                for clu in compo:
                    icl.append(len(clu))
                plot_y_aic.append(np.mean(icl))
        return plot_x,plot_y_pl,plot_y_lc,plot_y_aic

def attack_graph(graph_object,percentage_of_nodes_of_attack):
    total_nodes=graph_object.number_of_nodes()
    number_of_nodes_to_delete=int((percentage_of_nodes_of_attack*total_nodes)/100)
    deleted_nodes=0
    plot_x=[]
    plot_y_pl=[]
    plot_y_lc=[]
    plot_y_aic=[]
    invl=int((total_nodes*(percentage_of_nodes_of_attack/100))/20)
    # print(invl)
    if(invl==0):
        x=graph_object.degree()
        x=dict(x)
        print(x)
        for i in range(number_of_nodes_to_delete):
            print(deleted_nodes)
            # print(x)
            node_to_delete=max(x.items(), key=operator.itemgetter(1))[0]
            # print(node_to_delete,type(node_to_delete))
            # print(list(G.neighbors(node_to_delete)))
            for ne in list(graph_object.neighbors(node_to_delete)):
                # print(ne)
                x[ne]-=1
            del x[node_to_delete]
            graph_object.remove_node(node_to_delete)
            deleted_nodes+=1

            plot_x.append(deleted_nodes/total_nodes)
            #average path length
            apl=[]
            compo=[]
            nxcss=nx.connected_components(graph_object)
            for C in (graph_object.subgraph(c).copy() for c in nxcss):
                compo.append(list(C.nodes()))
                apl.append(nx.average_shortest_path_length(C))
            plot_y_pl.append(max(apl))
            #relative size of largest Cluster
            largest_cc = max(compo, key=len)
            plot_y_lc.append(len(largest_cc)/graph_object.number_of_nodes())
            #average size of isolated Clusters
            icl=[]
            for clu in compo:
                icl.append(len(clu))
            plot_y_aic.append(np.mean(icl))
        return plot_x,plot_y_pl,plot_y_lc,plot_y_aic

    else:
        x=graph_object.degree()
        x=dict(x)
        print(x)
        for i in range(number_of_nodes_to_delete):
            print(deleted_nodes)
            # print(x)
            node_to_delete=max(x.items(), key=operator.itemgetter(1))[0]
            # print(node_to_delete,type(node_to_delete))
            # print(list(G.neighbors(node_to_delete)))
            for ne in list(graph_object.neighbors(node_to_delete)):
                # print(ne)
                x[ne]-=1
            del x[node_to_delete]
            graph_object.remove_node(node_to_delete)
            deleted_nodes+=1

            if(deleted_nodes%invl==0):
                plot_x.append(deleted_nodes/total_nodes)
                #average path length
                apl=[]
                compo=[]
                nxcss=nx.connected_components(graph_object)
                for C in (graph_object.subgraph(c).copy() for c in nxcss):
                    compo.append(list(C.nodes()))
                    apl.append(nx.average_shortest_path_length(C))
                plot_y_pl.append(max(apl))
                #relative size of largest Cluster
                largest_cc = max(compo, key=len)
                plot_y_lc.append(len(largest_cc)/graph_object.number_of_nodes())
                #average size of isolated Clusters
                icl=[]
                for clu in compo:
                    icl.append(len(clu))
                plot_y_aic.append(np.mean(icl))
        return plot_x,plot_y_pl,plot_y_lc,plot_y_aic


def get_plot_failure(G,percentage_of_nodes_to_failure, task_id):
    plt_x,plt_y_pl,plt_y_lc,plt_y_aic=failure_graph(G,percentage_of_nodes_to_failure)
    print(plt_y_aic)
    star = mpath.Path.unit_regular_star(100)
    circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
    verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star = mpath.Path(verts, codes)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('#1d92fd')
        ax.spines['top'].set_color('#1d92fd') 
        ax.spines['right'].set_color('#1d92fd')
        ax.spines['left'].set_color('#1d92fd')
        ax.tick_params(axis='x', colors='#1d92fd')
        ax.tick_params(axis='y', colors='#1d92fd') 
        ax.yaxis.label.set_color('#1d92fd')
        ax.xaxis.label.set_color('#1d92fd')
        ax.title.set_color('#1d92fd')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Characteristic Path Length")
        ax.plot(plt_x,plt_y_pl, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"cpl_f.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('#1d92fd')
        ax.spines['top'].set_color('#1d92fd') 
        ax.spines['right'].set_color('#1d92fd')
        ax.spines['left'].set_color('#1d92fd')
        ax.tick_params(axis='x', colors='#1d92fd')
        ax.tick_params(axis='y', colors='#1d92fd') 
        ax.yaxis.label.set_color('#1d92fd')
        ax.xaxis.label.set_color('#1d92fd')
        ax.title.set_color('#1d92fd')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Relative Size of Largest Cluster")
        ax.plot(plt_x,plt_y_lc, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"lcs_f.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('#1d92fd')
        ax.spines['top'].set_color('#1d92fd') 
        ax.spines['right'].set_color('#1d92fd')
        ax.spines['left'].set_color('#1d92fd')
        ax.tick_params(axis='x', colors='#1d92fd')
        ax.tick_params(axis='y', colors='#1d92fd') 
        ax.yaxis.label.set_color('#1d92fd')
        ax.xaxis.label.set_color('#1d92fd')
        ax.title.set_color('#1d92fd')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Average Size of Isolated Cluster")
        ax.plot(plt_x,plt_y_aic, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"ics_f.png", transparent=True)



def get_plot_attack(G,percentage_of_nodes_to_attack, task_id):
    plt_x,plt_y_pl,plt_y_lc,plt_y_aic=attack_graph(G,percentage_of_nodes_to_attack)
    star = mpath.Path.unit_regular_star(100)
    circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
    verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star = mpath.Path(verts, codes)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('#1d92fd')
        ax.spines['top'].set_color('#1d92fd') 
        ax.spines['right'].set_color('#1d92fd')
        ax.spines['left'].set_color('#1d92fd')
        ax.tick_params(axis='x', colors='#1d92fd')
        ax.tick_params(axis='y', colors='#1d92fd') 
        ax.yaxis.label.set_color('#1d92fd')
        ax.xaxis.label.set_color('#1d92fd')
        ax.title.set_color('#1d92fd')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Characteristic Path Length")
        ax.plot(plt_x,plt_y_pl, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"cpl_a.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('#1d92fd')
        ax.spines['top'].set_color('#1d92fd') 
        ax.spines['right'].set_color('#1d92fd')
        ax.spines['left'].set_color('#1d92fd')
        ax.tick_params(axis='x', colors='#1d92fd')
        ax.tick_params(axis='y', colors='#1d92fd') 
        ax.yaxis.label.set_color('#1d92fd')
        ax.xaxis.label.set_color('#1d92fd')
        ax.title.set_color('#1d92fd')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Relative Size of Largest Cluster")
        ax.plot(plt_x,plt_y_lc, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"lcs_a.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('#1d92fd')
        ax.spines['top'].set_color('#1d92fd') 
        ax.spines['right'].set_color('#1d92fd')
        ax.spines['left'].set_color('#1d92fd')
        ax.tick_params(axis='x', colors='#1d92fd')
        ax.tick_params(axis='y', colors='#1d92fd') 
        ax.yaxis.label.set_color('#1d92fd')
        ax.xaxis.label.set_color('#1d92fd')
        ax.title.set_color('#1d92fd')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Average Size of Isolated Cluster")
        ax.plot(plt_x,plt_y_aic, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"ics_a.png", transparent=True)


