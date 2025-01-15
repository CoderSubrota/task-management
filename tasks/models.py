from django.db import models

# Create your models here.
class Task(models.Model):
    # one to many connection 
     project=models.ForeignKey(
         "Project",
         on_delete=models.CASCADE,
         default=1
     )
     title=models.CharField(max_length=255)
     description = models.TextField()
     due_date = models.DateField()
     is_complete = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

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
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    assign_to=models.CharField(max_length=210)
    priority=models.CharField(max_length=1, choices=PRIORITY_OPTIONS,default=LOW)
        

class Project(models.Model):
      name = models.CharField(max_length=352)
      start_date=models.DateField()
      