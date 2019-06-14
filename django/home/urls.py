from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.show_feed, name='show-feed'),
    path('custom-login/', views.custom_login, name='custom-login'),
    path('custom-logout/', views.custom_logout, name='custom-logout'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('<str:username>', views.view_profile, name='view-profile'),
    path('users/follow', views.follow_profile, name='follow-profile'),
    path('users/unfollow', views.unfollow_profile, name='unfollow-profile'),
    path('users/check/<str:username>', views.check_profile_exists, name='check-profile-exists'),
    path('new-recipe/', views.new_recipe, name='new-recipe')
]