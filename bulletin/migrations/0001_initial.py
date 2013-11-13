# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from tourprom.bulletin.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Bulletin'
        db.create_table('bulletin_bulletin', (
            ('id', orm['bulletin.Bulletin:id']),
            ('date', orm['bulletin.Bulletin:date']),
            ('issue_number', orm['bulletin.Bulletin:issue_number']),
            ('issue_year_number', orm['bulletin.Bulletin:issue_year_number']),
            ('date_created', orm['bulletin.Bulletin:date_created']),
        ))
        db.send_create_signal('bulletin', ['Bulletin'])
        
        # Adding model 'BulletinLog'
        db.create_table('bulletin_bulletinlog', (
            ('id', orm['bulletin.BulletinLog:id']),
            ('bulletin', orm['bulletin.BulletinLog:bulletin']),
            ('email', orm['bulletin.BulletinLog:email']),
            ('date', orm['bulletin.BulletinLog:date']),
        ))
        db.send_create_signal('bulletin', ['BulletinLog'])
        
        # Adding model 'SubscriptionActivation'
        db.create_table('bulletin_subscriptionactivation', (
            ('id', orm['bulletin.SubscriptionActivation:id']),
            ('email', orm['bulletin.SubscriptionActivation:email']),
            ('activation_key', orm['bulletin.SubscriptionActivation:activation_key']),
            ('company', orm['bulletin.SubscriptionActivation:company']),
            ('city', orm['bulletin.SubscriptionActivation:city']),
            ('company_type', orm['bulletin.SubscriptionActivation:company_type']),
            ('phone', orm['bulletin.SubscriptionActivation:phone']),
            ('contact_person', orm['bulletin.SubscriptionActivation:contact_person']),
            ('date', orm['bulletin.SubscriptionActivation:date']),
        ))
        db.send_create_signal('bulletin', ['SubscriptionActivation'])
        
        # Adding model 'Subscription'
        db.create_table('bulletin_subscription', (
            ('id', orm['bulletin.Subscription:id']),
            ('email', orm['bulletin.Subscription:email']),
            ('active', orm['bulletin.Subscription:active']),
        ))
        db.send_create_signal('bulletin', ['Subscription'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Bulletin'
        db.delete_table('bulletin_bulletin')
        
        # Deleting model 'BulletinLog'
        db.delete_table('bulletin_bulletinlog')
        
        # Deleting model 'SubscriptionActivation'
        db.delete_table('bulletin_subscriptionactivation')
        
        # Deleting model 'Subscription'
        db.delete_table('bulletin_subscription')
        
    
    
    models = {
        'bulletin.bulletin': {
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_number': ('django.db.models.fields.IntegerField', [], {}),
            'issue_year_number': ('django.db.models.fields.IntegerField', [], {'default': '216'})
        },
        'bulletin.bulletinlog': {
            'bulletin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bulletin.Bulletin']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bulletin.subscription': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bulletin.subscriptionactivation': {
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'company_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['bulletin']
