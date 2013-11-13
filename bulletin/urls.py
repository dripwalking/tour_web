from django.conf import settings
from django.conf.urls.defaults import *



urlpatterns = patterns('',
#show community
    url(r'^subscribe/$', 'tourprom.bulletin.views.subscribe', name='bulletin-subscribe'),
    (r'^activate/$', 'tourprom.bulletin.views.activate_subscription'),
    (r'^subscribe_done/$', 'django.views.generic.simple.direct_to_template', {'template': 'bulletin/subscribe_done.html'}),
    (r'^subscribe_active/$', 'django.views.generic.simple.direct_to_template', {'template': 'bulletin/subscribe_active.html'}),
    (r'^subscribe_notvalid/$', 'django.views.generic.simple.direct_to_template', {'template': 'bulletin/subscribe_notvalid.html'}),
    (r'^unsubscribe/$', 'tourprom.bulletin.views.unsubscribe'),
    (r'^help/$', 'django.views.generic.simple.direct_to_template', {'template': 'bulletin/help.html'}),
    (r'^top/$', 'tourprom.bulletin.views.get_top3x3'),
    (r'^unsubscribe_done/$', 'django.views.generic.simple.direct_to_template', {'template': 'bulletin/unsubscribe_done.html'}),
    url(r'^ajax/subscribe/$', 'tourprom.bulletin.views.ajax_subscribe', name='bulletin-ajax-subscribe'),

)