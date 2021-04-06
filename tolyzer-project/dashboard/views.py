from django.shortcuts import render
from .functions import *
from .forms import *
# Create your views here.
def home(request):
    dataToPass = {}
    print("HI")
    if request.POST:
        dataToPass['form'] = uploadFile(request.POST, request.FILES)
        if(dataToPass['form'].is_valid()):
            handle_uploaded_file(request.FILES['network'])
    else:
        dataToPass['form'] = uploadFile(auto_id=False)
    
    return render(request, "index.html", dataToPass)
