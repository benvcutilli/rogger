from django.conf.urls import url
from settings import views

urlpatterns = [
    url(r'$', views.settings, name="settingsView")
]
