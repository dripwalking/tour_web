# -*- coding: utf-8 -*-
import random
import re
import sha
import urllib
import urllib2
import datetime


from django.template import Context, loader
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from urllib2 import Request, urlopen, URLError, HTTPError

import datetime
import calendar
from datetime import date, timedelta, time
import tourprom.settings
from tourprom.adsman.models import *
from tourprom.bulletin.models import *
from tourprom.bulletin.forms import *
from tourprom.adsman.views import *
from tourprom.news.models import News
from tourprom.advertisers.models import Informer, Announcement, Expert, Interview, ChangedDate, CatalogReservation
from tourprom.countries.models import *
from tourprom.accounts.models import *
from tourprom.community.models import *
from tourprom.currency.models import *
from tourprom.photo.models import PhotoGallery, Picture
from tourprom.weather.models import *
from tourprom.tv.models import Video


def _send_local(subs, subject, body, bulletin):
    total = sent = 0
    failed = []
    already_sent = []
    for sub in subs:
        try:
            total = total + 1
            if _was_sent_to(bulletin, sub.email):
                already_sent.append(sub.email)
            else:
                msg = EmailMessage(subject, body, tourprom.settings.SUBSCRIPTION_FROM_EMAIL, [sub.emai])
                msg.content_subtype = "html"
                msg.send()
                sent = sent + 1
                log = BulletinLog(bulletin=bulletin, email=sub.emai)
                log.save()
        except:
            failed.append(sub.email)
    return total, sent, already_sent, failed

def _do_http(url, values):
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, {"content-type": 'application/x-www-form-urlencoded; charset=windows-1251'})
        response = urllib2.urlopen(req)
        return response.read()
#    except URLError, e:
#        return e.reason
    except HTTPError, e:
        return e.read()


    
def get_dict_for_bulletin(pub_date, bulletin, mode= "default" ):
    dict = _load_posts(pub_date, mode)
    dict["bulletin_date"] = parse_user_date(pub_date)
    dict["post_count"] =  AdsPost.objects.filter(publish_date = parse_user_date(pub_date) ).filter(is_free = False).count()
    dict["post_avia_count"] =  AdsPost.objects.filter(publish_date = parse_user_date(pub_date) ).filter(is_free = False).filter(page__parent__uid = 'avia').count()
    dict["post_tour_count"] =  AdsPost.objects.filter(publish_date = parse_user_date(pub_date) ).filter(is_free = False).filter(page__parent__uid = 'tour').count()
    dict["post_vacancy_count"] =  AdsPost.objects.filter(publish_date = parse_user_date(pub_date) ).filter(is_free = False).filter(page__uid = 'vacancy').count()
    dict["post_cv_count"] =  AdsPost.objects.filter(publish_date = parse_user_date(pub_date) ).filter(is_free = False).filter(page__uid = 'cv').count()
    dict["post_rest_count"] = dict["post_count"] - dict["post_avia_count"] - dict["post_tour_count"] - dict["post_vacancy_count"] - dict["post_cv_count"]
    dict["news"] = _get_news_text(parse_user_date(pub_date), mode)
    dict["headlines"] = _get_headlines_text(parse_user_date(pub_date), mode)
    dict["informers"] = _get_informer_text(parse_user_date(pub_date), mode)
    dict["anounces"] = _get_anounces_text(parse_user_date(pub_date), mode)
    dict["catalogs"] = _get_catalog_text(parse_user_date(pub_date), mode)
    dict["quest"] = _get_quest_text(parse_user_date(pub_date), mode)
    dict["expert"] = _get_expert_text(parse_user_date(pub_date), mode)
    dict["interview"] = _get_interview_text(parse_user_date(pub_date), mode)
    dict["video"] = _get_video_text(parse_user_date(pub_date), mode)
    dict["photogallery"] = _get_photogallery_text(parse_user_date(pub_date), mode)
    dict["mode"] = "email"
    dict["issue"] = bulletin.issue_number
    dict["issue_year"] = bulletin.issue_year_number
    dict["usd_mail"] = _get_currency_head('USD')
    dict["eur_mail"] = _get_currency_head('EUR')
    dict["currency_date"] = _get_currency_date('USD')
    dict["weather_res"] = _get_weather_result(parse_user_date(pub_date), mode)
    dict["subs_count"] = Subscription.objects.filter(active = True).count()
    dict["job_messages"] = _get_job_text(parse_user_date(pub_date), mode)
    return dict

