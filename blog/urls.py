from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # index url
    url(r'^$', views.menu_out, name='post_list'),

    # dishes urls
    url(r'^dish/$', views.dishes_list, name='dishes_list'),
    url(r'^dish/(?P<pk>\d+)/$', views.dish_details, name='post_detail'),
    url(r'^dish/new/$', views.new_dish, name='post_new'),
    url(r'^dish/(?P<pk>\d+)/edit/$', views.dish_edit, name='post_edit'),
    url(r'^dish/(?P<pk>\d+)/remove/$', views.dish_remove, name='post_remove'),

    # url(r'^post/admin/$', views.post_admin, name='post_admin'),

    # ingredient urls
    url(r'^ingredient/$', views.ingredient_list, name='post_ingredientlist'),
    url(r'^ingredient/new/$', views.new_ingredient, name='post_ingredientnew'),
    url(r'^ingredient/(?P<pk>\d+)/edit/$', views.ingredient_edit, name='post_ingredientedit'),
    url(r'^ingredient/(?P<pk>\d+)/$', views.ingredient_detail, name='post_ingredientdetail'),
    url(r'^ingredient/(?P<pk>\d+)/remove/$', views.ingredient_remove, name='ingredient_remove'),

    # menu urls
    url(r'^menu/$', views.history_out, name='menu_archive'),
    url(r'^menu/new/$', views.new_menu, name='new_menu'),
    url(r'^menu/(?P<pk>\d+)/remove/$', views.menu_remove, name='menu_remove'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.menu_edit, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/item/(?P<item_pk>\d+)/remove', views.menu_item_remove, name='menu_item_remove'),

    # have no permission url
    url(r'^no_permission/$', views.no_permission, name='no_permission'),

    url(r'^schedule_new/$', views.schedule_new, name='schedule_new'),
    url(r'^schedule/(?P<pk>\d+)/edit/$', views.schedule_edit, name='schedule_edit'),

    #to resolve bugs
    url(r'^auth/register/schedule/(?P<pk>\d+)/edit/$', views.schedule_edit, name='schedule_edit'),
    url(r'^auth/register/schedule_new$', views.schedule_new, name='schedule_new'),
    url(r'^auth/user/schedule_new$', views.schedule_new, name='schedule_new'),
    url(r'^auth/user/schedule/(?P<pk>\d+)/edit/$', views.schedule_edit, name='schedule_edit'),

]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)