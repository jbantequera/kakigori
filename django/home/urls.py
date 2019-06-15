from django.urls import path

from . import views
from kakigori_users import views as user_views
from recipes import views as recipes_views

app_name = 'home'

urlpatterns = [
    #HOME
    path('', views.show_feed, name='home'),
    
    #LOGIN y LOGOUT
    path('custom-login/', user_views.custom_login, name='custom-login'),
    path('custom-logout/', user_views.custom_logout, name='custom-logout'),
    path('create-account/', user_views.custom_signup, name='create-user'),
    
    #RECETAS
    path('<str:username>/<int:recipe_id>', recipes_views.view_recipe, name='view_recipe'),
    path('recipes/new', recipes_views.new_recipe, name='new-recipe'),
    path('recipes/vote', recipes_views.vote_recipe, name='vote-recipe'),
    path('recipes/delete', recipes_views.delete_recipe, name='delete-recipe'),
    path('recipes/search/<str:recipe>', recipes_views.search_recipe, name='search-recipe'),
    
    #PERFILES
    path('users/search/<str:profile_name>', user_views.profile_search, name='profile_search'),
    path('<str:username>/followers', user_views.view_profile_followers, name='view_followers'),
    path('<str:username>/followed', user_views.view_profile_followed, name='view_followed'),
    path('<str:username>', user_views.view_profile, name='view-profile'),
    path('users/edit', user_views.edit_profile, name='edit-profile'),
    path('users/follow', user_views.follow_profile, name='follow-profile'),
    path('users/unfollow', user_views.unfollow_profile, name='unfollow-profile'),
    path('users/check/<str:username>', user_views.check_profile_exists, name='check-profile-exists'),
]