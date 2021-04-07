from django.shortcuts import render, redirect
from .functions import *
from .forms import *
from .tasks import *
import time
import threading
from threading import Thread

# Create your views here.
def home(request):
    dataToPass = {}
    print("HI")
    if request.POST:
        dataToPass['form'] = uploadFile(request.POST, request.FILES)
        if(dataToPass['form'].is_valid()):
            handle_uploaded_file(request.FILES['network'])
        return redirect('submission/'+request.FILES['network'].name)
    else:
        dataToPass['form'] = uploadFile(auto_id=False)
        return render(request, "index.html", dataToPass)


def submission(request, filename):
    print("before")
    print(filename)
    
    #func1_thread = Thread(target = process)
    
    #while func1_thread.isAlive():
        #render(request, "submission.html")
    time.sleep(5)
    
    return redirect(result)
    #process.delay()
    #print("after")
    #return render(request, "submission.html")


def result(request):
    return render(request, "result.html")