
#from django.conf.urls import url
from workoutLogging import views

# [94] import
import django.urls

urlpatterns = [
    django.urls.re_path(r'new$', views.newEntry, name="newEntryView"),
    django.urls.re_path(r'storedate', views.storeDate, name="storeDate"),
    django.urls.re_path(r'(\d+)$', views.viewEntry, name="viewEntryView"),
    django.urls.re_path(r'(\d+)/commentadd$', views.commentAddView, name="commentAddView"),
    django.urls.re_path(r'(\d+)/commentdelete', views.commentDeleteView, name="commentDeleteView")
]
