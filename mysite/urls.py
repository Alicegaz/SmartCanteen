"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from authentication.views import AccountViewSet
#from authentication.views import LoginView
#from authentication.views import LogoutView
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
#from mysite.views import IndexView
#from rest_framework_nested import routers
from . import views


#router = routers.SimpleRouter()
#router.register(r'accounts', AccountViewSet)

admin.autodiscover()


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
    url(r'^auth/', include('authentication.urls')),
]


#if not settings.DEBUG:
   # urlpatterns += patterns('',
    #    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT,'show_indexes': False}),
    #)