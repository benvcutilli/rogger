# This code may be based off the code found at [98, Write your first view]/[98,
# other spots], but with modifications to work with this specfic Django app
# within the array in the defintion of urlpatterns.

from django.conf.urls import url
from settings import views

urlpatterns = [
    # This next URL supports importing Merv[70]-exported data:
    url(r'import$', views.importView, name="importView"),
    url(r'$', views.settings, name="settingsView"),
]
