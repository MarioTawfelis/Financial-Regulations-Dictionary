from django.urls import re_path
from . import views as scanner_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'scanner'

urlpatterns = [
          re_path(r'^$', scanner_views.home, name='home'),
          # url(r'scrape/<str:url>/$', scanner_views.scrape, name='scrape')
      ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