def get_bulletin_text_and_objects(pub_date):
    bulletin = _get_bulletin(pub_date, True)
    dict = get_dict_for_bulletin(pub_date, bulletin)
    subject = u"Бюллетень №%s (%s), %s" % (bulletin.issue_year_number, bulletin.issue_number, pub_date)
    body = render_template('bulletin/bulletin_new.html', dict)
    return body, subject, bulletin


def _load_posts(pub_date, mode = "default", request = None):
    entries = []
    for page in AdsPage.objects.exclude(parent = None).order_by('parent__id'):
        entry = {}
        entry['html'] = load_page(page.id, pub_date, mode, request)
        entry['page'] =  page
        if entry['html'] != "":
            entries.append( entry )
    return {"entries" : entries, "pub_date": pub_date}

def _get_post_parts(post):
    parts = {}
    parts["id"] = post.id
    if post.active_date:
        parts["active_date"] = post.active_date
    else:
        parts["active_date"] = None
    parts["id"] = post.id
    if post.author:
        parts["sender_id"] = post.author.id
        parts["sender"] = post.author.name
    else:
        parts["sender_id"] = post.user.id
        parts["sender"] = post.user.nickname 
    for item in post.entries.all():
        try:
            parts[item.key] = item.value
        except:
            pass
    return parts

    
def _get_test_object(post, parts):
    obj = {}
    obj["page"] = post.page
    if post.author:
        obj["user"] = post.author.id
    else:
        obj["user"] = post.user.id
    if post.active_date:
        obj["date"] = post.active_date
    if post.price and post.currency:
        obj["price"] = "%s %s" % (post.price, post.currency)
        
    if "avia_route_2" in parts.keys():
        obj["avia_route"] = parts["avia_route_2"]
    elif "country" in parts.keys():
        obj["country"] = parts["country"]
        if "resort" in parts.keys():
            obj["resort"] = parts["resort"]
    elif "resort" in parts.keys():
        obj["resort"] = parts["resort"]
    elif "marshrut" in parts.keys():
        obj["marshrut"] = parts["marshrut"]
    elif "dop_info" in parts.keys():
        obj["dop_info"] = parts["dop_info"]
    elif "add_condition" in parts.keys():
        obj["add_condition"] = parts["add_condition"]
    else:
        return None
    return obj
            
def _load_actual_posts():
    entries = []
    i = 0
    for page in AdsPage.objects.exclude(parent = None).order_by('parent__id'):
        entry = {}

        last_date = get_latest_bulletin_date()
        next_date = get_next_pub_date(last_date)
        from_date = last_date - timedelta(days=3)
        posts= AdsPost.objects.filter(page=page, is_free = False)
        posts_1 = posts.filter( publish_date = next_date ).exclude(active_date__isnull=False, active_date__lt = date.today()).order_by('active_date')
        posts_2 = posts.filter( Q(publish_date__lte = last_date, publish_date__gt = from_date, active_date__isnull=False, active_date__gte = date.today()) | Q(publish_date__lte = last_date, publish_date__gt = from_date, active_date__isnull=True) ).order_by('active_date', '-publish_date')
        res_list = []
        test_list = []
        for post in posts_1:
            parts = _get_post_parts(post)
            test_obj = _get_test_object(post, parts)
            if test_obj:
                test_list.append(test_obj)
            parts["is_new"] = True
            res_list.append(parts)
        for post in posts_2:
            parts = _get_post_parts(post)
            test_obj = _get_test_object(post, parts)
            if not (test_obj and test_obj in test_list):
                test_list.append(test_obj)
                res_list.append(parts)
        res_list = sorted(res_list, key=lambda obj: obj["active_date"])
        if len(res_list)== 0:
            entry['html'] = ""
        else:
            entry['html'] = get_bulletin_text(page, res_list, 'site')
        entry['page'] =  page
        if entry['html'] != "":
            entries.append( entry )
    return {"entries" : entries, "pub_date": last_date}
    
