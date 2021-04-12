from .models import *
from .functions import *
from background_task import background
import time
import os
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
    

    
    
    
    
    
    
    obj.status = True
    obj.save()

