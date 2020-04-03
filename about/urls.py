# Skeleton code from [98, Write your first view] and possibly elsewhere from
# that page.
from django.conf.urls import url
from . import views

urlpatterns = [
    # These next url(...) lines may be from [98, Write your first view] or just
    # [98] in general, but were modified for Rogger
    url(r'^$', views.about, name='about'),
]
