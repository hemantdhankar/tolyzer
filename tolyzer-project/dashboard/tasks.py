from .models import *
from .functions import *
from background_task import background
import time
import os
import copy
from django.core.files.base import ContentFile, File
import json


@background(schedule=1)
def process(task_id):
    print("Task ", task_id, " Received.")
    obj = Submission.objects.get(submission_id = task_id)
    results = Result.objects.get(submission_id = task_id)
    G = read_network(obj.uploaded_file)
    
    print(G)

    info = general_properties(G)
    results.nodes = info['Nodes']
    results.edges = info['Edges']
    results.average_degree = info['ad']
    results.cpl = info['cpl']
    results.diameter = info['Diameter']
    results.density = info['density']
    
    c_bc, c_d = top_5_crucial_nodes(G.copy())
    results.top_5_bc_nodes = json.dumps(c_bc)
    results.top_5_degree_nodes = json.dumps(c_d)

    results.failure_tolerance = get_failure_score_tol(G.copy())
    results.attack_tolerance = get_attack_score_tol(G.copy())
    results.save()
    
    plot_histo(G.copy(), task_id)
    get_pyvis_plot(G.copy(), task_id)
    
    recommend_graph(G.copy(),task_id,5)
    
    with open("./static/results/" + str(task_id)+"recommend.gml") as f:
        results.recommended_file.save(os.path.basename(f.name),File(f))
        results.save()
    
    
    get_plot_failure(G.copy() ,5, task_id)
    
    get_plot_attack(G.copy(), 5, task_id)
    
    
    
    
    
    
    obj.status = True
    obj.save()

