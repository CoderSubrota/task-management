from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView
# Class Based View Re-use example


class Greetings(View):
    greetings = 'Hello Everyone'

    def get(self, request):
        return HttpResponse(self.greetings)


class HiGreetings(Greetings):
    greetings = 'Hi Everyone'


class HiHowGreetings(Greetings):
    greetings = 'Hi Everyone, How are you'


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


def is_employee(user):
    return user.groups.filter(name='Manager').exists()

@method_decorator(user_passes_test(is_manager, login_url='no-permission'),name="dispatch")
class ManagerDashboardView(View):
    template_name = "dashboard/manager-dashboard.html"

    def get(self, request, *args, **kwargs):
        counts = Task.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING')),
        )

        type = request.GET.get('type', 'all')
        base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

        if type == 'completed':
            tasks = base_query.filter(status='COMPLETED')
        elif type == 'in-progress':
            tasks = base_query.filter(status='IN_PROGRESS')
        elif type == 'pending':
            tasks = base_query.filter(status='PENDING')
        else: 
            tasks = base_query.all()

        context = {
            "tasks": tasks,
            "counts": counts,
            "role": 'manager'
        }
        return render(request, self.template_name, context)
    
@method_decorator(user_passes_test(is_employee), name="dispatch")
class EmployeeDashboardView(View):
    template_name = "dashboard/user-dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required,name="dispatch")
@method_decorator(permission_required("tasks.add_task", login_url='no-permission'),name="dispatch")
class TaskCreateView(CreateView):
    template_name = "task_form.html"
    form_class = TaskModelForm 
    task_detail_form_class = TaskDetailModelForm

    def get(self, request, *args, **kwargs):
        task_form = self.get_form()
        task_detail_form = self.task_detail_form_class()
        context = {
            "task_form": task_form,
            "task_detail_form": task_detail_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = self.get_form()
        task_detail_form = self.task_detail_form_class(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            # Save the task
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create-task')  # Redirect to the desired URL after success

        context = {
            "task_form": task_form,
            "task_detail_form": task_detail_form,
        }
        return render(request, self.template_name, context)

# variable for list of decorators
create_decorators = [login_required, permission_required(
    "tasks.add_task", login_url='no-permission')]


@method_decorator(login_required,name="dispatch")
@method_decorator(permission_required("tasks.add_task", login_url='no-permission'),name="dispatch")
class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """ For creating task """
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    """ 
    0. Create Task
    1. LoginRequiredMixin
    2. PermissionRequiredMixin
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get(
            'task_detail_form', TaskDetailModelForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(
                task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)

@method_decorator(login_required,name="dispatch")
@method_decorator(permission_required("tasks.change_task", login_url='no-permission'),name="dispatch")
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        # print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(
                instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)


@method_decorator(login_required,name="dispatch")
@method_decorator(permission_required("tasks.delete_task", login_url='no-permission'),name="dispatch")
class DeleteTaskView(View):
    def post(self, request, id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)  # Safely get the task or return a 404
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')

    def get(self, request, id, *args, **kwargs):
        messages.error(request, 'Invalid request method. Please use POST to delete a task.')
        return redirect('manager-dashboard')

@method_decorator(login_required,name="dispatch")
@method_decorator(permission_required("tasks.view_task", login_url='no-permission'),name="dispatch")
class ViewTaskView(View):
    template_name = "show_task.html"

    def get(self, request, *args, **kwargs):
        projects = Project.objects.annotate(
            num_task=Count('task')
        ).order_by('num_task')
        return render(request, self.template_name, {"projects": projects})

view_project_decorators = [login_required, permission_required(
    "projects.view_project", login_url='no-permission')]


@method_decorator(view_project_decorators, name='dispatch')
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(
            num_task=Count('task')).order_by('num_task')
        return queryset



@method_decorator(login_required(login_url='no-permission'), name='dispatch')
@method_decorator(permission_required("tasks.view_task", login_url='no-permission'), name='dispatch')
class TaskDetailsView(View):
    template_name = 'task_details.html'
    def get(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, id=task_id)  
        status_choices = Task.STATUS_CHOICES
        return render(request, self.template_name, {"task": task, 'status_choices': status_choices})

    def post(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, id=task_id)  
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

class TaskDetail(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # {"task": task}
        # {"task": task, 'status_choices': status_choices}
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)


@method_decorator(login_required, name="dispatch")
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if is_manager(request.user):
            return redirect('manager-dashboard')
        elif is_employee(request.user):
            return redirect('user-dashboard')
        elif is_admin(request.user):
            return redirect('admin-dashboard')
        else:
            return redirect('home')