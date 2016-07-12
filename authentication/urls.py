from django.conf.urls import url, patterns, include
from rest_framework import authentication
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^login/$', views.login, name='login.html'),
    url(r'^logout/$', views.logout, name='logout.html'),
    url(r'^register/$', views.register, name='register.html'),
    url(r'^no/permission/$', views.no_permission, name='no_permission.html'),
    url(r'^user/$', views.users, name='users.html'),
    url(r'^user/(?P<pk>\d+)/remove/$', views.user_remove, name='user_remove'),
    #url(r'^have_no_permission/', views.no_permission, name='no_permission'),
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
