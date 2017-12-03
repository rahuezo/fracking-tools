from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^network-builder/', include('network_builder.urls', namespace='network_builder')),
    url(r'^$', include('home.urls', namespace='home'), name='home'),
]
