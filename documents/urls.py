from django.urls import re_path
from . import views as documents_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'documents'

urlpatterns = [
                  re_path(r'^$', documents_views.new_document, name='new_document'),
                  re_path(r'^new$', documents_views.new_document, name='new_document'),
                  re_path(r'^new(?P<url>\d+)$', documents_views.new_document, name='new_document'),
                  re_path(r'^downloads$', documents_views.downloads, name='downloads'),
                  re_path(r'^download-document/(?P<pk>\d+)$', documents_views.download_document, name='download_document'),
                  re_path(r'^delete-document/(?P<pk>\d+)$', documents_views.delete_document, name='delete_document'),
                  re_path(r'^search$', documents_views.search, name='search'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
