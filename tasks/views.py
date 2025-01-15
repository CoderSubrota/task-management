from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    # return HttpResponse("This is tasks management system")
    return render(request,'home.html')

def contact(request):
    # return HttpResponse("This is contact page")
    return render(request,'contact.html')

def show_tasks(request):
    return HttpResponse("This is show tasks")

def user_information(request):
    context={
        "title":"This is our users",
        "users":[
             'subrota chandra sarker','rahim','karim','jamal','kamal'
        ]
    }
    return render(request, 'users.html', context)

def dashboard(request):
    
    return render(request, "dashboard/dashboard.html")

