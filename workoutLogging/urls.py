from django.conf.urls import url
from workoutLogging import views
urlpatterns = [
    url(r'new$', views.newEntry, name="newEntryView"),
    url(r'(\d+)$', views.editEntry, name="editEntryView"),
    url(r'view$', views.viewEntry, name="viewEntryView"),
]
