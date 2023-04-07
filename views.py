from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib import messages

def send_email_to_unlock(user):
    # Implement email sending logic here
    pass

def login_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if not user.is_blocked:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Your account has been blocked. Check your email to unlock your account.')
            else:
                user = User.objects.filter(email=email).first()
                if user:
                    user.failed_attempts += 1
                    user.save()
                    if user.failed_attempts >= 3:
                        user.is_blocked = True
                        user.save()
                        send_email_to_unlock(user)
                        messages.error(request, 'Your account has been blocked. Check your email to unlock your account.')

        elif 'register' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use.')
            elif password != password_confirm:
                messages.error(request, 'Passwords do not match.')
            else:
                user = User.objects.create_user(email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully. You can now login.')

    return render(request, 'login.html', {'messages': messages.get_messages(request)})

@login_required
def home(request):
    return HttpResponse('Welcome to the homepage!')

