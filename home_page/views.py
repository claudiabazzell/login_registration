from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt


def index(request):
    return render(request, 'index.html')


def create(request):
    errors = User.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')

    new_user = User.objects.register(request.POST)
    request.session['user_id'] = new_user.id
    return redirect('/success')


def login(request):
    result = User.objects.authenticate(
        request.POST['email'], request.POST['password'])
    if result == False:
        messages.error(request, "Invalid Email/Password", extra_tags='login')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/success')
    return redirect('/')


def success(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'success.html', context)


def logout(request):
    request.session.clear()

    return redirect('/')
