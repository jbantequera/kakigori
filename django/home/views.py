# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

# Create your views here.
def custom_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        
    return HttpResponseRedirect(reverse('home:show-feed'))

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect(reverse('home:show-feed'))

def show_feed(request):
    if request.user.is_authenticated:
        return render(request, "home/feed.html", {})
    else:
        return render(request, 'home/login.html', {})