# FAKE - give "mail-preview" for preview
def _get_news_text_fake(pub_date, mode = "mail-preview"):
    news = News.objects.filter(bulletin_date=pub_date, published=True, bulletin=True)
    return render_to_string('bulletin/news.html', {'news': news, 'mode': mode, 'pub_date': pub_date, 'site': Site.objects.get_current()})

# FAKE - give "mail-preview" for preview
def _get_headlines_text_fake(pub_date, mode = "mail-preview"):
    headlines = News.objects.filter(bulletin_date=pub_date, published=True, bulletin_short=True)
    return render_to_string('bulletin/headlines.html', {'headlines': headlines, 'mode': mode, 'pub_date': pub_date, 'site': Site.objects.get_current()})


def _get_news_text(pub_date, mode = "default"):
    news = News.objects.filter(bulletin_date=pub_date, published=True, bulletin=True)
    return render_to_string('bulletin/news_new.html', {'news': news, 'mode': mode, 'pub_date': pub_date, 'site': Site.objects.get_current()})

def _get_headlines_text(pub_date, mode = "default"):
    headlines = News.objects.filter(bulletin_date=pub_date, published=True, bulletin_short=True)
    return render_to_string('bulletin/headlines_new.html', {'headlines': headlines, 'mode': mode, 'pub_date': pub_date, 'site': Site.objects.get_current()})

def _get_informer_text(pub_date, mode = "default"):
    informers = Informer.objects.filter(pubdate=pub_date)
    return render_to_string('bulletin/informers_new.html', {'informers': informers, 'mode': mode, 'site': Site.objects.get_current()})

def _get_catalog_text(pub_date, mode = "default"):
    reserves = CatalogReservation.objects.filter(bulletin_publish_date=pub_date)
    if len(reserves) == 0:
        reserves = []
        advertisers = []
        reserves_tmp = CatalogReservation.objects.filter(year=pub_date.year, month=pub_date.month, catalog__converted=True, bulletin_publish_date=None)
        for reserve in reserves_tmp:
            if not reserve.user.id in advertisers:
                reserve.bulletin_publish_date = pub_date
                reserve.save()
                reserves.append(reserve)
                advertisers.append(reserve.user.id)
    if len(reserves) > 0:
        return render_to_string('bulletin/catalogs.html', {'reserves': reserves, 'mode': mode, 'site': Site.objects.get_current()})
    reserves = CatalogReservation.objects.filter(year=pub_date.year, month=pub_date.month, catalog__converted=True)
    if len(reserves) > 0:
        return render_to_string('bulletin/catalogs_short.html', {'reserves': reserves, 'mode': mode, 'site': Site.objects.get_current()})
    return ""

def _get_job_text(pub_date, mode = "default"):
    from tourprom.job.models import BulletinVacancy, Resume
    vacancies = BulletinVacancy.objects.filter(date=pub_date)
    try:
        prev_bulletin = Bulletin.objects.filter(date__lt=pub_date).order_by('-date')[0]
        resumes = Resume.objects.filter(date_changed__lt=datetime.combine(pub_date, time()), date_changed__gt=datetime.combine(prev_bulletin.date, time()), is_published=True)
    except IndexError:
        resumes = []

    return render_to_string('bulletin/job_messages.html', {'vacancies': vacancies, 'resumes': resumes, 'mode': mode, 'site': Site.objects.get_current()})

