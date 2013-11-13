# -*- coding: utf-8 -*-
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext
from django.db.models import Max
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
import datetime
from datetime import date
from tourprom.adsman import  *
from tourprom.adsman.models import *
from tourprom.bulletin.models import *
from tourprom.advertisers.models import Advertiser, ChangedDate
from tourprom.accounts.models import CustomUser
from tourprom.news.models import News
import calendar

def parse_pub_dates(request):
    return [ date.strip() for date in  request.POST["pub_date"].split("\n") if date.strip() != "" ]

def get_latest_bulletin():
    return Bulletin.objects.order_by('-date')[0]
        
def get_latest_bulletin_date():
    return (get_latest_bulletin()).date
               
def get_referer(request):
    try:
        return request.POST["return_page"]
    except:
        try:
            return request.META["HTTP_REFERER"]
        except:
            "/profi/login/"
        
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
        


def get_price_from_request(request):
    price = None
    if "price" in request.POST:
        try:
            price = int(request.POST["price"])
        except:
            pass    
    currency = None
    if "price_currency" in request.POST:
        currency = request.POST["price_currency"]    
    return price, currency


def init_post_from_request(request , post, user, date):
    price, currency = get_price_from_request(request)
    if post.is_free:
        post.user = user
    else:
        post.author = user
    post.publish_date = parse_user_date(date)
    post.price = price
    post.currency = currency
    if "country" in request.POST:
        post.location = "+".join(request.POST.getlist("country"))
    if "avia_route_2" in request.POST:
        from tourprom.avia.models import Airport
        try:
            post.location = Airport.objects.get(title=request.POST["avia_route_2"]).city.country.title
        except:
            pass
    if post.page.parent.id == 21:
            post.location = "Россия"
    if "tour_start" in request.POST:
        post.active_date = parse_user_date(request.POST["tour_start"])
    if "dept_date" in request.POST:
        post.active_date = parse_user_date(request.POST["dept_date"])

        
def posts_2_html(posts, mode="default", request = None, is_search=False):
    container = []
    ids = get_basket(request, "t-basket")
    for post in posts:
        entry = {}
        values = {}
        values["id"] = post.id
        try:
            values["sender_id"] = post.author.id
            values["sender"] = post.author.name
        except:
            pass
        if str(post.id) in ids:
            values["checked"] = "checked"
        else:
            values["checked"] = ""  
        for data in post.entries.all():
            values[data.key] = data.value 
        if post.author:
            usr = post.author
        else:
            usr = post.user    
        _update_values(values, usr)
        entry["post"] = post
        entry['html'] = get_bulletin_text(post.page, [values], mode, is_search)
        if entry['html'] != "":
            container.append(entry)    
    return container

def _get_price_from_post(post):
    for entry in post.entries.all():
        if entry.key == "price":
            return entry.value
    return 0

def parse_user_date(str):
    (day, month, year) = str.split(".")
    if len(year) == 2:
        year = '20' + year
    return date(int(year), int(month), int(day))

def check_pub_date(request):
    dt = parse_user_date(request.POST['date'])
    if is_pub_date_valid(dt):
        return HttpResponse("")
    else:
        return HttpResponse("Публикация в этот день невозможна")

def get_user_date(date):
    #return "%s.%s.%s" %(date.day, date.month, date.year)
    return date.strftime("%d.%m.%Y")

#def init_post_fields(post, key, value):
#    if key == 'tour_start' or key == 'dept_date':
#        post.active_date = parse_user_date(value)
#        post.save()
        
def _get_post_data(post_id):
    post = AdsPost.objects.get(id=post_id)
    values = {}
    for entry in post.entries.all():
        #init_post_fields (post, entry.key, entry.key)
        if entry.key == "pub_date":
            values["pub_date"] = get_user_date(post.publish_date)
        else:
            values[entry.key] = entry.value    
    return values, post


def _fix_posts(key, posts = None):
    if posts == None:
        posts = AdsPost.objects.filter(entries__key = key)
    for post in AdsPost.objects.filter(entries__key = key):
        for entry in post.entries.all():
            try:
                if entry.key == key:
                    post.active_date = parse_user_date(entry.value)
                    post.save()
                    break
            except:
                pass

