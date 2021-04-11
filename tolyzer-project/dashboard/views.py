from django.shortcuts import render, redirect 
from .forms import *
from .tasks import *
from .models import *
import time
import threading
from threading import Thread
from multiprocessing import Process
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
    return render(request, "result.html", {'task_id':str(task_id)})