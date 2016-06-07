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
from django.conf.urls import url, include, patterns
from django.contrib import admin
from mysite import settings
from rest_framework_nested import routers
from mysite.views import IndexView

from authentication.views import AccountViewSet
from authentication.views import LoginView
from authentication.views import LogoutView
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

admin.autodiscover()


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
    url(r'^api/v1/', include(router.urls)),
    url('^.*$', IndexView.as_view(), name='index'),
    #url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/admin/$', views.post_admin, name='post_admin'),
    url(r'^post/ingredientnew/$', views.post_ingredientnew, name='post_ingredientnew'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    # url(r'^post/ingredientlist/$', views.post_ingredientlist, name='post_ingredientlist'),
    url(r'^post/(?P<pk>\d+)/ingredientedit/$', views.post_ingredientedit, name='post_ingredientedit'),
    url(r'^post/(?P<pk>\d+)/ingredientdetail/$', views.post_ingredientdetail, name='post_ingredientdetail'),
    url(r'^post/ingredientlist/$', views.post_ingredientlist, name='post_ingredientlist'),

]

#if not settings.DEBUG:
   # urlpatterns += patterns('',
    #    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT,'show_indexes': False}),
    #)