# These two imports may have been automatically supplied by Django's "startproject"
# [79, "startproject"]. "django" package is by [94].
from django.conf.urls import url, include
from django.contrib import admin

from shared import views
# Provided by [94]
from django.urls import path




# This variable was probably already here (it's likely from when "startproject"[] was run) as well
# as the first call to url(). Not sure if subsequent calls to url() were copy-pasted and modified
# from the first call.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('homepage.urls')),
    url(r'^about', include('about.urls')),
    url(r'^users/', include('userProfile.urls')),
    url(r'^workouts/', include('workoutLogging.urls')),
    url(r'^settings', include('settings.urls')),
    url(r'^search', views.search, name='search'),
    path("protected/profilepicture/<int:primarykey>", views.fetchProfilePicture, name="profilePicture"),
    path("protected/thumbnail/<int:primarykey>", views.fetchThumbnail, name="thumbnail")
]

handler400 = 'shared.views.error400View'
handler403 = 'shared.views.error403View'
handler404 = 'shared.views.error404View'
handler500 = 'shared.views.error500View'
