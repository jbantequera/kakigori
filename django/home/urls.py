from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.show_feed, name='show-feed'),
    url(r'^custom-login/$', views.custom_login, name='custom-login'),
    url(r'^custom-logout/$', views.custom_logout, name='custom-logout'),
]