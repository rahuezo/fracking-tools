from django.conf.urls import url
from . import views
from document_comparison.views import document_comparison_view, compare_documents_view
from document_tagging.views import document_tagging_view, tag_documents_view, ner_tagging_view, tag_ner_view
from document_stats.views import document_stats_view, analyze_documents_view

from django.conf import settings
from django.conf.urls.static import static

app_name = 'document_utilities'

urlpatterns = [
    url(r'^$', views.document_utilities_view, name='docutils'),
    url(r'^document-comparison/$', document_comparison_view, name='doccomp'),
    url(r'^document-comparison/compare-documents/$', compare_documents_view, name='compdocs'),
    url(r'^document-keywords-tagging/$', document_tagging_view, name='doctag'),
    url(r'^document-keywords-tagging/tag-documents-keywords/$', tag_documents_view, name='tagdocs'),
    url(r'^document-ner-tagging/$', ner_tagging_view, name='nertag'),
    url(r'^document-ner-tagging/tag-documents-ner/$', tag_ner_view, name='tagner'),
    url(r'^document-statistics/$', document_stats_view, name='docstats'),
    url(r'^document-statistics/compute-document-statistics/$', analyze_documents_view, name='statdocs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