def _get_anounces_text(pub_date, mode = "default"):
    anounces = Announcement.objects.filter(pubdate=pub_date, approved=True)
    return render_to_string('bulletin/anounces_new.html', {'anounces': anounces, 'mode': mode, 'site': Site.objects.get_current()})
    
def _get_interview_text(pub_date, mode = "default"):
    interviews = Interview.objects.filter(pubdate=pub_date, approved=True)
    if len(interviews) > 0:
        return render_to_string('bulletin/interview_new.html', {'interview': interviews[0], 'mode': mode, 'site': Site.objects.get_current()})
    return ""

def _get_expert_text(pub_date, mode = "default"):
    expert = Expert.objects.filter(pubdate__lte=pub_date, enddate__gte=pub_date, approved=True, is_special=False)
    spec_expert = Expert.objects.filter(pubdate__lte=pub_date, enddate__gte=pub_date, approved=True, is_special=True)
    if len(expert) > 0 or len(spec_expert) > 0:
        if len(expert) > 0:
            exp = expert[0]
        else:
            exp = None
        if len(spec_expert) > 0:
            spec_exp = spec_expert[0]
        else:
            spec_exp = None
        return render_to_string('bulletin/expert_new.html', {'expert': exp, 'special_expert': spec_exp, 'mode': mode, 'site': Site.objects.get_current()})
    return ""

def _get_quest_text(pub_date, mode = "default"):
    from quest.models import Tour
    tours = Tour.objects.filter(startdate__lte=pub_date, enddate__gte=pub_date).order_by('-startdate')
    if len(tours) > 0:
        return render_to_string('bulletin/quest_new.html', {'quest_tour': tours[0], 'mode': mode, 'site': Site.objects.get_current()})
    return ""

def _get_video_text(pub_date, mode = "default"):
    videos = Video.objects.filter(bulletin_date=pub_date, published=True, bulletin=True)
    video_count = videos.count()
    return render_to_string('bulletin/tv_new.html', {'videos': videos, 'video_count': video_count,  'mode': mode, 'pub_date': pub_date, 'site': Site.objects.get_current()})

def _get_photogallery_text(pub_date, mode = "default"):

    weekday = pub_date.weekday()
    if weekday == 0:
        ts = time(0,0)
        te = time(23,59)
        holidays = ChangedDate.objects.filter(date=pub_date,publish=False)
        if len(holidays) > 0:
            dt_s = datetime.combine(pub_date - timedelta(days=4), ts)
        else:
            dt_s = datetime.combine(pub_date - timedelta(days=3), ts)
        dt_e = datetime.combine(pub_date - timedelta(days=1), te)

        photos = PhotoGallery.objects.filter(date_added__lte=dt_e, date_added__gte=dt_s, gallery_type=2)
        photos_count = photos.count()

    else:
        ts = time(0,0)
        te = time(23,59)
        holidays = ChangedDate.objects.filter(date=pub_date,publish=False)
        if len(holidays) > 0:
            dt_s = datetime.combine(pub_date - timedelta(days=2), ts)
        else:
            dt_s = datetime.combine(pub_date - timedelta(days=1), ts)
        dt_e = datetime.combine(pub_date - timedelta(days=1), te)

        photos = PhotoGallery.objects.filter(date_added__lte=dt_e, date_added__gte=dt_s, gallery_type=2)
        photos_count = photos.count()


    return render_to_string('bulletin/photo_gallery_new.html', {'photos': photos, 'photos_count': photos_count,  'mode': mode, 'pub_date': pub_date, 'site': Site.objects.get_current()})

