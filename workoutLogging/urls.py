from django.conf.urls import url
from workoutLogging import views
urlpatterns = [
    url(r'new$', views.newEntry),
    url(r'\d+$', views.editEntry),
]
