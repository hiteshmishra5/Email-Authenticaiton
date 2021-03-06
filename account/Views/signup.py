from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import uuid
from account.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

#creating view
@login_required(login_url='/')
def home(request):
    return render(request, 'base.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail')
            return redirect('/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Invalid username or Password')
            return redirect('/login')
        if user:
            return redirect('/inside_login')

    return render(request, 'base.html')


def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
                messages.success(request,'Username is Taken.')
                return redirect('/signup')
            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is Taken.')
                return redirect('/signup')

            user_obj = User(username = username, email = email, password = password)
            user_obj.password = make_password(user_obj.password)
            user_obj.save()
            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            print(profile_obj)
            return redirect('token_send')
        except Exception as e:
            print(e)
    return render(request, 'signup.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified!')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified!')
            return redirect('/success')
        else:
            return redirect('/login')
    except Exception as e:
        print(e)
        return redirect('/login')


def error_page(request):
    return render(request, 'inside_login.html')

def send_mail_after_registration(email, token):
    subject = 'Your account need to be verified'
    message = f'Hi paste the link to verified the account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_link = [email]
    send_mail(subject, message, email_from, recipient_link)

