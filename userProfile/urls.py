# SKELETON CODE FROM https://docs.djangoproject.com/en/1.10/intro/tutorial01/
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^([a-zA-Z0-9_]+)$', views.userView, name='userView'),
    # next line is using a url redirect approach for generating pdfs from the previous version of Rogger, see README for the url to the code for the previous version of Rogger
    url(r'^([a-zA-Z0-9_]+)/week([0-9]*)\.([0-9]*)\.([0-9]*).pdf$', views.weekPDFView, name='weekPDFView'),
]