#def fix_data(request):
#    _fix_posts('tour_start') 
#    _fix_posts('dept_date')   
#    return HttpResponse("OK")

def get_page_template(page):
    if page.template == None or page.template == "":
        url = 'adsman/ads_posts_tour.html'
    else:
        url = page.template
    return url

def render_template(tfile, dict):
    t = get_template(tfile)
    return t.render(Context(dict))

def get_bulletin_text(page, posts, mode="default", is_search=False):
    url = get_page_template(page)
    return render_template(url, {"posts": posts, "mode": mode, 'is_search': is_search})


def load_page(page_id, pub_date, mode, request= None ):
    page = AdsPage.objects.get(id = page_id)
#    if page.uid == "cv" or page.uid == "vacancy":
#        return ""
    posts = get_post_objects(page_id, pub_date, request) 
    if len(posts)== 0:
        return ""
    return get_bulletin_text(page, posts, mode)   


def get_page_list(request, mode="default"):
    pages = AdsPage.objects.filter(parent=None)
    if mode == "admin":
        url = 'adsman/ads_pages_adm.html'
    else:
        if request.user.is_authenticated and type(request.user) is Advertiser:
            user = request.user
        else:
            return HttpResponseRedirect('/profi/login/')
        url = 'adsman/ads_pages.html'
        pages = pages.filter(visible = True)
    return render_to_response(url,
                              { 'pages': pages, "mode" : mode }, context_instance=RequestContext(request))
    
def get_page_adm(request, page_id):
    return get_page(request, page_id, "admin")

def _show_page(request, page_id, mode="default", values=None, wrong=None, post = None, return_page = ""):
    page = AdsPage.objects.get(id=page_id)
    if mode == "default" or mode == "job":
        url = 'adsman/ads_page.html'
    elif mode == "edit-post" :
        url = url = 'adsman/ads_page_edit.html'
    else:   
        url = 'adsman/ads_page_adm.html'  
    controls = page.controls.order_by("position").all()      
    if values == None:
        values = _parse_pcontrol_value(controls)
    _update_values(values, request.user)
    return render_to_response(url,
                              { "page": page, "controls" :  controls, "post" : post, "return" : return_page,
                                "mode" : mode , "values" : values, "wrong": wrong} , context_instance=RequestContext(request))
    

def get_page(request, page_id, mode="default"): 
     if request.user.is_authenticated and(  (type(request.user) is Advertiser) or ( type(request.user) is CustomUser) ):
            user = request.user
     else:
            return HttpResponseRedirect('/profi/login/')
     return _show_page(request, page_id, mode)
    
    
def get_page_list_adm (request):
    return get_page_list(request, "admin")

def create_page(request):
    template_id = 0
    parent_id = 0
    try:
        template_id = int(request.POST["template"])
        parent_id = int(request.POST["parent"])
    except:
        pass
    page = AdsPage (title=request.POST["title"])
    if parent_id != 0:
        page.parent = AdsPage.objects.get(id=parent_id)        
    page.save()
    if template_id != 0 :
        t_page = AdsPage.objects.get(id=template_id)
        for pcontrol in t_page.controls.all():
            AdsPlacedControl.objects.create(page=page, control=pcontrol.control,
                        position=pcontrol.position, hidden=pcontrol.hidden, mandatory=pcontrol.mandatory)            
    return HttpResponseRedirect("/admin/adspages/")

def remove_page(request, page_id):
    AdsPage.objects.get(id=page_id).delete()
    return HttpResponseRedirect("/admin/adspages/")

def get_position_on_page(page_id):
    try:
        return AdsPlacedControl.objects.filter(page=page_id).order_by("-position")[0].position + 1
    except:
        return 0

def add_control(request, page_id, control_id):
    page = AdsPage.objects.get(id=page_id)
    control = AdsControl.objects.get(id=control_id)
    position = get_position_on_page(page_id)
    AdsPlacedControl.objects.create(page=page, control=control, position=position)
    return HttpResponseRedirect("/admin/adspages/" + str(page.id) + "/")
    

