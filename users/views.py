from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm
from django.contrib import messages
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views import View
from django.utils.decorators import method_decorator
User = get_user_model()

# Create your views here.

# Test for users
"""
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        print("views", user_profile)
        context['form'] = self.form_class(
            instance=self.object, userprofile=user_profile)
        return context

    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
"""


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


class SignUpView(View):
    def get(self, request):
        form = CustomRegistrationForm()
        return render(request, 'registration/register.html', {"form": form})

    def post(self, request):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False  
            user.save()
            messages.success(request, 'A confirmation email has been sent. Please check your email.')
            return redirect('sign-in')
        else:
            print("Form is not valid")
        
        return render(request, 'registration/register.html', {"form": form})
    
class SignInView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'registration/login.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


@method_decorator(user_passes_test(login_required,login_url='no-permission'), name='dispatch')
class SignOutView(View):
    def post(self, request):
        logout(request)
        return redirect('sign-in')


class ActivateUser (View):
    def get(self, request, user_id, token):
        try:
            user = User.objects.get(id=user_id)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('sign-in')
            else:
                return HttpResponse('Invalid Id or token')

        except User.DoesNotExist:
            return HttpResponse('User  not found')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')


@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch') 
class AdminDashboardView(View):
    def get(self, request):
        users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()

        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'

        return render(request, 'admin/dashboard.html', {"users": users})

@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class AssignRoleView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id) 
        form = AssignRoleForm()
        return render(request, 'admin/assign_role.html', {"form": form, "user": user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id) 
        form = AssignRoleForm(request.POST)
        
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  
            user.groups.add(role)  
            messages.success(request, f"User  {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

        return render(request, 'admin/assign_role.html', {"form": form, "user": user})


@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch') 
class CreateGroupView(View):
    def get(self, request):
        form = CreateGroupForm()
        return render(request, 'admin/create_group.html', {'form': form})

    def post(self, request):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')

        return render(request, 'admin/create_group.html', {'form': form})
    

@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch') 
class GroupListView(View):
    def get(self, request):
        groups = Group.objects.prefetch_related('permissions').all()
        return render(request, 'admin/group_list.html', {'groups': groups})

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)


""" 

    Admin
        - Sobkisui
    Manager
        - project
        - task create
    Employee
        - Task read
        - Task update
    
    Role Based Access Control (RBAC)
"""