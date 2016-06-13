from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/admin/$', views.post_admin, name='post_admin'),
    url(r'^post/ingredientnew/$', views.post_ingredientnew, name='post_ingredientnew'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/ingredientedit/$', views.post_ingredientedit, name='post_ingredientedit'),
    url(r'^post/(?P<pk>\d+)/ingredientdetail/$', views.post_ingredientdetail, name='post_ingredientdetail'),
    url(r'^post/ingredientlist/$', views.post_ingredientlist, name='post_ingredientlist'),
    url(r'^mymodal/(?P<pk>\d+)/$', views.mymodal, name='mymodal'),
    url(r'^new/menu/$', views.new_menu, name='new_menu'),
    # url(r'^post/(?P<pk>\d+)/images/$', view.post)
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)