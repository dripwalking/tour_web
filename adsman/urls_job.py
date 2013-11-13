from django.conf import settings
from django.conf.urls.defaults import *



urlpatterns = patterns('',
 #job part
    url(r'^$', 'tourprom.adsman.views.get_job_intro_page', name='jobs'),
    url(r'^(.*)/new/$', 'tourprom.adsman.views.get_job_post_form'),
    #url(r'^not_valid_post/$', 'django.views.generic.simple.direct_to_template', {'template': 'adsman/not_valid_post.html'}),
    url(r'^store/(.*)$', 'tourprom.adsman.views.store_j_item'),
    url(r'^remove/(.*)$', 'tourprom.adsman.views.remove_j_item'),
    url(r'^basket/$', 'tourprom.adsman.views.j_basket'),
    url(r'^(.*)/$', 'tourprom.adsman.views.get_job_page'),
)