def send(request, pub_date):
    body, subject, bulletin = get_bulletin_text_and_objects(pub_date)
    bulletin.save()
    subs =  Subscription.objects.filter(active = True)
    if request.POST.has_key("from") and request.POST["from"] != "":
        subs = subs.filter(email__gte = request.POST["from"])
    if request.POST.has_key("to") and request.POST["to"] != "":
        subs = subs.filter(email__lte = request.POST["to"])
    subs = subs.order_by('email')
    if "server" in request.POST:
        server = request.POST["server"]
    else:
        server = "remote"
    if server == "local":
        total = sent = already_sent = failed = _send_local(subs, subject, body, bulletin)
        return render_to_response('bulletin/bulletin_report.html', {"total" : total, 
                        "sent" : sent, "failed" : failed, "ignored": already_sent} )
    else:
        return HttpResponse(_send_remote(subs, subject, body, pub_date) )

#

def _was_sent_to (bulletin, email):
    try:
        obj = BulletinLog.objects.filter(bulletin = bulletin, email = email)[0]
        return True
    except:
        return False
    
    

def _get_bulletin(user_date, auto_create = False):
    dt = parse_user_date(user_date)
    try:
        return Bulletin.objects.get(date = dt)
    except:
        if auto_create:
            latest = get_latest_bulletin()
            if latest.date.year == dt.year:
                issue_year_number = latest.issue_year_number + 1
            else:
                issue_year_number = 1
            bulletin = Bulletin(date = dt, issue_number = latest.issue_number + 1, issue_year_number = issue_year_number)
            bulletin.save()
            return bulletin
        return None
    
def _get_currency_value(code): 
     currency = CurrencyValues.objects.filter(code__code = code).order_by('-datetime')[0]
     return float(currency.tax)   
 
def _get_cheapest(parent_id):
    bt = get_latest_bulletin()
    posts = AdsPost.objects.filter(publish_date = bt.date, price__gt = 0, page__parent__id = parent_id ).order_by('price_rub')[0:3]
    return posts

@cache_page(60 * 5)
def get_top3x3(request):
    #magic numbers below
    dict = {}
    dict["avia"] = _get_cheapest(16)
    dict["foreign"] = _get_cheapest(18)
    dict["russia"] = _get_cheapest(21)
    return render_to_response('bulletin/top3.html', dict)


def init_rub_price(date):
    posts = AdsPost.objects.filter(publish_date = parse_user_date(date), price__gt = 0 ).exclude(currency = None)
    rates = {}
    rates["USD"] = _get_currency_value("USD")
    rates["EUR"] = _get_currency_value("EUR")
    rates["RUB"] = float(1.0)
    for post in posts:
        if post.currency == None or post.currency == "" or post.currency not in ["USD", "EUR", "RUB"]:
            continue
        post.price_rub = int( post.price * rates[post.currency] )
        post.save()

def _get_currency_head(code):
    res = ''
    tax = ''
    dt = ''
    dt_prev = ''
    exist_prev = True
    tax_delta = ''
    try:
        entry = CurrencyValues.objects.filter(code__code = code)[0]
        tax = str(entry.tax)
        dt = entry.date

        dt_prev = dt - timedelta(days=1)
        try:
            entry_prev = CurrencyValues.objects.filter(code__code__exact=code)[:2]
            for ff in entry_prev:
                tax_prev = str(ff.tax)
                dt_prev = ff.date
        except:
            exist_prev = False
        if exist_prev:
            if (float(tax) >= float(tax_prev)):
                tax_delta = '<img src="http://www.tourprom.ru/site_media/images/arrow_top.gif">&nbsp;<span style="font-size: 0.8em;color: green;">+' + str(round(float(tax) - float(tax_prev),4)) + '</span>'
            else:
                tax_delta = '<img src="http://www.tourprom.ru/site_media/images/arrow_bottom.gif">&nbsp;<span style="font-size: 0.8em;color: red;">' + str(round(float(tax) - float(tax_prev),4)) + '</span>'

        res = '<table cellpadding="2" cellspacing="2" style="font-size: 0.9em;"><tbody><tr valign="top"><td width="65" align="center"><span style="font-size: 1.1em;font-weight: bold;">' + code + '</span><br><span style="font-size: 0.8em;">' + dt.strftime('%d.%m.%y') + '</span></td><td width="65""><span style="font-weight: bold;">' + tax + '</span><br>' + tax_delta + '</td></tr></tbody></table>'
    except:
        res = ' '

    return res

