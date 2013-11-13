# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'tourprom.adsman.advert_views.get_page_list'),
    (r'^(?P<page_id>\d+)/$', 'tourprom.adsman.advert_views.get_page'),    
    #(r'^posts/(\d+)/edit/$', 'tourprom.adsman.views.edit_post'),
    #(r'^posts/(\d+)/f-edit/$', 'tourprom.adsman.views.edit_my_fpost'),
    #(r'^posts/(\d+)/save/$', 'tourprom.adsman.views.save_post'),# save after edit
    (r'^(?P<page_id>\d+)/preview_post/$', 'tourprom.adsman.advert_views.preview_post'),# preview new
    #(r'^(?P<page_id>\d+)/post$', 'tourprom.adsman.views.post'),# save new
    #(r'^posts/(\d+)/delete/$', 'tourprom.adsman.views.delete_post'),
    #(r'^posts/(\d+)/copy-form/$', 'tourprom.adsman.views.get_copy_form'),
    #(r'^posts/(\d+)/copy/$', 'tourprom.adsman.views.copy_post'),
    #(r'^(?P<page_id>\d+)/posts/$', 'tourprom.adsman.views.get_posts'),
    #(r'^future/dates/$', 'tourprom.adsman.views.get_future_pub_dates'),
    #(r'^past/dates/(.*)$', 'tourprom.adsman.views.get_past_pub_dates'),
    #(r'^check_pub_date/$', 'tourprom.adsman.views.check_pub_date'),
    #(r'^(?P<page_id>\d+)/preview_edit$', 'tourprom.adsman.views.edit_from_preview'),
    #(r'^test/$', 'django.views.generic.simple.direct_to_template', {'template': 'adsman/ads_page_test.html'}),
)