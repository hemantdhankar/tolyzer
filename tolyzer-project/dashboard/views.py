from django.shortcuts import render, redirect 
from .forms import *
from .tasks import *
from .models import *
import time
import json
import threading
from threading import Thread
from multiprocessing import Process
from django.conf import settings
from django.http import HttpResponse, Http404

# Create your views here.
def home(request):
    dataToPass = {}
    print("HI")
    if request.POST:
        form = uploadFile(request.POST, request.FILES)
        dataToPass['form'] = form
        
        if(dataToPass['form'].is_valid()):
            task = Submission()
            task.uploaded_file = request.FILES['network']
            task.status = False
            task.save()
        
            task_id = task.submission_id
            result = Result()
            result.submission_id = task
            result.save()
            filename = request.FILES['network'].name

            process(task_id)
            
        return redirect('submission/'+str(task_id))        
    else:
        dataToPass['form'] = uploadFile(auto_id=False)
        return render(request, "index.html", dataToPass)


def submission(request, task_id):
        if request.POST:
            obj = Submission.objects.get(submission_id = task_id)
            print(obj.status)
            if(obj.status == False):
                return render(request,"submission.html")
            else:
                return redirect(result, task_id)
        else:
            return render(request, "submission.html")
    
    
def result(request, task_id):
    print(task_id)
    if(request.POST):
        return redirect(download, task_id)
    else:
        results = Result.objects.get(submission_id = task_id)
        jsonDec = json.decoder.JSONDecoder()
        top_5_degree_nodes = jsonDec.decode(results.top_5_degree_nodes)
        top_5_bc_nodes = jsonDec.decode(results.top_5_bc_nodes)
        return render(request, "result.html", {'task_id':str(task_id), 'nodes':results.nodes, 'edges':results.edges,
                                                'diameter':results.diameter, 'cpl':results.cpl, 'average_degree':results.average_degree,
                                                'density': results.density, 'top_5_degree_nodes':top_5_degree_nodes, 'top_5_bc_nodes':top_5_bc_nodes,
                                                'attack_tolerance': results.attack_tolerance, 'failure_tolerance':results.failure_tolerance})
    
    

from django.http import FileResponse
def download(request, task_id):
    results = Result.objects.get(submission_id = task_id)
    file_path = results.recommended_file.path
    response = FileResponse(open(file_path, 'rb'))
    return response
    """
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    """