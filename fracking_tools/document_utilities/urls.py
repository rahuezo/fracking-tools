from django.conf.urls import url
from . import views
from document_comparison.views import document_comparison_view, compare_documents_view
from document_tagging.views import document_tagging_view

from django.conf import settings
from django.conf.urls.static import static

app_name = 'document_utilities'

urlpatterns = [
    url(r'^$', views.document_utilities_view, name='docutils'),
    url(r'^document-comparison', document_comparison_view, name='doccomp'),
    url(r'^compare-documents', compare_documents_view, name='compdocs'),
    url(r'^document-tagging', document_tagging_view, name='doctag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
