# -*- coding: utf-8 -*-
from django.db import models
from tourprom.advertisers.models import Informer, Announcement

class Subscription(models.Model):
    email = models.EmailField(u'E-mail')
    active = models.BooleanField(u'Активный')
    newsdigest_active = models.BooleanField(u'Активная подписка на Туристический вестник', default=False)
    
    class Meta:
        ordering = ('email',)
        verbose_name = u'Подписка на бюллетень'
        verbose_name_plural = u'Подписки на бюллетень'

    def __unicode__(self):
        return '%s' % self.email
    
 


class Bulletin(models.Model):
    date = models.DateField(u'Дата', unique = True)
    issue_number = models.IntegerField(u'Номер')
    issue_year_number = models.IntegerField(u'Номер', default= 216)
    date_created = models.DateTimeField(u'Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = u'Бюллетень'
        verbose_name_plural = u'Бюллетени'

    def __unicode__(self):
        return '%s' % self.date

    def save(self):
        super(Bulletin, self).save()
        informers = Informer.objects.filter(pubdate=self.date)
        for inf in informers:
            inf.published = True
            inf.save()

        announcements = Announcement.objects.filter(pubdate=self.date)
        for announce in announcements:
            announce.published = True
            announce.save()


class BulletinLog(models.Model):
    bulletin =   models.ForeignKey(Bulletin) 
    email = models.EmailField()  
    date = models.DateTimeField( auto_now_add=True)
    def __unicode__(self):
        return '%s %s' % (self.bulletin.date,  self.email )


class SubscriptionActivation(models.Model):
    email = models.EmailField(u'E-mail')
    activation_key = models.CharField(u'Код активации', max_length=40)
    company = models.CharField('Название компании', max_length=200)
    city = models.CharField('Город', max_length=200)
    company_type = models.CharField(u'Тип компании', max_length=200)
    phone = models.CharField(u'Телефон', max_length=200)
    contact_person = models.CharField(u'Контактное ФИО, должность', max_length=300)
    date = models.DateTimeField(u'Дата')

    class Meta:
        verbose_name = u'Активация подписки'
        verbose_name_plural = u'Активации подписки'