def remove_control(request, page_id, pcontrol_id):
    to_remove = AdsPlacedControl.objects.get(id=pcontrol_id)
    position = to_remove.position
    for pcontrol in AdsPlacedControl.objects.filter(page__id=page_id).filter(position__gte=position):
        pcontrol.position = pcontrol.position - 1
        pcontrol.save()
    to_remove.delete()
    return HttpResponseRedirect("/admin/adspages/" + str(page_id) + "/")

def move_control(page_id, pcontrol_id, step):
     pcontrol = AdsPlacedControl.objects.get(id=pcontrol_id)
     prev_position = pcontrol.position
     next_position = prev_position + step
     if next_position >= 0:
         to_move = AdsPlacedControl.objects.filter(page__id=page_id).filter(position=next_position)[0]
         if to_move:
             to_move.position = prev_position
             pcontrol.position = next_position
             pcontrol.save()
             to_move.save()             
     return HttpResponseRedirect("/admin/adspages/" + str(page_id) + "/")
 


def change_mandatory_option(request, page_id, pcontrol_id):
    pcontrol = AdsPlacedControl.objects.get(id=pcontrol_id)
    pcontrol.mandatory = not  pcontrol.mandatory
    pcontrol.save()  
    return HttpResponseRedirect("/admin/adspages/" + str(page_id) + "/")

def move_control_up (request, page_id, pcontrol_id):
    return move_control(page_id, pcontrol_id, -1)

def move_control_down (request, page_id, pcontrol_id):
    return move_control(page_id, pcontrol_id, 1)

def move_control_to (request, page_id, pcontrol_id):
    pcontrol = AdsPlacedControl.objects.get(id=pcontrol_id)
    new_position = int(request.POST["position"])
    current_position = pcontrol.position
    if new_position < current_position:
        step = 1
        high = new_position 
        low = current_position - 1
    else:
        step = -1
        high = current_position + 1
        low = new_position
    ctrls = AdsPlacedControl.objects.filter(page__id=page_id, position__gte=high, position__lte=low)
    for ctr in ctrls:
        ctr.position += step
        ctr.save()        
    pcontrol.position = new_position
    pcontrol.save()
    return HttpResponseRedirect("/admin/adspages/" + str(page_id) + "/")
 
def _parse_control_value(controls):
    values = {}
    for control in controls:
        if control and control.value != "":
            values[control.name] = control.value
    return values

def _parse_pcontrol_value(pcontrols):
    values = {}
    for pcontrol in pcontrols:
        if pcontrol.control:
            #pcontrol.control.p_value = pcontrol.control.value.split(pcontrol.control.delimiter)
            if pcontrol.control.value != "" :
                values[pcontrol.control.name] = pcontrol.control.value
            if (pcontrol.control.type == "calendar" and pcontrol.mandatory) or pcontrol.control.type == "pub_date":
                next_day = get_next_pub_date()#datetime.date.today() + datetime.timedelta(days=1)
                values[pcontrol.control.name] = get_user_date(next_day)                
    return values

def get_all_controls(request, page_id):
    page = AdsPage.objects.get(id=page_id)
    controls = AdsControl.objects.order_by("-id")
    return render_to_response('adsman/ads_page_adm.html',
                              { "page": page, "values": controls,
                               "controls" : [AdsPlacedControl (page=page, control=control, position=0) for control in controls ],
                               "mode" : "all-controls" })
def _validate_value(constraint, type, value, data):
    try:
        if constraint and constraint != "" and constraint.isdigit():
            return len(value) <= int(constraint)
        if (type == "price" or  type == "price_avia") and data["price_currency"] == "":
            return False            
        if constraint == "int" or type == "price" or  type == "price_avia":
            return value.isdigit()
        if constraint == "date" or type == "calendar":
#                udate = parse_user_date(value)
#                if udate < date.today():
#                    return False
                return True
        if type == "pub_date":
            dates = [parse_user_date(val) for val in  value.split("\n") if val.strip() != ""]
            for date in dates:
                if not is_pub_date_valid(date):
                    return False
            return True            
    except:
        return False               
    return True 

