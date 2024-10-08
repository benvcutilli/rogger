# This code may be based off the code found at [98, Write your first view]/[98,
# other spots], but with modifications to work with this specfic Django app
# within the array in the defintion of urlpatterns. The first section of import
# statements may apply to this, as well as the defintion of the "urlpatterns"
# variable (however, the stuff inside the list that initialized urlpatterns was
# almost certainly written by me)

# Ben doesn't use this anymore
#from django.conf.urls import url
from settings import views

# Used below; read comment for it there. Importing [94].
import django.urls



urlpatterns = [
    # This next URL supports importing Merv[70]-exported data:
    django.urls.re_path(r'import$', views.importView, name="importView"),
    # URL for deleting (see the datamanagement(...) function's comment) and exporting data (the URL
    # after it is just for exporting; again, revelvant comments for that line can be found above
    # views.export)
    django.urls.path("/datamanagement", views.datamanagement, name="scram"),
    django.urls.path("/datamanagement/dump", views.export, name="export"),
    django.urls.re_path(r'$', views.settings, name="settingsView"),
]
