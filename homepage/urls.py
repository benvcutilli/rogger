# Skeleton code from [98, Write your first view] and possibly elsewhere from
# that page.
from django.conf.urls import url
from . import views

urlpatterns = [
    # These next url(...) lines may be from [98, Write your first view] or just
    # [98] in general, but were modified for Rogger
    url(r'^$', views.homepage, name='homepage'),
    url(r'^login$', views.loginView, name='loginView'),
    url(r'^logout$', views.logoutUser, name='logout'),
    url(r'^newaccount$', views.newAccountView, name='newAccountView'),
    url(r'^changepassword$', views.changePasswordView, name='changePasswordView'),
    url(r'^resetpassword/([^/]+)/([^/]+)$', views.passwordResetView, name='passwordResetView'),
    url(r'^resetpasswordrequest$', views.passwordResetRequestView, name='passwordResetRequestView'),
]
