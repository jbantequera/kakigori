from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    #HOME
    path('', views.show_feed, name='home'),
    
    #LOGIN y LOGOUT
    path('custom-login/', views.custom_login, name='custom-login'),
    path('custom-logout/', views.custom_logout, name='custom-logout'),
    path('create-account/', views.custom_signup, name='create-user'),
    
    #RECETAS
    path('<str:username>/<int:recipe_id>', views.view_recipe, name='view_recipe'),
    path('recipes/new', views.new_recipe, name='new-recipe'),
    path('recipes/vote', views.vote_recipe, name='vote-recipe'),
    path('recipes/delete', views.delete_recipe, name='delete-recipe'),
    
    #PERFILES
    path('<str:username>', views.view_profile, name='view-profile'),
    path('users/edit', views.edit_profile, name='edit-profile'),
    path('users/follow', views.follow_profile, name='follow-profile'),
    path('users/unfollow', views.unfollow_profile, name='unfollow-profile'),
    path('users/check/<str:username>', views.check_profile_exists, name='check-profile-exists'),
]