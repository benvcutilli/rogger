"""rogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from shared import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('homepage.urls')),
    url(r'^about', include('about.urls')),
    url(r'^users/', include('userProfile.urls')),
    url(r'^workouts/', include('workoutLogging.urls')),
    url(r'^settings', include('settings.urls')),
    url(r'^search', views.search, name='search')
]

handler400 = 'shared.views.error400View'
handler403 = 'shared.views.error403View'
handler404 = 'shared.views.error404View'
handler500 = 'shared.views.error500View'
