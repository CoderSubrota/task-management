from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'
    
class NoPermissionView(TemplateView):
    template_name ='no_permission.html'
    
    