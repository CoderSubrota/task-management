from django import forms
from tasks.models import Task

# class TaskForm(forms.Form):
    
#     title = forms.CharField(max_length=250, label="Title")
#     description = forms.CharField(widget=forms.Textarea, label="Description")
#     due_date=forms.DateField(widget=forms.SelectDateWidget, label="Due date")
#     assign_to= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple ,choices=[], label="Assign to")
    
#     def __init__(self, *args, **kwargs):
#         employees = kwargs.pop('employees', [])
#         super().__init__(*args, **kwargs)
    
#         self.fields['assign_to'].choices = [
#             (emp.id, emp.name) for emp in employees
#         ]
        
class styleMixin:
    default_class='ring-2 ring-indigo-500 flex text-lg flex-col my-4 w-96 rounded-xl pl-2 py-2'
   
    def applyStyleWidget(self):
      for field_name, field in  self.fields.items():
          if isinstance(field.widget,forms.TextInput):
              field.widget.attrs.update({
                  'class':f"{self.default_class}",
                  'placeholder':f'Enter {field.label.lower()}'
              })
          elif isinstance(field.widget,forms.Textarea):
              field.widget.attrs.update({
                  "class":f"{self.default_class} resize-none",
                  'placeholder':f'Enter {field.label.lower()}',
                  'rows':4
              })
              
          elif isinstance(field.widget,forms.SelectDateWidget):
              field.widget.attrs.update({
                  "class":"ring-2 ring-indigo-500 my-4 text-lg font-bold rounded-xl pl-2 mx-2  py-2",
              })     
              
          elif isinstance(field.widget,forms.CheckboxSelectMultiple):
              field.widget.attrs.update({
                  "class":"accent-emerald-500/25 my-3 text-lg",
              })  
              
class TaskModelForm(styleMixin,forms.ModelForm):
    class Meta:
        model = Task 
        fields=['title','description','due_date','assign_to']
        
        widgets={
            'title':forms.TextInput,
            'description':forms.Textarea,
            'due_date':forms.SelectDateWidget,
            'assign_to':forms.CheckboxSelectMultiple
        }
        
        # widgets={
        #     'title':forms.TextInput(attrs={
        #         'class':'ring-2 ring-indigo-500 flex flex-col my-4 w-96 rounded-xl pl-2 py-2',
        #         'placeholder':'Enter meaningful title',
        #         }),
        #     'description':forms.Textarea(
        #         attrs={
        #         'class':'ring-2 ring-indigo-500 flex flex-col  w-96 my-4 rounded-xl pl-2 h-32 px-3  py-2',
        #         'placeholder':'Enter meaningful description'
        #         }
        #     ), 
        #     'due_date':forms.SelectDateWidget(
        #         attrs={
        #         'class':'ring-2 ring-indigo-500 my-4 text-lg font-bold rounded-xl pl-2 mx-2  py-2',
        #         }),
        #     'assign_to':forms.CheckboxSelectMultiple( attrs={
        #         'class':'accent-emerald-500/25 my-3',
        #         })
        # }
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applyStyleWidget()
            
        