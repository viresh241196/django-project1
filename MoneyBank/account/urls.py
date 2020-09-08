from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('base1', views.base1, name='base1'),
    path('register1', views.register1, name='register1'),
    path('register2', views.register2, name='register2'),
    path('profile', views.profile, name='profile'),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('passbook', views.check_passbook, name="passbook"),
    path('deposit', views.deposit, name="deposit"),
    path('withdraw', views.withdraw, name="withdraw"),
    path('transfer', views.transfer, name="transfer"),
]


