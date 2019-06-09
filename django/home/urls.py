from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.show_feed, name='show-feed'),
    path('custom-login/', views.custom_login, name='custom-login'),
    path('custom-logout/', views.custom_logout, name='custom-logout'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('new-recipe/', views.new_recipe, name='new-recipe')
]