def validate_post(request, page_id, ignore_pubdate=False):
    result = True
    missing = {}
    for key, values in request.POST.lists():
        val = "+".join(values)      
        try:
            val = val.encode("cp1251") 
            if len(val) > 499:
                 missing[key] = True
                 result = False                    
        except:
            missing[key] = True
            result = False                 
    for control in AdsPlacedControl.objects.filter(page__id=page_id):
        if control.control.name in request.POST and request.POST[control.control.name] != "":
            if not (control.control.type == "pub_date" and ignore_pubdate):
                if not _validate_value(control.control.constraint, control.control.type, request.POST[control.control.name], request.POST):
                    missing[control.control.name] = True
                    result = False
        if control.mandatory:
            if control.control.name in request.POST and request.POST[control.control.name] != "":
                continue
            else:
                missing[control.control.name] = True
                result = False              
    return result, missing

def _is_balance_valid(user, post):
    if  user.messages_expire_date == None or datetime.date.today() > user.messages_expire_date:
    #post.publish_date > user.messages_expire_date:
        return False
    if user.messages_quantity == 0:
        return False
    return True

def _is_date_limit_valid(user, post):
    limit = post.page.limit
    if limit == 0:
        return True
    count = AdsPost.objects.filter(author__id=user.id, publish_date=post.publish_date).count()
    if count < limit:
        return True
    return False

def _is_valid_for_free(user, post, request):
    today = datetime.date.today()
    if AdsPost.objects.filter(user=user, date_added__year=today.year, date_added__month=today.month, date_added__day=today.day).count() > 0:
        return False
    if 'email' in request.POST:
        if AdsPostEntry.objects.filter(key='email', value=request.POST['email'], post__is_free=True, post__date_added__year=today.year, post__date_added__month=today.month, post__date_added__day=today.day).count() > 0:
            return False
    return True

def _split_long(str, step):
    res= str[:step]
    tail = str[step:]
    while len(tail) > 0:
        res += " " +  tail[:step]
        tail = tail[step:]
    return res
    #print res

   
def _process_long (str):
    step = 70
    words = str.split(" ")
    fixed = []
    str = ""
    for word in words: 
        if len(word) > step:
            word = _split_long(word, step)
        fixed.append(word)
    str = " ".join(fixed)
    return str

def post(request, page_id):
    page = AdsPage.objects.get(id=page_id)
    if not page.visible:
        return HttpResponseRedirect('/job/rubric_disabled/')
    is_free = False
    if (request.user.is_authenticated and type(request.user) is Advertiser) or (type(request.user) is CustomUser and page.allow_free) :
        user = request.user
        if type(user) is CustomUser:
            is_free = True
    else:
        return HttpResponseRedirect('/profi/login/')
    dates =  parse_pub_dates(request) #request.POST["pub_date"].split("\n")
    cnt = 0
    for date in dates:
        post = AdsPost(page=page)
        post.is_free = is_free
        init_post_from_request(request , post, user, date)
        if not is_free:
            if not _is_balance_valid(user, post):
                return HttpResponseRedirect('/profi/not_enough/')        
                #raise InvalidBalance()     
            if not _is_date_limit_valid(user, post):
                return HttpResponseRedirect('/profi/date_limit_exeed/')        
            user.messages_quantity -= 1
            cnt += 1
            user.save()
        if is_free and not _is_valid_for_free(user, post, request):
            return HttpResponseRedirect('/job/not_valid_post/')

        post.save()
        for key, value_list in request.POST.lists():
            #init_post_fields(post, key, value_list[0])
            if key != "pub_date":
                if key == 'country':
                    vl = _process_long( ("+".join(value_list)).strip() )
                else:
                    vl = _process_long( (",".join(value_list)).strip() )
                AdsPostEntry.objects.create(post=post, key=key, value=vl, position=0)
            else:
                AdsPostEntry.objects.create(post=post, key=key, value= date, position=0)
                
    #return render_to_response('adsman/ads_post_confirm.html', {"mode" : "ok"}, context_instance=RequestContext(request))
    if is_free:
        return HttpResponseRedirect('/job/' + page.uid + "/") 
    msg = u"Опубликовано объявлений: %s , осталось на счету: %s. " % (cnt, user.messages_quantity)
    return  render_to_response('advertisers/profi_profile.html',
        {'user': user, 'msg' : msg},
        context_instance=RequestContext(request))
    
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
        
        

