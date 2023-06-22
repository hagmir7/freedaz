from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.views.generic import DetailView, UpdateView, UpdateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/dashboard')
            else:
                return redirect('/')
        else:
            return render(request, 'auth/login.html', {'message': 'Username or Password incrrect!'})
    else:
        return render(request, 'auth/login.html')
    

# REGISTER 
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                form.cleaned_data['username']
                new_user.email
                new_user.save()
                if new_user is not None:
                    if new_user.is_active:
                        login(request, new_user)
                        return redirect('/')
                    
                return redirect('login')
    context = {'title': _('Register'), 'form': form, }
    return render(request, 'auth/register.html', context)


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile/profile.html'
    count_hit = True

    def get_context_data(self, *arge, **kwargs):
        context = super(ProfileView, self).get_context_data(*arge, **kwargs)
        page = get_object_or_404(Profile, slug=self.kwargs['slug'])
        title = f'{page.user.first_name} {page.user.last_name}'
        description = _('You can join now to connect with your  friends and enjoy your books and courses register now')
        context["page"] = page
        context['description'] = f'{title} {description}'
        return context



@login_required
def ProfileUpdate(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = UpdateProfile(instance=profile)
    if request.method == "POST":
        if request.user == profile.user:
            form = UpdateProfile(request.POST, instance=request.user.profile, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile_update', id=profile.id)
        else:
            return redirect('/')
        

    context = {
        'page': profile,
        'title': _('Update Profile')
    }

    return render(request, 'profile/update_profile.html', context)

@login_required
class ProfileViewUpdate(UpdateView):
    model = Profile
    template_name = 'profile/update_profile.html'
    form_class = UpdateProfile

    def get_context_data(self, *arge, **kwargs):
        context = super(ProfileViewUpdate, self).get_context_data(*arge, **kwargs)
        page = get_object_or_404(Profile, id=self.kwargs['pk'])
        title = _('Update Profile')
        context["page"] = page
        context["title"] = title
        return context
    
@login_required
def user_update_info(request):
    confirm = False
    if request.method == 'POST':
        form = UserUpdateInfo(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            confirm = True
    else:
        form = UserUpdateInfo(instance=request.user)
    context = {'form': form, 'confirm':confirm, 'title': _("Contact information")}
    return render(request, 'profile/user_update_info.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/change-password.html', {'form': form})





def posword_reset_done(request):
    context = {'title':_("Password reset has been sent")}
    return render(request, 'password_reset/reset_password_done.html', context)


def settings(request):
    return render(request, 'settings.html')


        


