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
import seaborn as sns

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
    g=Network(height=800,width=900,notebook=False,bgcolor="#AARRGGBB",font_color='white')
    g.barnes_hut()
    g.from_nx(G)
    g.inherit_edge_colors(True)
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
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white') 
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Characteristic Path Length")
        ax.plot(plt_x,plt_y_pl, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"cpl_f.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white') 
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Relative Size of Largest Cluster")
        ax.plot(plt_x,plt_y_lc, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"lcs_f.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white') 
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')
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
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white') 
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Characteristic Path Length")
        ax.plot(plt_x,plt_y_pl, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"cpl_a.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white') 
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Relative Size of Largest Cluster")
        ax.plot(plt_x,plt_y_lc, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"lcs_a.png", transparent=True)
    with plt.style.context('classic'):
        plt.figure(figsize=(8,8))
        ax=plt.axes()
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white') 
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.set_xlabel("Fraction of Nodes Deleted")
        ax.set_ylabel("Average Size of Isolated Cluster")
        ax.plot(plt_x,plt_y_aic, '#10febd', marker='o', markersize=10,linewidth=2)
        plt.savefig("./static/results/" + str(task_id)+"ics_a.png", transparent=True)


def general_properties(G):
    d={}
    d["Nodes"]=round(G.number_of_nodes(), 3)
    d["Edges"]=round(G.number_of_edges(), 3)
    d["Diameter"]=round(nx.diameter(G), 3)
    d["cpl"]=round(nx.average_shortest_path_length(G), 3)
    d["ad"]=round(d["Edges"]/d["Nodes"], 3)
    d["density"]=round(nx.density(G), 3)
    return d


def top_5_crucial_nodes(G):
    bc=nx.betweenness_centrality(G)
    c_bc=sorted(bc, key=bc.get, reverse=True)[:5]
    d=list(G.degree())
    d.sort(key=lambda tup:tup[1],reverse=True)
    c_d=[]
    for i in range(5):
        c_d.append(d[i][0])
    return c_bc,c_d


def score_attack(G):
    initial_no_of_nodes=G.number_of_nodes()
    intial_apl=nx.average_shortest_path_length(G)
    x=G.degree()
    x=dict(x)
    G_copy=G.copy()
    deleted_nodes=0
    while(True):
        print(deleted_nodes)
        if(G_copy.number_of_nodes()==0):
            print("No Isolated Clusters Detected")
            break
        else:
            node_to_delete=max(x.items(), key=operator.itemgetter(1))[0]
            for ne in list(G_copy.neighbors(node_to_delete)):
                x[ne]-=1
            del x[node_to_delete]
            deleted_nodes+=1
            G_copy.remove_node(node_to_delete)
            if(nx.is_connected(G_copy)):
                G=G_copy.copy()
            else:
                final_apl=nx.average_shortest_path_length(G)
                final_no_of_nodes=G_copy.number_of_nodes()
                degree_dist=dict(G_copy.degree())
                break
    return degree_dist,initial_no_of_nodes,final_no_of_nodes,intial_apl,final_apl


def score_failure(G):
    initial_no_of_nodes=G.number_of_nodes()
    intial_apl=nx.average_shortest_path_length(G)
    nodes=list(G.nodes)
    G_copy=G.copy()
    deleted_nodes=0
    while(True):
        print(deleted_nodes)
        if(G_copy.number_of_nodes()==0):
            print("No Isolated Clusters Detected")
            break
        else:
            node_to_delete=random.choice(nodes)
            nodes.remove(node_to_delete)
            G_copy.remove_node(node_to_delete)
            deleted_nodes+=1
            if(nx.is_connected(G_copy)):
                G=G_copy.copy()
            else:
                final_apl=nx.average_shortest_path_length(G)
                final_no_of_nodes=G_copy.number_of_nodes()
                degree_dist=dict(G_copy.degree())
                break
    return degree_dist,initial_no_of_nodes,final_no_of_nodes,intial_apl,final_apl


def plot_histo(G, task_id):
    dda,inona,fnona,iapla,fapla=score_attack(G.copy())
    ddf,inonf,fnonf,iaplf,faplf=score_failure(G.copy())
    ddn=degree_dist=dict(G.degree())
    l1=list(dda.values())
    l2=list(ddf.values())
    l3=list(ddn.values())
    l1=pd.DataFrame(l1)
    l1.loc[:,0]
    l2=pd.DataFrame(l2)
    l2.loc[:,0]
    l3=pd.DataFrame(l3)
    l3.loc[:,0]
    plt.figure(figsize=(15,8), dpi= 120)
    ax=plt.axes()
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white') 
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    sns.kdeplot(l1.loc[:,0], shade=True, color="r", label="Degree Distribution - Attack", alpha=.5)
    sns.kdeplot(l2.loc[:,0], shade=True, color="#7270fe", label="Degree Distribution - Failure", alpha=.5)
    sns.kdeplot(l3.loc[:,0], shade=True, color="#10febd", label="Degree Distribution - Normal", alpha=.5)


    # Decoration
    plt.title('Degree Distribution - Attack vs Failure vs Normal')
    plt.xlabel("Degree")
    plt.ylabel("P(k)")
    plt.legend()
    plt.savefig("./static/results/" + str(task_id)+"multi_histo.png",transparent=True)


def get_failure_score_tol(G):
    dd,inon,fnon,iapl,fapl=score_failure(G)
    non_score=((inon-fnon)/inon)*100
    print("F",non_score)
    return round(non_score,1)

def get_attack_score_tol(G):
    dd,inon,fnon,iapl,fapl=score_attack(G)
    non_score=((inon-fnon)/inon)*100
    print("A",non_score)
    return round(non_score,1)


def recommend_graph(G,task_id, ne_add_seed=5):
    bc,d=top_5_crucial_nodes(G)
    cru_nodes=bc+d
    cru_nodes=list(set(cru_nodes))
    nodes=list(G.nodes())
    for i in range(len(cru_nodes)):
        backup_node=str(cru_nodes[i])+"_back"
        G.add_node(backup_node)
        for ne in list(G.neighbors(cru_nodes[i])):
            G.add_edge(backup_node,ne)
        for ne in range(ne_add_seed):
            for i in range(10):
                node_to_add=random.choice(nodes)
                if(not G.has_edge(backup_node,node_to_add)):
                    break
            G.add_edge(backup_node,node_to_add)
    nx.write_gml(G, "./static/results/" + str(task_id)+"recommend.gml")
    return