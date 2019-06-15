# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from kakigori_users.forms import ProfileForm, SignupForm
from kakigori_users.models import Profile
from recipes.models import Recipe

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

        return render(request, 'users/create-account.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

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

        return render(request, 'users/edit-profile.html', replacements)
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

        return render(request, 'users/view-profile.html', replacements)
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

def view_profile_followers(request, username):
    if request.user.is_authenticated:
        profile = User.objects.get(username=username).profile
        followers = profile.followers.all()

        replacements = {
            'page_name': 'Seguidores de ' + profile.display_name,
            'profile_list': followers,
        }

        return render(request, 'users/profile-list.html', replacements)
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

        return render(request, 'users/profile-list.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))

def profile_search(request, profile_name):
    if request.user.is_authenticated:
        profiles = Profile.objects.filter(display_name__icontains=profile_name)

        replacements = {
            'page_name': 'Búsqueda de Usuarios',
            'profile_list': profiles
        }

        return render(request, 'users/profile-list.html', replacements)
    else:
        return HttpResponseRedirect(reverse('home:home'))