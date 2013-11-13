from django.conf import settings
from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^avia/$', 'tourprom.bulletin.views.trade_area_avia'),
    url(r'^tour/$', 'tourprom.bulletin.views.trade_area_tour'),
    url(r'^tstore/(.*)$', 'tourprom.adsman.views.store_t_item'),
    url(r'^remove/(.*)$', 'tourprom.adsman.views.remove_t_item'),
    url(r'^basket/$', 'tourprom.adsman.views.t_basket'),
    url(r'^add_to_favorites/(\d+)/$', 'tourprom.adsman.views.add_to_favorites'),
    url(r'^remove_from_favorites/(\d+)/$', 'tourprom.adsman.views.remove_from_favorites'),
    url(r'^favorites/$', 'tourprom.adsman.views.favorites'),
    url(r'^$', 'tourprom.bulletin.views.trade_area', name='tradearea'),
    url(r'^(.+)/$', 'tourprom.bulletin.views.trade_area_old', name='tradearea-old'),
)