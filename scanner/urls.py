from django.conf.urls import url
from . import views as scanner_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'scanner'

urlpatterns = [
                  url(r'^$', scanner_views.home, name='home'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
