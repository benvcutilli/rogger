# Skeleton code from [98, Write your first view] and possibly elsewhere from
# that page; the line below, however, has been commented out
#from django.conf.urls import url
from . import views

# Package from [94]
import django.urls

urlpatterns = [
    # These next url(...) lines may be from [98, Write your first view] or just
    # [98] in general, but were modified for Rogger
    django.urls.re_path(r'^$', views.homepage, name='homepage'),
    django.urls.re_path(r'^login$', views.loginView, name='loginView'),
    django.urls.re_path(r'^logout$', views.logoutUser, name='logout'),
    django.urls.re_path(r'^newaccount$', views.newAccountView, name='newAccountView'),
    django.urls.re_path(r'^changepassword$', views.changePasswordView, name='changePasswordView'),
    django.urls.re_path(r'^resetpassword/([^/]+)/([^/]+)$', views.passwordResetView, name='passwordResetView'),
    django.urls.re_path(r'^resetpasswordrequest$', views.passwordResetRequestView, name='passwordResetRequestView'),
]
