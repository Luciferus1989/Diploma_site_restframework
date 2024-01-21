from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django import forms
from django.http import HttpResponse, HttpRequest
from django.views import View
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view

from .models import CustomUser


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['login'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('frontend:index')
        else:
            pass

    return render(request, 'frontend/signIn.html')


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return redirect('frontend:index')


@api_view(['POST'])
class RegisterView(View):
    template_name = 'frontend/signUp.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name)
        group = Group.objects.get(name='Users')
        user.groups.add(group)

        login(request, user)

        return redirect(reverse_lazy('frontend:index'))


