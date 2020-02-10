from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .tasks import send_email
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser


def get_registration(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email.delay(user.email, "Registration confirm", settings.SITE_URL + 'user/confirm/' + str(user.id))
            group = Group.objects.get(name='Users')
            user.groups.add(group)
            messages.success(request, "To verify the data provided we have sent you a confirmation email.")
            return redirect(reverse('index'))
    return render(request, 'users/registration.html', {'form': form})


def get_login(request):
    form = CustomUserLoginForm()
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, "Congratulations! Now you logged in.")
                if "next" in request.GET:
                    return redirect(request.GET['next'])
                return redirect(reverse('index'))
            messages.error(request, "Invalid username or password!")
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

def user_confirm(request, uuid):
    user = CustomUser.objects.filter(id=uuid).first()
    if user:
        user.is_active = True
        user.save()
        messages.success(request, "Now you can login")
        return redirect(reverse('login'))
