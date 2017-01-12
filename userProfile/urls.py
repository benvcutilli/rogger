# SKELETON CODE FROM https://docs.djangoproject.com/en/1.10/intro/tutorial01/
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'([a-zA-Z0-9_]+)^$', views.userView, name='userView'),
]
