from django.urls import path
from tasks.views import show_tasks,user_information,dashboard

urlpatterns=[
    path('show-tasks/', show_tasks),
    path('users/', user_information),
    path('dashboard/', dashboard)
]

