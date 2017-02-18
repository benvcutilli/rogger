from django.conf.urls import url
from settings import views

urlpatterns = [
    url(r'import$', views.importView, name="importView"),
    url(r'$', views.settings, name="settingsView"),
]
