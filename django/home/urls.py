from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    #HOME
    path('', views.show_feed, name='show-feed'),
    
    #LOGIN y LOGOUT
    path('custom-login/', views.custom_login, name='custom-login'),
    path('custom-logout/', views.custom_logout, name='custom-logout'),
    
    #RECETAS
    path('<str:username>/<int:recipe_id>', views.view_recipe, name='view_recipe'),
    path('new-recipe/', views.new_recipe, name='new-recipe'),
    path('recipes/vote', views.vote_recipe, name='vote-recipe'),
    
    #PERFILES
    path('<str:username>', views.view_profile, name='view-profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('users/follow', views.follow_profile, name='follow-profile'),
    path('users/unfollow', views.unfollow_profile, name='unfollow-profile'),
    path('users/check/<str:username>', views.check_profile_exists, name='check-profile-exists'),
]