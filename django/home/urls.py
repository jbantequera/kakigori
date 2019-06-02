from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.custom_login, name='custom_login'),
]