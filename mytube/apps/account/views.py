from django.shortcuts import render, reverse, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.contrib.auth.views import LoginView


def login(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.get_user()
            print(form.errors.as_data())
            print('user', user)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('video:index'))

    return render(request, 'account/login.html', {'form': form})


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('account:login'))

    return render(request, 'account/register.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('video:index'))
