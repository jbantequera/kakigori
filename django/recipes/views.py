# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from recipes.forms import RecipeForm
from recipes.models import Recipe

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