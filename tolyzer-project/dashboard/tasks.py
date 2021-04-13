from .models import *
from .functions import *
from background_task import background
import time
import os
import copy
from django.core.files.base import ContentFile, File
@background(schedule=1)
def process(task_id):
    print("Task ", task_id, " Received.")
    obj = Submission.objects.get(submission_id = task_id)
    results = Result.objects.get(submission_id = task_id)
    G = read_network(obj.uploaded_file)
    
    print(G)
    print(G.nodes)
    
    get_pyvis_plot(G, task_id)
    
    with open('./static/results/'+str(task_id)+'graph.html') as f:
        results.graph1.save(os.path.basename(f.name),File(f))
        results.save()
    
    
    get_plot_failure(G.copy() ,5, task_id)
    
    get_plot_attack(G.copy(), 5, task_id)
    
    
    
    
    
    
    obj.status = True
    obj.save()

