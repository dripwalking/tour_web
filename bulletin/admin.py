# -*- coding: utf-8 -*-
from tourprom.bulletin.models import *
from django.contrib import admin
from django import forms

class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription

    def clean(self):
        if not self.instance.pk:
            if(Subscription.objects.filter(email=self.cleaned_data["email"]).count()>0):
                raise forms.ValidationError("Подписка на этот e-mail уже существует")
        return self.cleaned_data

class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm
    search_fields = ["email",]
    list_display = ('email', 'active',)
admin.site.register(Subscription, SubscriptionAdmin)

class BulletinAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bulletin, BulletinAdmin)

class BulletinLogAdmin(admin.ModelAdmin):
    search_fields = ["email" ]    
admin.site.register(BulletinLog, BulletinLogAdmin)