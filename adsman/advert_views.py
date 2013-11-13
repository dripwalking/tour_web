# -*- coding: utf-8 -*-
import datetime
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from tourprom.adsman.models import AdsPage
from tourprom.advertisers.models import Advertiser, ChangedDate
from tourprom.bulletin.models import Bulletin

# utils
def get_user_date(date):
    return date.strftime("%d.%m.%Y")

def get_latest_bulletin():
    return Bulletin.objects.order_by('-date')[0]
    
def get_latest_bulletin_date():
    return (get_latest_bulletin()).date    
    
def is_pub_date_valid(tdt):
    if tdt <= get_latest_bulletin_date():
        return False
    dt = ChangedDate.objects.filter(date=tdt)
    if len(dt) > 0:
        if not dt[0].publish:
            return False
    else:
        if tdt.weekday() == 5 or tdt.weekday() == 6:
            return False
    return True

def get_next_pub_date(td = None):
    if td == None:
        td = get_latest_bulletin_date()
    for i in range (1, 100):
        next_day = td + datetime.timedelta(days=i)
        if is_pub_date_valid(next_day):
            return next_day
    return None
    

# private functions
def _parse_pcontrol_value(pcontrols):
    values = {}
    for pcontrol in pcontrols:
        if pcontrol.control:
            if pcontrol.control.value != "" :
                values[pcontrol.control.name] = pcontrol.control.value
            if (pcontrol.control.type == "calendar" and pcontrol.mandatory) or pcontrol.control.type == "pub_date":
                next_day = get_next_pub_date()
                values[pcontrol.control.name] = get_user_date(next_day)                
    return values

def _update_values(values, user):
        if type(user) is Advertiser:
            values['sender'] = user.name
            if not values.has_key('web_site'):
                if user.web_site:
                    values['web_site'] = user.web_site
                else:
                    values['web_site'] = "http://"
        else:
            values['sender'] = user.nickname
        values['sender_id'] = user.id

def _show_page(request, page_id, mode="default", values=None, wrong=None, post = None, return_page = ""):
    page = AdsPage.objects.get(id=page_id)
    if mode == "default" or mode == "job":
        url = 'adsman/advert/ads_page.html'
    elif mode == "edit-post" :
        url = url = 'adsman/advert/ads_page_edit.html'
    else:
        url = 'adsman/ads_page_adm.html'    # ?
    controls = page.controls.order_by("position").all()      
    if values == None:
        values = _parse_pcontrol_value(controls)
    _update_values(values, request.user)
    return render_to_response(url,
                              { "page": page, "controls" :  controls, "post" : post, "return" : return_page,
                                "mode" : mode , "values" : values, "wrong": wrong} , context_instance=RequestContext(request))


# views                                
def get_page_list(request, mode="default"):
    pages = AdsPage.objects.filter(parent=None)
    if mode == "admin":# ?
        url = 'adsman/ads_pages_adm.html'# ?
    else:
        if request.user.is_authenticated and type(request.user) is Advertiser:
            user = request.user
        else:
            return HttpResponseRedirect('/profi/login/')
        url = 'adsman/advert/ads_pages.html'
        pages = pages.filter(visible = True)
    return render_to_response(url,
                              { 'pages': pages, "mode" : mode }, context_instance=RequestContext(request))

def get_page(request, page_id, mode="default"): 
     if request.user.is_authenticated and(  (type(request.user) is Advertiser) or ( type(request.user) is CustomUser) ):
            user = request.user
     else:
            return HttpResponseRedirect('/profi/login/')
     return _show_page(request, page_id, mode)

def preview_post(request, page_id):
    page = AdsPage.objects.get(id=page_id) 
    if (request.user.is_authenticated and type(request.user) is Advertiser):
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    valid, missing = validate_post(request, page_id)
    if valid:
        values = _parse_post_values(request)
        html = get_bulletin_text(page , [values])
        return render_to_response('adsman/advert/preview_post.html', {"text" : html, "page" : page_id,
                                    "values" : values, 'url' : get_referer(request) }, context_instance=RequestContext(request))      
    else:        
        return _show_page(request, page_id, "default", _parse_post_values(request), missing)
     