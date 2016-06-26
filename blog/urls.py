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

    url(r'^new/menu/$', views.new_menu, name='new_menu'),
    url(r'^dishes/list/$', views.dishes_list, name='dishes_list'),
    url(r'^no/permission/$', views.no_permission, name='no_permission'),
    url(r'^new/supper/$', views.new_supper, name='new_supper'),
    url(r'^new/breakfast/$', views.new_breakfast, name='new_breakfast'),
    url(r'^new/dinner/$', views.new_dinner, name='new_dinner'),
    url(r'^menu/archive/$', views.menu_archive, name='menu_archive'),
    url(r'^breakfast/edit/$', views.breakfast_edit, name='breakfast_edit'),
    url(r'^supper/edit/$', views.supper_edit, name='supper_edit'),
    url(r'^dinner/edit/$', views.dinner_edit, name='dinner_edit'),
    url(r'^dishes/list/post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^supper/edit/$', views.supper_edit, name='supper_edit'),
    url(r'^supper/edit/$', views.supper_edit, name='supper_edit'),
    url(r'^post/(?P<pk>\d+)/menu/remove/$', views.menu_remove, name='menu_remove'),
   # url(r'^post/(?P<pk>\d+)/menu/item/remove/$', views.menu_item_remove, name='menu_item_remove'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.menu_edit, name='menu_edit'),
    #url(r'^post/(?P<pk>\d+)/menu/item/remove/$', views.menu_item_remove, name='menu_item_remove'),
    url(r'^menu/(?P<pk>\d+)/item/(?P<item_pk>\d+)/remove', views.menu_item_remove, name='menu_item_remove'),
    url(r'^post/ingredientlist/(?P<pk>\d+)/remove/$', views.ingredient_remove, name='ingredient_remove'),
    # url(r'^post/(?P<pk>\d+)/images/$', view.post)
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)