# SKELETON CODE FROM https://docs.djangoproject.com/en/1.10/intro/tutorial01/
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^login$', views.loginView, name='loginView'),
    url(r'^logout$', views.logoutUser, name='logout'),
    url(r'^newaccount$', views.newAccountView, name='newAccountView')
]
