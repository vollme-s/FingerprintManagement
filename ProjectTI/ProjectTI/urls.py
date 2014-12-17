from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/fingerprint/')),
    url(r'^fingerprint/', include('fingerprint.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
