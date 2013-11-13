# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from tourprom.adsman.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AdsPostEntry'
        db.create_table('adsman_adspostentry', (
            ('id', orm['adsman.AdsPostEntry:id']),
            ('post', orm['adsman.AdsPostEntry:post']),
            ('key', orm['adsman.AdsPostEntry:key']),
            ('value', orm['adsman.AdsPostEntry:value']),
            ('position', orm['adsman.AdsPostEntry:position']),
        ))
        db.send_create_signal('adsman', ['AdsPostEntry'])
        
        # Adding model 'AdsPost'
        db.create_table('adsman_adspost', (
            ('id', orm['adsman.AdsPost:id']),
            ('page', orm['adsman.AdsPost:page']),
            ('author', orm['adsman.AdsPost:author']),
            ('publish_date', orm['adsman.AdsPost:publish_date']),
            ('price', orm['adsman.AdsPost:price']),
            ('currency', orm['adsman.AdsPost:currency']),
            ('active_date', orm['adsman.AdsPost:active_date']),
            ('price_rub', orm['adsman.AdsPost:price_rub']),
            ('location', orm['adsman.AdsPost:location']),
            ('is_free', orm['adsman.AdsPost:is_free']),
        ))
        db.send_create_signal('adsman', ['AdsPost'])
        
        # Adding model 'AdsPlacedControl'
        db.create_table('adsman_adsplacedcontrol', (
            ('id', orm['adsman.AdsPlacedControl:id']),
            ('control', orm['adsman.AdsPlacedControl:control']),
            ('page', orm['adsman.AdsPlacedControl:page']),
            ('position', orm['adsman.AdsPlacedControl:position']),
            ('hidden', orm['adsman.AdsPlacedControl:hidden']),
            ('mandatory', orm['adsman.AdsPlacedControl:mandatory']),
        ))
        db.send_create_signal('adsman', ['AdsPlacedControl'])
        
        # Adding model 'AdsControl'
        db.create_table('adsman_adscontrol', (
            ('id', orm['adsman.AdsControl:id']),
            ('name', orm['adsman.AdsControl:name']),
            ('caption', orm['adsman.AdsControl:caption']),
            ('type', orm['adsman.AdsControl:type']),
            ('delimiter', orm['adsman.AdsControl:delimiter']),
            ('value', orm['adsman.AdsControl:value']),
            ('hint', orm['adsman.AdsControl:hint']),
            ('constraint', orm['adsman.AdsControl:constraint']),
        ))
        db.send_create_signal('adsman', ['AdsControl'])
        
        # Adding model 'AdsPage'
        db.create_table('adsman_adspage', (
            ('id', orm['adsman.AdsPage:id']),
            ('parent', orm['adsman.AdsPage:parent']),
            ('title', orm['adsman.AdsPage:title']),
            ('template', orm['adsman.AdsPage:template']),
            ('uid', orm['adsman.AdsPage:uid']),
            ('allow_free', orm['adsman.AdsPage:allow_free']),
        ))
        db.send_create_signal('adsman', ['AdsPage'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AdsPostEntry'
        db.delete_table('adsman_adspostentry')
        
        # Deleting model 'AdsPost'
        db.delete_table('adsman_adspost')
        
        # Deleting model 'AdsPlacedControl'
        db.delete_table('adsman_adsplacedcontrol')
        
        # Deleting model 'AdsControl'
        db.delete_table('adsman_adscontrol')
        
        # Deleting model 'AdsPage'
        db.delete_table('adsman_adspage')
        
    
    
    models = {
        'accounts.companytype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'adsman.adscontrol': {
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'constraint': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'delimiter': ('django.db.models.fields.CharField', [], {'default': "','", 'max_length': '1'}),
            'hint': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000', 'null': 'True', 'blank': 'True'})
        },
        'adsman.adspage': {
            'allow_free': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'blank': 'True', 'null': 'True', 'to': "orm['adsman.AdsPage']"}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'adsman.adsplacedcontrol': {
            'control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adsman.AdsControl']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandatory': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'controls'", 'to': "orm['adsman.AdsPage']"}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        'adsman.adspost': {
            'active_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['advertisers.Advertiser']"}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_free': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adsman.AdsPage']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_rub': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'adsman.adspostentry': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['adsman.AdsPost']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'advertisers.advertiser': {
            'announcements_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'company_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['accounts.CompanyType']"}),
            'contact_person': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adv_country'", 'to': "orm['countries.Country']"}),
            'foundation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'informers_expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'informers_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'informers_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'messages_expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'messages_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'messages_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'other_phones': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Region']", 'null': 'True', 'blank': 'True'}),
            'tgb_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'web_site': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'countries.contentnode': {
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'modified_title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modify_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modify_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.IntegerField', [], {}),
            'rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'countries.continent': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'countries.country': {
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'content_tree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.ContentNode']"}),
            'continent': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['countries.Continent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'modified_title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modified_title_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modify_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modify_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'countries.federaldistrict': {
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Country']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'countries.region': {
            'content_tree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.ContentNode']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'federal_district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.FederalDistrict']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['adsman']
