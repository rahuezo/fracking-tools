from django.conf.urls import url
from . import views
from network_comparison.views import network_comparison_view, compare_networks_view

from django.conf import settings
from django.conf.urls.static import static

app_name = 'network_builder'

urlpatterns = [
    url(r'^$', views.network_builder_view, name='network_builder'),
    url(r'^build-event-networks$', views.build_event_networks, name='build_enet'),
    url(r'^build-pair-networks', views.build_pair_networks, name='build_pnet'),
    url(r'^events$', views.events_network_view, name='events'),
    url(r'^pairs$', views.pairs_network_view, name='pairs'),
    url(r'^network-comparison$', network_comparison_view, name='netcomp'),
    url(r'^compare-networks$', compare_networks_view, name='compnets'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)