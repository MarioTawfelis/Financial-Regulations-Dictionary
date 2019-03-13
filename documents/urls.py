from django.conf.urls import url
from . import views as documents_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'documents'

urlpatterns = [
                  url(r'^$', documents_views.new_document, name='new_document'),
                  url(r'^new$', documents_views.new_document, name='new_document'),
                  url(r'^downloads$', documents_views.downloads, name='downloads'),
                  url(r'^download-document/(?P<pk>\d+)$', documents_views.download_document, name='download_document'),
                  url(r'^delete-document/(?P<pk>\d+)$', documents_views.delete_document, name='delete_document'),
                  url(r'^search$', documents_views.search, name='search'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
