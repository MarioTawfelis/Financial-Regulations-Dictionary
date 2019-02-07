from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import login, logout
from . import views as account_views
from dashboard import views as dashboard_views


app_name = 'accounts'

urlpatterns = [
    url(r'^$', dashboard_views.home, name='home'),
    url(r'^register/$', account_views.register, name='register'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^profile/$', account_views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', account_views.edit_profile, name='edit_profile'),


]