def _get_currency_date(code):
    res = ''
    try:
        entry = CurrencyValues.objects.filter(code__code = code)[0]
        res = entry.date
    except:
        res = ' '
        
    return res

def _get_weather_result(pub_date, mode = "default"):
    res = ''
    dt = pub_date

    resorts = ResortTable.objects.filter(show=True)
    r_list = []
    for f in resorts:
        r_list.append(f.id)

    for n in r_list:
        t_day = ''
        t_night = ''
        pict = ''
        city_list = ResortTable.objects.get(id=str(n))

        weather = WeatherTable.objects.filter(resort_table=str(n), date = pub_date)
        if weather.count() != 0:
            for f in weather:
                if str(f.hour) == '15':
                    t_day = str(f.t_max)
                    pict = str(f.pict)
                if str(f.hour) == '21':
                    t_night = str(f.t_min)

            res += '<div style="text-align: left;font-size: 0.9em;padding-top: 10px;"><strong>' + str(city_list.resort) + '</strong> (' +  str(city_list.country_table.country) +'):<br/>'
            res += '<img src="http://www.tourprom.ru/site_media/images/weather/' + pict + '" width="18" height="18">&nbsp;'
            res += '<span style="vertical-align: top;">День: ' + t_day + '</span>&nbsp;'
            res += '<span style="vertical-align: top;">Ночь: ' + t_night + '</span></div>'

    return res



def preview(request, user_date):
    bulletin = _get_bulletin(user_date)
    exists = False
    if bulletin != None:
        exists = True
    else:
        bulletin = get_latest_bulletin()
        bulletin.issue_year_number += 1
    dict = get_dict_for_bulletin(user_date, bulletin, "mail-preview")
    # FAKE - give "mail-preview" for preview
    #dict = get_dict_for_bulletin_fake(user_date, bulletin, "mail-preview")
    if not exists:
        dict["bulletin_already_exists"] = True
    init_rub_price(user_date)
    return render_to_response('bulletin/bulletin_preview_new.html', dict)
   
def trade_area_old(request, user_date):
    if user_date == "tomorrow":
        user_date = get_user_date(get_next_pub_date(get_latest_bulletin_date()) ) 
    else:
        if user_date == None or user_date == "" or _get_bulletin(user_date) == None:
            user_date = get_user_date(get_latest_bulletin_date()) #datetime.date.today()
    dict = cache.get('trade_area_old_%s' % user_date)
    if dict == None:
        dict = _load_posts(user_date, "site", request)
        dict["pub_date"] = user_date
        #dict["basket_size"] =  str( len( get_basket(request, "t-basket")))
        dict["years"] = ",".join([str(y) for y in range(2008, date.today().year + 1)])
        cache.set('trade_area_old_%s' % user_date, dict, 60*30)

    return render_to_response('bulletin/trade_area.html', dict, context_instance=RequestContext(request))

def trade_area(request):
    import zlib
    import cPickle
    user_date = get_user_date(get_latest_bulletin_date())
    z = cache.get('trade_area')
    if z:
        dict = cPickle.loads(zlib.decompress(z))
    else:
        dict = _load_actual_posts()
        dict["pub_date"] = user_date
        dict["years"] = ",".join([str(y) for y in range(2008, date.today().year + 1)])
        z = zlib.compress(cPickle.dumps(dict))
        cache.set('trade_area', z, 60*30)
    
    favorites = []
    if request.user.is_authenticated():
        favorites = FavoriteAdsPost.objects.filter(user__id=request.user.id).values_list('post__id', flat=True)
    dict["favorites"] = favorites
    dict["favorites_count"] = len(favorites)
    
    return render_to_response('bulletin/trade_area.html', dict, context_instance=RequestContext(request))
    
