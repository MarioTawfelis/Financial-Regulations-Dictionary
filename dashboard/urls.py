from django.conf.urls import url
from . import views as dashboard_views


app_name = 'dashboard'

urlpatterns = [
    url(r'^$', dashboard_views.home, name='home'),

]