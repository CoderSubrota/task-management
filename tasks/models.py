from django.db import models
from django.db.models import DateField
class Employee(models.Model):
    name = models.CharField(max_length=541)
    email=models.EmailField(unique=True, max_length=221)
    
    def __str__(self):
        return self.name
    
    

class Task(models.Model):
    # one to many connection 
     project=models.ForeignKey(
         "Project",
         on_delete=models.CASCADE,
         default=1
     )
     assign_to = models.ManyToManyField(Employee,related_name="tasks")
     title=models.CharField(max_length=255)
     description = models.TextField()
     due_date = models.DateField() 
     is_complete = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
# 22 - 7 = 15 
# due date 20 => 20 > 15 not over due
# 12 < 15 over due 


# one to one  connection
class TaskDetails(models.Model):
    HIGH="H"
    MEDIUM="M"
    LOW="L"
    
    PRIORITY_OPTIONS=(
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'LOW'),
    )
    
    task = models.OneToOneField(
                                Task, 
                                on_delete=models.CASCADE,   
                                related_name="details")
    assign_to=models.CharField(max_length=210)
    priority=models.CharField(max_length=1, choices=PRIORITY_OPTIONS,default=LOW)
        

class Project(models.Model):
      name = models.CharField(max_length=352)
      start_date=models.DateField()
      assign_to = models.ManyToManyField(Employee, related_name='projects')
      