def _parse_post_values(request):
    values = {}
    for key, value_list in request.POST.lists():
        if key == "new":
            continue
        if key == 'country':
            values[key] = "+".join(value_list)
        else:
            values[key] = ",".join(value_list)
    _update_values(values, request.user)
    return values
    
def preview_post(request, page_id):
    page = AdsPage.objects.get(id=page_id) 
    if (request.user.is_authenticated and type(request.user) is Advertiser) or (type(request.user) is CustomUser and page.allow_free):
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    valid, missing = validate_post(request, page_id)
    if valid:
        values = _parse_post_values(request)
        html = get_bulletin_text(page , [values])
        return render_to_response('adsman/preview_post.html', {"text" : html, "page" : page_id,
                                    "values" : values, 'url' : get_referer(request) }, context_instance=RequestContext(request))      
    else:        
        return _show_page(request, page_id, "default", _parse_post_values(request), missing)
    
def edit_from_preview(request, page_id):
    if request.user.is_authenticated and type(request.user) is Advertiser:
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    valid, missing = validate_post(request, page_id)      
    return _show_page(request, page_id, "default", _parse_post_values(request), missing)
        

def _init_post_values(entries, pcontrols):
    for entry in entries:
        for pcontrol in pcontrols:
            if entry.key == pcontrol.control.name:
                pcontrol.control.value = entry.value
    return pcontrols

def _show_for_dates(request, posts, mode = "future", defaults = {}):
    container = posts_2_html(posts)        
    return  render_to_response('adsman/future_dates.html',
        {'container' : container, 'mode': mode, 'defaults' : defaults, 'years': ",".join([str(y) for y in range(2008, date.today().year + 1)])},
        context_instance=RequestContext(request))
    

    
def get_past_dates(udate):
    date_now = get_latest_bulletin_date() #datetime.date.today() 
    if udate == "":
        month, year = date_now.month, date_now.year
    else:
        month, year = [int(chunk) for chunk in udate.split('.')]
    date_from = date(int(year), int(month), 1)
    if month == date_now.month and year == date_now.year: 
        date_to = date_now
    else:
        date_to =  date(int(year), int(month), calendar.monthrange(year, month)[1] )
    return str(month), str(year), date_from, date_to       
        

def get_past_pub_dates(request, udate = ""):
     if request.user.is_authenticated and type(request.user) is Advertiser:
        user = request.user
     else:
        return HttpResponseRedirect('/profi/login/')
     values = {}
     values['month'], values['year'], date_from, date_to  = get_past_dates(udate)
     posts = AdsPost.objects.filter(author=user, publish_date__gte = date_from, publish_date__lte = date_to).order_by('-publish_date', 'page', 'active_date', 'location')
     return _show_for_dates(request, posts, "past", values)

def get_future_pub_dates(request):
     if request.user.is_authenticated and type(request.user) is Advertiser:
        user = request.user
     else:
        return HttpResponseRedirect('/profi/login/')
     date_from = datetime.date.today()
     #date_to =  date_from + datetime.timedelta(days=90)    
     posts = AdsPost.objects.filter(author=user, publish_date__gt = date_from ).order_by('publish_date', 'page', 'active_date', 'location')
     return _show_for_dates(request, posts)
     
  
