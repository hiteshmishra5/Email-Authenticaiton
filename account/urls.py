from django.contrib import admin
from django.urls import path
from .Views import signup
urlpatterns = [
    path('' , signup.home, name = 'home'),
    path('signup',signup.Signup,name = 'signup'),
    path('login', signup.Login, name = 'login'),
    path('success',signup.success,name = 'success'),
    path('token',signup.token_send,name = 'token_send'),
    path('verify/<auth_token>',signup.verify, name = 'verify'),
    path('inside_login', signup.error_page, name = 'inside_login'),
]