def trade_area_search(request, mode):
    last_date = get_latest_bulletin_date()
    next_date = get_next_pub_date(last_date)
    from_date = last_date - timedelta(days=7)
    location = ""

    flt  = AdsPost.objects.filter(publish_date__gt = from_date, publish_date__lte = next_date, active_date__isnull=False, active_date__gte = date.today())
    if mode == "avia":
        if ( "airport" in request.GET)  and (request.GET['airport'] != "" ):
            flt = flt.filter(entries__key = 'avia_route_2', entries__value = request.GET['airport'])
            location = request.GET['airport']
        else:
            return HttpResponseRedirect("/tradearea/")
    else:
        if ( "country" in request.GET)  and (request.GET['country'] != "" ):  
            flt = flt.filter(entries__key = 'country', entries__value = request.GET['country']) 
            location = request.GET['country']
        else:
            return HttpResponseRedirect("/tradearea/")
    flt = flt.order_by('active_date', '-publish_date')

    entries = []
    test_list = []
    for post in flt:
        parts = _get_post_parts(post)
        test_obj = _get_test_object(post, parts)
        if not (test_obj and test_obj in test_list):
            test_list.append(test_obj)
            entries.append({'html': get_bulletin_text(post.page, [parts], "simple", True), 'post': post})
    
    favorites = []
    if request.user.is_authenticated():
        favorites = FavoriteAdsPost.objects.filter(user__id=request.user.id).values_list('post__id', flat=True)
    
    return render_to_response('bulletin/trade_area_search.html', 
                                {
                                    "entries" : entries,
                                    "favorites": favorites,
                                    "favorites_count": len(favorites),
                                    "location": location
                                },
                                context_instance=RequestContext(request))


def trade_area_avia(request):
	return trade_area_search(request, "avia")
	
def trade_area_tour(request):
	return trade_area_search(request, "tour")
    
  
def _send_remote(subs, subject, body, pub_date):
    emails = ",".join([sub.email.strip() for sub in subs ] )
    values = {'emails': emails, 'subj' : subject.encode(tourprom.settings.MAIL_ENCODING),
               'text' : body.encode(tourprom.settings.MAIL_ENCODING), "date": pub_date,
               'tp_key' : tourprom.settings.MAILER_KEY }
    return  _do_http (settings.REMOTE_MAILER_URL, values)
     

def start(request):
    return render_to_response('bulletin/bulletin_start.html')

def subscribe(request):
    from accounts.models import CustomUser
    from advertisers.models import Advertiser

    if request.user.is_authenticated():
        if type(request.user) is CustomUser:
            return HttpResponseRedirect('/accounts/profile/%s/' % request.user.id)
        if type(request.user) is Advertiser:
            return HttpResponseRedirect('/profi/emails/')
    return HttpResponseRedirect('/registration/')


    """
    from tourprom.accounts.models import CompanyType
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():

            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+form.cleaned_data["email"]).hexdigest()
            company_type = CompanyType.objects.get(id=form.cleaned_data["company_type"])
            if form.cleaned_data["city_choice"] == u'Москва':
                city = u'Москва'
            else:
                city = form.cleaned_data["city"]
            activation = SubscriptionActivation(email=form.cleaned_data["email"], activation_key=activation_key,
                            company=form.cleaned_data["company"], company_type=company_type.name, city=city,
                            phone=form.cleaned_data["phone"], contact_person=form.cleaned_data["contact_person"], date=datetime.now())
            activation.save()

            subject = u'Активация подписки на бюллетень "Турпрома"'
            body = render_to_string('bulletin/subscription_message.html', { 'activation_key': activation_key })
            msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data["email"]])
            msg.content_subtype = "html"
            msg.send()

            return HttpResponseRedirect('/bulletin/subscribe_done/')
    else:
        form = SubscribeForm()

    return render_to_response("bulletin/subscribe.html",
                              {"form": form,},
                              context_instance=RequestContext(request))
    """

