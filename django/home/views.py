# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def custom_login(request):
    return render(request, "home/login.html", {})

def show_feed(request):
    return render(request, "home/feed.html", {})