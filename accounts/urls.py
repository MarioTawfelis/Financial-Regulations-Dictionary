from django.urls import re_path
from django.contrib.auth.views import LoginView, LogoutView
from . import views as account_views
from dashboard import views as dashboard_views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^$', dashboard_views.home, name='home'),
    re_path(r'^register/$', account_views.register, name='register'),
    re_path(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    re_path(r'^logout/$', LoginView.as_view(template_name='accounts/logout.html'), name='logout'),
    re_path(r'^profile/$', account_views.view_profile, name='view_profile'),
    re_path(r'^profile/edit/$', account_views.edit_profile, name='edit_profile'),
]
