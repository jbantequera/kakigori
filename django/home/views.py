# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User

from itertools import chain

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
        recipes_followed = Recipe.objects.filter(author__in = request.user.profile.followed.all())
        recipes_own = Recipe.objects.filter(author=request.user.profile)

        recipes = list(chain(recipes_followed, recipes_own))

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

def view_profile(request, username):
    profile = User.objects.get(username=username).profile
    recipes = Recipe.objects.filter(author=profile)

    if profile in request.user.profile.followed.all():
        is_followed = True
    else:
        is_followed = False

    if profile in request.user.profile.followers.all():
        is_following = True
    else:
        is_following = False

    replacements = {
        'profile': profile,
        'is_followed': is_followed,
        'is_following': is_following,
        'recipes': recipes,
    }

    return render(request, 'home/view-profile.html', replacements)

def check_profile_exists(request, username):
    try:
        profile = User.objects.get(username=username).profile

        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})

def follow_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        profile = User.objects.get(username=username).profile

        profile.followers.add(request.user.profile)
        request.user.profile.followed.add(profile)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

def unfollow_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        profile = User.objects.get(username=username).profile

        profile.followers.remove(request.user.profile)
        request.user.profile.followed.remove(profile)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

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

def delete_recipe(request):
    try:
        recipe_id = request.POST.get('recipe_id')
        recipe = request.user.profile.recipe_set.get(id=recipe_id)
        recipe.delete()

        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})