def copy_post(request, post_id):    
    if request.user.is_authenticated and type(request.user) is Advertiser:
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    post = AdsPost.objects.get(id=post_id)
    if not post.page.visible:
        return HttpResponseRedirect('/job/rubric_disabled/')
    dates = parse_pub_dates(request) #request.POST["pub_date"].split("\n")
    for date in dates:
        udate = ()
        try:
            udate = parse_user_date(date)
        except:
            continue
        if not is_pub_date_valid(udate):
            continue        
        new_post = AdsPost(page = post.page, author = post.author, publish_date = udate)
        if not _is_balance_valid(user, post):
            return HttpResponseRedirect('/profi/not_enough/')   
        if not _is_date_limit_valid(user, new_post):
            return HttpResponseRedirect('/profi/date_limit_exeed/')        
        new_post.price = post.price
        new_post.currency = post.currency  
        new_post.active_date = post.active_date
        new_post.location = post.location
        new_post.save()
        user.messages_quantity -= 1
        user.save()
        for entry in post.entries.all():
            new_entry = AdsPostEntry(post = new_post, key = entry.key, value = entry.value, position = entry.position)
            if entry.key == "pub_date":
                new_entry.value = date
            new_entry.save()
    return HttpResponseRedirect(request.POST["url"])
    

def get_copy_form (request, post_id):    
    if request.user.is_authenticated and type(request.user) is Advertiser:
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    return  render_to_response('adsman/ads_post_copy.html',
        {'post_id': post_id, 'url' : get_referer(request)},
        context_instance=RequestContext(request))



def delete_post(request, post_id):
    post = AdsPost.objects.get(id=post_id)
    if (request.user.is_authenticated and type(request.user) is Advertiser) or (type(request.user) is CustomUser and post.is_free) :
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    if not post.is_free:
        user.messages_quantity += 1
        user.save()
    post.delete()
    return HttpResponseRedirect(get_referer(request))
#    msg = u"Объявление удалено , осталось на счету: %s. " % (user.messages_quantity)
#    return  render_to_response( request.META["HTTP_REFERER"],
#        {'user': user, 'msg' : msg},
#        context_instance=RequestContext(request))
    
def edit_my_fpost (request, post_id):
    if request.user.is_authenticated and type(request.user) is Advertiser:
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    values, post = _get_post_data(post_id) 
    # get_referer(request)
    return_url = "/adspages/future/dates/"
    return render_to_response("adsman/ads_page_edit.html",
                              { "page": post.page, "post" : post, "values" : values,
                                "controls" : post.page.controls.order_by("position").all() ,
                                "mode" : "edit-post",
                                "return" : return_url } , context_instance=RequestContext(request))

    

def edit_post(request, post_id):
    try:
        values , post = _get_post_data(post_id)
    except AdsPost.DoesNotExist:
        return HttpResponseRedirect('/admin/')
    return render_to_response("adsman/ads_page_edit_adm.html",
                              { "page": post.page, "post" : post, "values" : values,
                                "controls" : post.page.controls.order_by("position").all() ,
                                "mode" : "edit-post",
                                "return" : "/admin/bulletin/preview/" + values['pub_date'] + "/" } , context_instance=RequestContext(request))

def _get_post_entry(post, key):
    try:
        return  AdsPostEntry.objects.filter(post=post, key=key)[0]
    except:
        return  AdsPostEntry(post=post, key=key)

def save_post(request, post_id):
    post = AdsPost.objects.get(id=post_id)
    if (request.user.is_authenticated and type(request.user) is Advertiser) or (type(request.user) is CustomUser and post.page.allow_free):
        user = request.user
    else:
        return HttpResponseRedirect('/profi/login/')
    valid, missing = validate_post(request, post.page.id, ignore_pubdate=True)
    if not valid:
        return _show_page(request, post.page.id, "edit-post", _parse_post_values(request), missing, post, request.POST['return_page'])
    dates = parse_pub_dates(request)
    init_post_from_request(request , post, user, dates[0])
    post.save()
    prev_entries = {}
    for prev_entry in post.entries.all():
        prev_entries[prev_entry.key] = prev_entry.id
    for key, value_list in request.POST.lists():
        #init_post_fields(post, key, value_list[0])
        if key == 'country':
            evalue = "+".join(value_list)
        else:
            evalue = ",".join(value_list)
        try:
            val = evalue.encode("cp1251")            
        except:
            continue
        if prev_entries.has_key(key):
            del(prev_entries[key])
        if key == "return_page":
            continue
        found = False
        for entry in post.entries.all():
            if key == entry.key:
                found = True
                entry.value = evalue
                entry.save()
                break
        if not found:
            AdsPostEntry.objects.create(post=post, key=key, value= evalue, position=0)
    for obsolete in prev_entries.keys():
        AdsPostEntry.objects.get(id=prev_entries[obsolete]).delete()                
    return HttpResponseRedirect(request.POST["return_page"])
            

