from django.shortcuts import render
from django.http import HttpResponse
from tasks.form import TaskModelForm
from tasks.models import Task
from django.db.models import Q ,Count
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

def tasks(request):
    tasks = Task.objects.all()
    task = Task.objects.get(id=2) 
    # filter_tasks = Task.objects.filter(title='This is', id=2).values() 
    filter_tasks = Task.objects.filter(title='This is').values() 
    and_or = Task.objects.filter(Q(title='Modal title') & Q(id=6))
    and_or2 = Task.objects.filter(Q(title='Modal title') | Q(id=6))
    exclude =  Task.objects.exclude(Q(title='This is title') |  Q(title='dfd'))
    # task_count = Task.objects.annotate(total_task=Count('title')) 
    task_count = Task.objects.aggregate(total_task=Count('id')) 
    icontains = Task.objects.filter(title__icontains='this')
    
    getter_then = Task.objects.filter(id__gt=6)
    less_then = Task.objects.filter(id__lt=10)
    getter_then_equal = Task.objects.filter(id__gte=10)
    less_then_equal = Task.objects.filter(id__lte=10)
    
    context = {
         "tasks":tasks,
         "task":task,
         "filter_tasks":filter_tasks,
         "and_or":and_or,
         "and_or2":and_or2,
         "exclude":exclude,
         "task_count":task_count,
         "icontains":icontains,
         "conditions":{
             "getter_then":getter_then,
             "less_then":less_then,
             "getter_then_equal":getter_then_equal,
             "less_then_equal":less_then_equal
         }
    }
    return render(request,'dashboard/tasks.html',context)

