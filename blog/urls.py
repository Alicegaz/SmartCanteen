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
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.menu_edit, name='menu_edit'),
    # have no permission url
    url(r'^no_permission/$', views.no_permission, name='no_permission'),

    url(r'^buy/$', views.buy_dishes, name='buy'),

    url(r'^schedule/$', views.schedule_new, name='schedule_new'),
    url(r'^schedule/(?P<pk>\d+)/edit/$', views.schedule_edit, name='schedule_edit'),

    # shares
    url(r'^shares/$', views.shares_list, name='shares'),
    url(r'^shares/form/$', views.shares_new, name='shares_new'),
    url(r'^shares/(?P<pk>\d+)/edit/$', views.shares_edit, name='shares_edit'),

    # offers
    url(r'^offer/$', views.get_offers, name='offers_list'),
    url(r'^offer/(?P<pk>\d+)', views.offer_detail, name='offer_detail'),
    url(r'^shares/(?P<pk>\d+)/$', views.shares_detail, name='shares_detail'),

    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^contacts/new/$', views.new_contact, name='new_contact'),
    url(r'^contacts/(?P<pk>\d+)/edit/$', views.contact_edit, name='contact_edit'),
    url(r'^contacts/(?P<pk>\d+)/remove/$', views.contacts_remove, name='contacts_remove'),

    # url(r'^cashier/$', views.casher_out, name='cashier_out'),
    url(r'^cashier/add/$', views.cashier_create, name='cashier_create'),
    url(r'^cashier/$', views.cashier_out, name='cashier_out'),

    url(r'^schedule_for_user/$', views.schedule_for_user, name='schedule_for_user')
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)