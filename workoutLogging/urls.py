from django.conf.urls import url
from workoutLogging import views
urlpatterns = [
    url(r'new$', views.newEntry, name="newEntryView"),
    url(r'storedate', views.storeDate, name="storeDate"),
    url(r'(\d+)$', views.viewEntry, name="viewEntryView"),
    url(r'(\d+)/commentadd$', views.commentAddView, name="commentAddView"),
    url(r'(\d+)/commentdelete', views.commentDeleteView, name="commentDeleteView")
]
