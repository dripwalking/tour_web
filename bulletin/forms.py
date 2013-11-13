# -*- coding: utf-8 -*-
from django import forms
from tourprom.bulletin.models import Subscription

class SubscribeForm(forms.Form):
    from tourprom.accounts.models import CompanyType

    company = forms.CharField(label=u'Название компании', max_length=200)
    city_choice = forms.ChoiceField(label=u'Город', widget=forms.RadioSelect(), choices=((u'Москва', u'Москва'), (u'Другой', u'Другой'),), initial=u'Москва')
    city = forms.CharField(label=u'Город', required=False)
    company_type = forms.ChoiceField(label=u'Тип компании', choices=CompanyType.objects.all().values_list('id', 'name'))
    email = forms.EmailField(label=u'E-mail')
    phone = forms.CharField(label=u'Телефон')
    contact_person = forms.CharField(label=u'Контактное ФИО, должность')

    def clean_email(self):
        check = Subscription.objects.filter(email=self.cleaned_data["email"], active=True)
        if len(check) > 0:
            raise forms.ValidationError("Подписка на данный e-mail адрес уже существует")

        return self.cleaned_data["email"]
