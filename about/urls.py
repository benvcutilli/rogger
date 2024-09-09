# Skeleton code from [98, Write your first view] and possibly elsewhere from
# that page. Commented out this line because it doesn't work anymore
#from django.conf.urls import url
from . import views

# [94] provides this package
import django.urls
urlpatterns = [
    # These next url(...) lines may be from [98, Write your first view] or just
    # [98] in general, but were modified for Rogger
    django.urls.re_path(r'^$', views.about, name='about'),
]