def get_posts(request, page_id):
    page = AdsPage.objects.get(id=page_id)
    try:
        pub_date = request.GET["pub_date"]
    except:
        pub_date = None        
    posts = get_post_objects(page_id, pub_date)    
    url = get_page_template(page)
    return render_to_response(url, {"posts": posts, "mode": "default"})    

def get_post_objects(page, date=None, request=None):
    res = []
    pg = AdsPage.objects.get(id = page)
    if pg.uid == "cv":
        posts = AdsPost.objects.filter(page=page)
    else:
        posts = AdsPost.objects.filter(page=page).filter(is_free = False)
    if date != None:
        #posts = posts.filter(entries__key="pub_date", entries__value=date)
        posts = posts.filter(publish_date = parse_user_date(date) ).exclude(active_date__isnull=False, active_date__lt=parse_user_date(date))
    posts = posts.order_by('active_date')
    if request:
        ids = get_basket(request, "t-basket")
    else:
        ids = []
    emails = {}
    for post in posts:
        email = ""
        parts = {}              
        parts["id"] = post.id
        if post.author:
            parts["sender_id"] = post.author.id
            parts["sender"] = post.author.name
        else:
            parts["sender_id"] = post.user.id
            parts["sender"] = post.user.nickname            
        if str(post.id) in ids:
            parts["checked"] = "checked"
        else:
            parts["checked"] = "" 
        for entry in post.entries.all():
            try:
                #TPM
                val = entry.value.encode("cp1251")
                parts[entry.key] = entry.value 
                if entry.key == "email":
                    email =  entry.value   
            except:
                pass    
        #  or post.page.uid == "vacancy"
        if (email != "") and (post.page.uid == "cv"):
            try:
                found_mail = emails[email]
                continue
            except:
                emails[email] = 1  
        res.append(parts)
    
    return res

def _get_page_by_uid(uid):
    try:
        return AdsPage.objects.filter(uid = uid)[0]
    except:
        return None
        

def get_job_intro_page(request):  
    page =  _get_page_by_uid("vacancy")  
    if page == None:
        return HttpResponseRedirect('/job/')         
    next_day = get_user_date( get_next_pub_date())
    vacancies = load_page(page.id, next_day, "default" )
    ids = get_basket(request, "j-basket")
    dt_now = datetime.datetime.now()
    t_now = datetime.time(0,0)
    #dt = datetime.date.today()
    dt = datetime.datetime.now()
    #dt = combine(dt, t_now)
    dt_prev = dt - datetime.timedelta(days=7)
    news_top = News.objects.filter(pubdate__gte = dt_prev, pubdate__lte = dt).order_by('-count_visits')[:10]
    return render_to_response("adsman/job_intro_page.html", 
                              {"vacancies" : vacancies,  "basket_size" : len(ids), "news_top": news_top}, context_instance=RequestContext(request))
    
def _get_page_number(request):
     # Make sure page request is an int. If not, deliver first page.
    try:
        return int(request.GET.get('page', '1'))
    except ValueError:
        return 1
    
def get_basket(request, basket):
    try:
        ids = request.session[basket]
    except:
        ids = []
    return ids    
    
