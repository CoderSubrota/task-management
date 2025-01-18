from django.shortcuts import render
from django.http import HttpResponse
from tasks.form import TaskModelForm
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

def create_task(request):
    # employees = Employee.objects.all()
    
    form = TaskModelForm()
    if  request.method =="POST":
        form = TaskModelForm(request.POST)
        
        if form.is_valid():
          form.save()
          
        """ For django form """
        
        # form = TaskForm(request.POST, employees=employees)
        # if form.is_valid():
        #     data = form.cleaned_data
        #     title = data.get("title")
        #     description = data.get("description")
        #     due_date = data.get("due_date")
        #     assign_to = data.get("assign_to") 
            
        #     task = Task.objects.create(title=title, description=description,due_date=due_date)

        #     for emp_id in assign_to:
        #         employee = Employee.objects.get(id=emp_id)
        #         task.assign_to.add(employee)
        
        context = {
            "form":form,
            "message":"Task added successfully !!"
        }

        return render(request,"dashboard/task_form.html",context)
                 
    context = {'form':form}
    
    return render(request,"dashboard/task_form.html",context)

