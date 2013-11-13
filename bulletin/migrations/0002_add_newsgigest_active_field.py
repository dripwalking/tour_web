# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Subscription.newsdigest_active'
        db.add_column('bulletin_subscription', 'newsdigest_active', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Subscription.newsdigest_active'
        db.delete_column('bulletin_subscription', 'newsdigest_active')


    models = {
        'bulletin.bulletin': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Bulletin'},
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_number': ('django.db.models.fields.IntegerField', [], {}),
            'issue_year_number': ('django.db.models.fields.IntegerField', [], {'default': '216'})
        },
        'bulletin.bulletinlog': {
            'Meta': {'object_name': 'BulletinLog'},
            'bulletin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bulletin.Bulletin']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bulletin.subscription': {
            'Meta': {'ordering': "('email',)", 'object_name': 'Subscription'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsdigest_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'bulletin.subscriptionactivation': {
            'Meta': {'object_name': 'SubscriptionActivation'},
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
