# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from itertools import chain
from operator import attrgetter

from django.contrib.auth import authenticate, login, logout
from base.forms import ProfileForm, RecipeForm, SignupForm
from base.models import Profile, Recipe

# Create your views here.
def custom_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        
    return HttpResponseRedirect(reverse('home:home'))

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect(reverse('home:home'))

def custom_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            
            if form.is_valid():
                new_user = form.save()
                display_name = form.cleaned_data.get('display_name')
                bio = form.cleaned_data.get('bio')
                
                new_user.profile = Profile()
                new_user.profile.display_name = display_name
                new_user.profile.bio = bio
                new_user.profile.save()

                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                
                login(request, user)
                return HttpResponseRedirect(reverse("home:home"))
        else:
            form = SignupForm()
        
        replacements = {
            'form': form
        }

        return render(request, 'home/create-account.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def show_feed(request):
    if request.user.is_authenticated:
        # Obtenemos todas las recetas
        if request.user.profile.followed.all():
            recipes_followed = Recipe.objects.filter(author__in = request.user.profile.followed.all())
            recipes_own = Recipe.objects.filter(author=request.user.profile)

            recipes = sorted(chain(recipes_followed, recipes_own), key=attrgetter('created_at'), reverse=True)
        else:
            recipes = Recipe.objects.all()

        #PAGINACIÓN
        paginator = Paginator(recipes, 10) # Enseñamos 10 recetas por página
        page = request.GET.get('page')
        if page:
            recipes = paginator.get_page(page)
        else:
            recipes = paginator.get_page(1)

        replacements = {
            'page_name': 'Inicio',
            'recipes': recipes,
            'profile': request.user.profile,
        }

        return render(request, "home/feed.html", replacements)
    else:
        return render(request, 'home/login.html', {})

def edit_profile(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        form = ProfileForm(instance = profile)

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)

            if form.is_valid():
                profile = form.save()
                return HttpResponseRedirect(reverse("home:home"))

        replacements = {
            'form': form,
        }

        return render(request, 'home/edit-profile.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def view_profile(request, username):
    if request.user.is_authenticated:
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
    else:
        return HttpResponseRedirect(reverse('home:home'))

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
    if request.user.is_authenticated:
        form = RecipeForm()

        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES)

            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.author = request.user.profile
                recipe.save()
                return HttpResponseRedirect(reverse('home:home'))

        replacements = {
            'form': form,
        }

        return render(request, 'recipes/new_recipe.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def view_recipe(request, username, recipe_id):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        recipe = user.profile.recipe_set.get(pk=recipe_id)
        total_votes = recipe.votes_up + recipe.votes_down

        if (recipe.author == request.user.profile):
            is_own = True
        else:
            is_own = False
        
        if recipe.voters.filter(user = request.user).exists():
            has_voted = True
        else:
            has_voted = False

        replacements = {
            'profile': user.profile,
            'recipe': recipe,
            'has_voted': has_voted,
            'is_own': is_own,
            'total_votes': total_votes,
        }

        return render(request, 'recipes/view_recipe.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def vote_recipe(request):
    if request.user.is_authenticated:
        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)
        
        if not recipe.voters.filter(user = request.user).exists():
            recipe_id = request.POST.get('recipe_id')
            vote_up = request.POST.get('vote_up')

            if vote_up == 'true':
                recipe.votes_up = recipe.votes_up + 1
            else:
                recipe.votes_down = recipe.votes_down + 1

            recipe.voters.add(request.user.profile)
            recipe.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        return HttpResponseRedirect(reverse('home:home'))

def delete_recipe(request):
    try:
        recipe_id = request.POST.get('recipe_id')
        recipe = request.user.profile.recipe_set.get(id=recipe_id)
        recipe.delete()

        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})

def view_profile_followers(request, username):
    if request.user.is_authenticated:
        profile = User.objects.get(username=username).profile
        followers = profile.followers.all()

        replacements = {
            'page_name': 'Seguidores de ' + profile.display_name,
            'profile_list': followers,
        }

        return render(request, 'home/profile-list.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def view_profile_followed(request, username):
    if request.user.is_authenticated:
        profile = User.objects.get(username=username).profile
        followed = profile.followed.all()

        replacements = {
            'page_name': 'Seguidos por ' + profile.display_name,
            'profile_list': followed,
        }

        return render(request, 'home/profile-list.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def profile_search(request, profile_name):
    if request.user.is_authenticated:
        profiles = Profile.objects.filter(display_name__icontains=profile_name)

        replacements = {
            'page_name': 'Búsqueda de Usuarios',
            'profile_list': profiles
        }

        return render(request, 'home/profile-list.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def search_recipe(request, recipe):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(name__icontains=recipe)

        paginator = Paginator(recipes, 10) # Enseñamos 10 recetas por página
        page = request.GET.get('page')
        
        if page:
            recipes = paginator.get_page(page)
        else:
            recipes = paginator.get_page(1)

        replacements = {
            'page_name': 'Búsqueda de Recetas',
            'recipes': recipes,
        }

        return render(request, "home/feed.html", replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))