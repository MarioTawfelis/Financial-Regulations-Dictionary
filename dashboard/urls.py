from django.urls import re_path
from . import views as dashboard_views


app_name = 'dashboard'

urlpatterns = [
    re_path(r'^$', dashboard_views.home, name='home'),

]