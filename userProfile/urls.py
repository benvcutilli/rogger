# Skeleton code from [98, Write your first view] and possibly elsewhere from
# that page.
from django.conf.urls import url
from . import views

urlpatterns = [
    # These next url(...) lines may be from [98, Write your first view] or just
    # [98] in general, but were modified for Rogger
    url(r'^([a-zA-Z0-9_]+)$', views.userView, name='userView'),
    # next line is using a url redirect approach for generating pdfs, which is from the previous version of Rogger, see README for the url to the code for the previous version of Rogger
    url(r'^([a-zA-Z0-9_]+)/week([0-9]*)\.([0-9]*)\.([0-9]*).pdf$', views.weekPDFView, name='weekPDFView'),
    url(r'^([a-zA-Z0-9_]+)/changePicture$', views.changePictureView, name='changePictureView'),
    url(r'^$', views.userView, name='userViewStub'),
]
