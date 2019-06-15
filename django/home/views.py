# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from itertools import chain
from operator import attrgetter

from recipes.models import Recipe

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
        return render(request, 'users/login.html', {})