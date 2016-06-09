from django.conf.urls import url, patterns, include
from rest_framework import authentication
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^login/$', views.login, name='login.html'),
    url(r'^logout/$', views.logout, name='logout.html'),
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
