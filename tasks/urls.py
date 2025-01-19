from django.urls import path
from tasks.views import show_tasks,user_information,create_task,dashboard,tasks

urlpatterns=[
    path('show-tasks/', show_tasks),
    path('users/', user_information),
    path('dashboard/', dashboard),
    path('create_task/', create_task),
    path('tasks/', tasks),
]

