# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from base.forms import ProfileForm, RecipeForm
from base.models import Profile, Recipe

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
        # Obtenemos todas las recetas
        recipes = Recipe.objects.filter(author__in = request.user.profile.followed.all())

        replacements = {
            'recipes': recipes,
            'profile': request.user.profile,
        }

        return render(request, "home/feed.html", replacements)
    else:
        return render(request, 'home/login.html', {})

def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile = form.save()
            return HttpResponseRedirect(reverse("home:show-feed"))

    replacements = {
        'form': form,
    }

    return render(request, 'home/edit-profile.html', replacements)

def new_recipe(request):
    form = RecipeForm()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user.profile
            recipe.save()
            return HttpResponseRedirect(reverse('home:show-feed'))

    replacements = {
        'form': form,
    }

    return render(request, 'recipes/new_recipe.html', replacements)