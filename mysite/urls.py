from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from . import views

admin.autodiscover()


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
    url(r'^auth/', include('authentication.urls')),
]