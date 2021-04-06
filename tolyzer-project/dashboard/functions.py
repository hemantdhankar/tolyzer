def test():
    print("Test Successfull")
    
    
def handle_uploaded_file(f):  
    print("hi")
    with open('dashboard/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)
            