def activate_subscription(request):

    if request.method == 'GET' and 'ak' in request.GET:
        try:
            act = SubscriptionActivation.objects.get(activation_key=request.GET['ak'])
        except SubscriptionActivation.DoesNotExist:
            return HttpResponseRedirect("/bulletin/subscribe_notvalid/")

        check = Subscription.objects.filter(email=act.email)
        if len(check) > 0:
            sub = check[0]
            if not sub.active:
                sub.active = True
                sub.save()
        else:
            sub = Subscription(email=act.email, active=True)
            sub.save()

        subject = u'Активация подписки на бюллетень "Турпрома"'
        body = render_to_string('bulletin/subscription_message_confirm.html',
                                {'email': act.email,
                                 'company': act.company,
                                 'company_type': act.company_type,
                                 'city': act.city,
                                 'phone': act.phone,
                                 'contact_person': act.contact_person})
        msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.FEEDBACK_EMAIL])
        msg.content_subtype = "html"
        try:
            msg.send()
        except:
            pass

        act.delete()
        return HttpResponseRedirect('/bulletin/subscribe_active/')

    return HttpResponseRedirect("/bulletin/subscribe_notvalid/")


def unsubscribe(request):
    email = ""
    if request.method == 'POST' and "email" in request.POST:
        email = request.POST["email"]
        sub = Subscription.objects.filter(email=email)
        sub.delete()
        return HttpResponseRedirect('/bulletin/unsubscribe_done/')
    elif request.method == 'GET' and "email" in request.GET:
        email = request.GET["email"]
    else:
        return render_to_response("bulletin/unsubscribe_form.html",
                                  {},
                                  context_instance=RequestContext(request))

    return render_to_response("bulletin/unsubscribe.html",
                              {"email": email,},
                              context_instance=RequestContext(request))

def add_subscriptions(request):
    messages = []
    if request.method == 'POST' and "emails" in request.POST:
        emails = request.POST["emails"]
        list = emails.split('\n')
        total, new, changed = len(list), 0, 0
        if request.POST["status"] == 'add':
            for email in list:
                try:
                    email.decode('ascii')
                except UnicodeEncodeError:
                    continue
                email = email.strip()
                subs = Subscription.objects.filter(email=email)
                if len(subs) > 0:
                    for sub in subs:
                        sub.active = True
                        sub.save()
                        changed = changed + 1
                else:
                    if email.find('@')>0:
                        sub = Subscription(email=email, active=True)
                        sub.save()
                        new = new + 1
        elif request.POST["status"] == 'delete':
            for email in list:
                email = email.strip()
                subs = Subscription.objects.filter(email=email)
                subs.delete()

        if request.POST["status"] == 'add':
            messages.append(u"Подписки добавлены и активированы. Всего в списке: %s, добавлено новых: %s, активировано: %s" % (total, new, changed))
        elif request.POST["status"] == 'delete':
            messages.append(u"Подписки удалены")

    return render_to_response("admin/add_subscriptions.html", {'messages': messages},
                              context_instance=RequestContext(request))
add_subscriptions = staff_member_required(add_subscriptions)

def ajax_subscribe(request):
    email = ""
    status = 0
    if request.method == 'POST' and "email" in request.POST:
        email = request.POST["email"]
        status = int(request.POST["status"])
    elif request.method == 'GET' and "email" in request.GET:
        email = request.GET["email"]
        status = int(request.GET["status"])
    else:
        return HttpResponse("")
    subs = Subscription.objects.filter(email=email)
    if len(subs) > 0:
        subs.update(active=bool(status))
    elif status == 1:
        sub = Subscription(email=email, active=True)
        sub.save()
    return HttpResponse(str(status))


