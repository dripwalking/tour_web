# -*- coding: utf-8 -*-
from django.db import models
from tourprom.advertisers.models import Advertiser
from tourprom.accounts.models import CustomUser
from django.contrib.auth.models import User

# Rubrics and controls for adverts (used by old and new advert models both)

class AdsControl(models.Model):
    name        =  models.CharField(max_length=200)
    caption     =  models.CharField(max_length=200)
    type        =  models.CharField(max_length=20, null=True,blank=True)
    delimiter   =  models.CharField(max_length=1, default = ",")
    value       =  models.CharField(max_length=2000, null=True,blank=True, default = "")
    hint        =  models.CharField(max_length=200, null=True,blank=True, default = "")
    constraint  =  models.CharField(max_length=200, null=True,blank=True, default = "") 
    def __unicode__(self):
        return self.name    


class AdsPage(models.Model):
    parent = models.ForeignKey('self',null=True,blank=True, related_name="children")
    title       = models.CharField(max_length=200)
    template    = models.CharField(max_length=200, null=True,blank=True)
    uid         = models.CharField(max_length=30,  null=True,blank=True,default = "")
    allow_free  = models.BooleanField(default=False)
    visible      = models.BooleanField(default=True)
    limit       = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title

class AdsPlacedControl(models.Model):
    control     =  models.ForeignKey(AdsControl)
    page        =  models.ForeignKey(AdsPage, related_name='controls')
    position    =  models.IntegerField()
    hidden      =  models.BooleanField(default=False)
    mandatory   =  models.BooleanField(default=False)
    def __unicode__(self):
        return "Control " + str(self.control) + " on " + str(self.page)

        
# Old AdsPost models
        
class AdsPost(models.Model):
    page        =  models.ForeignKey(AdsPage)
    author      =  models.ForeignKey(Advertiser, null=True, blank=True)
    user        =  models.ForeignKey(CustomUser, null=True, blank=True)
    publish_date = models.DateField(u'Дата публикации', null=True, blank=True)
    price        = models.IntegerField(null=True, blank=True)
    currency     = models.CharField(max_length=4, null=True, blank=True)
    active_date  = models.DateField(u'Дата тура', null=True, blank=True)
    price_rub    = models.IntegerField(null=True, blank=True)
    location     = models.CharField(max_length=100, null=True, blank=True)
    is_free      = models.BooleanField(default=False)
    date_added   = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return "%s %s %s " % ( unicode(self.page), unicode(self.author), self.publish_date )

    def parts(self):
        parts = {}
        parts["id"] = self.id
        if self.author:
            parts["sender_id"] = self.author.id
            parts["sender"] = self.author.name
        else:
            parts["sender_id"] = self.user.id
            parts["sender"] = self.user.nickname            
        for entry in self.entries.all():
            try:
                parts[entry.key] = entry.value 
            except:
                pass
        return parts
    
    def html(self):
        from tourprom.adsman.views import get_bulletin_text
        return get_bulletin_text(self.page, [self.parts()], 'simple')

    class Meta:
        verbose_name = u'Объявление'
        verbose_name_plural = u'Объявления'
        
        
class AdsPostEntry(models.Model):
    post        =  models.ForeignKey(AdsPost, related_name='entries')
    key         =  models.CharField(max_length=200)
    value       =  models.CharField(max_length=500)
    position    =  models.SmallIntegerField()
    def __unicode__(self):
        return self.key + " : " + self.value
    
class InvalidBalance(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FavoriteAdsPost(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(AdsPost)

    def __unicode__(self):
        return '%s' % self.post

    class Meta:
        verbose_name = u'Избранное объявление'
        verbose_name_plural = u'Избранные объявления'
    
# New Advert models (ex AdsPost)

class Advert(models.Model):
    page        =  models.ForeignKey(AdsPage, verbose_name=u'Рубрика')
    author      =  models.ForeignKey(Advertiser, verbose_name=u'Дата публикации')
    price        = models.IntegerField(u'Цена', null=True, blank=True)
    currency     = models.CharField(u'Валюта', max_length=4, null=True, blank=True)
    price_rub    = models.IntegerField(u'Цена в руб.', null=True, blank=True)
    active_date  = models.DateField(u'Дата тура', null=True, blank=True)
    location     = models.CharField(u'Направление', max_length=100, null=True, blank=True)
    is_free      = models.BooleanField(u'Бесплатно', default=False)
    date_added   = models.DateTimeField(u'Дата добавления', auto_now_add=True, null=True)
    date_changed = models.DateTimeField(u'Дата изменения', auto_now=True, null=True)

    def __unicode__(self):
        return "%s %s " % ( unicode(self.page), unicode(self.author) )

    def parts(self):
        parts = {}
        parts["id"] = self.id
        if self.author:
            parts["sender_id"] = self.author.id
            parts["sender"] = self.author.name
        else:
            parts["sender_id"] = self.user.id
            parts["sender"] = self.user.nickname            
        for entry in self.entries.all():
            try:
                parts[entry.key] = entry.value 
            except:
                pass
        return parts
    
    def html(self):
        from tourprom.adsman.views import get_bulletin_text
        return get_bulletin_text(self.page, [self.parts()], 'simple')

    class Meta:
        verbose_name = u'Объявление'
        verbose_name_plural = u'Объявления'

class AdvertEntry(models.Model):
    advert        =  models.ForeignKey(Advert, related_name='entries')
    key         =  models.CharField(max_length=200)
    value       =  models.CharField(max_length=500)
    position    =  models.SmallIntegerField()

    def __unicode__(self):
        return self.key + " : " + self.value
        
class AdvertDate(models.Model):
    advert = models.ForeignKey(Advert, related_name='bulletins')
    date = models.DateField()
    advertiser = models.ForeignKey(Advertiser)

    class Meta:
        verbose_name = u'Показ объявления в бюллетене'
        verbose_name_plural = u'Показы объявления в бюллетене'
        ordering = ['-date']

    @property
    def is_past(self):
        if date.today() >= self.date:
            return True
        return False        

class FavoriteAdvert(models.Model):
    user = models.ForeignKey(User)
    advert = models.ForeignKey(Advert)

    def __unicode__(self):
        return '%s' % self.advert

    class Meta:
        verbose_name = u'Избранное объявление'
        verbose_name_plural = u'Избранные объявления'
        