def get_job_page(request, uid):
    page =  _get_page_by_uid(uid)
    if page == None:
        return HttpResponseRedirect('/job/')  
    all_posts = AdsPost.objects.filter(page = page)
   
    if "vac_position" in request.POST and request.POST["vac_position"] != "":
        all_posts = all_posts.filter(entries__key = "vac_position", entries__value = request.POST["vac_position"])
    if "vac_experience" in request.POST and request.POST["vac_experience"] != "":
        all_posts = all_posts.filter(entries__key = "vac_experience", entries__value__gte = request.POST["vac_experience"])
    if "salary_from" in request.POST and request.POST["salary_from"] != "":
        all_posts = all_posts.filter(entries__key = "salary_from", entries__value__gte = request.POST["salary_from"])
    if "salary_to" in request.POST and request.POST["salary_to"] != "":
        all_posts = all_posts.filter(entries__key = "salary_to", entries__value__lte = request.POST["salary_to"])
  
    all_posts = all_posts.order_by('-publish_date')
    paginator = Paginator(all_posts, 20)
    page_number = _get_page_number(request)
    try:
        data = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        data = paginator.page(paginator.num_pages)
    container = posts_2_html(data.object_list, "job") 
    ids = get_basket(request, "j-basket")
    for entry in container:
        if str(entry["post"].id) in ids:
            entry["checked"] = "checked"
        else:
            entry["checked"] = ""           
    # get search form data
    form_page = _get_page_by_uid("search_vacancy")
    controls = form_page.controls.order_by("position").all()      
    values = _parse_pcontrol_value(controls)
    
    dt_now = datetime.datetime.now()
    t_now = datetime.time(0,0)
    #dt = datetime.date.today()
    dt = datetime.datetime.now()
    #dt = combine(dt, t_now)
    dt_prev = dt - datetime.timedelta(days=7)
    news_top = News.objects.filter(pubdate__gte = dt_prev, pubdate__lte = dt).order_by('-count_visits')[:10]
    return render_to_response("adsman/job_page.html", 
                              {"page" : form_page,  "controls" :  controls, "data_page" : page,
                               "values" : values,  "basket_size" : len(ids),
                               "container" : container, "pager" : data, "mode" : "service", "news_top": news_top }, 
                              context_instance=RequestContext(request))

def get_job_post_form(request, page_id):
     return get_page(request, page_id, "job")
 
def _store_basket_item(request, post_id, basket): 
    if basket in request.session:
        ids = request.session[basket]
        ids.append(post_id)
        request.session[basket] = ids
    else:
        request.session[basket] = [post_id]
    return HttpResponse(str( len(get_basket(request, basket)) ))
 
def store_j_item (request, post_id):
    return _store_basket_item(request, post_id, "j-basket")

def store_t_item (request, post_id):
    return _store_basket_item(request, post_id, "t-basket")

def _remove_basket_item (request, post_id, basket):
     try:
        ids = request.session[basket]
        ids.remove(post_id)
        request.session[basket] = ids
     except:
        pass
     return HttpResponse(str( len(get_basket(request, basket)) ))
 
def remove_j_item (request, post_id):
    return _remove_basket_item (request, post_id, "j-basket")

def remove_t_item (request, post_id):
    return _remove_basket_item (request, post_id, "t-basket")

def _show_basket(request, basket, mode):
    ids = get_basket(request, basket)
    posts = []
    for id in ids:
        try:
            posts.append(AdsPost.objects.get(id = id) ) 
        except:
            pass
    container = posts_2_html(posts, "job") 
    return container, ids

def t_basket(request):
    container, ids =  _show_basket(request, "t-basket", "ta")      
    return render_to_response("adsman/ta_basket.html", 
                               {"container" : container, "basket_size" : len(ids)}, context_instance=RequestContext(request))
    
def j_basket(request):
    container, ids =  _show_basket(request, "j-basket", "job")      
    return render_to_response("adsman/job_basket.html", 
                               {"container" : container, "basket_size" : len(ids)}, context_instance=RequestContext(request))
    
        
def add_to_favorites(request, id):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    user = request.user
    fav, created = FavoriteAdsPost.objects.get_or_create(user_id=user.id, post_id=id)
    return HttpResponse(simplejson.dumps({'success': True, 'created': created, 'text': u"Объявление добавлено в избранное"}))

def remove_from_favorites(request, id):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    user = request.user
    FavoriteAdsPost.objects.filter(user__id=user.id, post__id=id).delete()
    return HttpResponse(simplejson.dumps({'success': True, 'text': u"Объявление удалено из избранного"}))

@login_required
def favorites(request):
    user = request.user
    favorites = FavoriteAdsPost.objects.filter(user__id=user.id).order_by('post__page', 'post__active_date')
    return render_to_response('adsman/favorites.html', {'favorites': favorites}, context_instance=RequestContext(request))


        




