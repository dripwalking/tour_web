# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from tourprom.adsman.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'AdsPage.visible'
        db.add_column('adsman_adspage', 'visible', orm['adsman.adspage:visible'])
        
        # Adding field 'AdsPost.user'
        db.add_column('adsman_adspost', 'user', orm['adsman.adspost:user'])
        
        # Changing field 'AdsPost.author'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['advertisers.Advertiser'], null=True, blank=True))
        db.alter_column('adsman_adspost', 'author_id', orm['adsman.adspost:author'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'AdsPage.visible'
        db.delete_column('adsman_adspage', 'visible')
        
        # Deleting field 'AdsPost.user'
        db.delete_column('adsman_adspost', 'user_id')
        
        # Changing field 'AdsPost.author'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['advertisers.Advertiser']))
        db.alter_column('adsman_adspost', 'author_id', orm['adsman.adspost:author'])
        
    
    
    models = {
        'accounts.companytype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'accounts.customuser': {
            'about_company': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'about_me': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'children': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.CompanyType']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'country'", 'to': "orm['countries.Country']"}),
            'eye_color': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'family_status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'favorite_countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'figure': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.CustomUser']", 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hair_color': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Interest']", 'null': 'True', 'blank': 'True'}),
            'job_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.JobStatus']", 'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Language']", 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Profession']", 'null': 'True', 'blank': 'True'}),
            'regime': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Region']", 'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'show_name': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'smoking': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'tourism_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['countries.TourismType']", 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'visited_countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wished_countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'})
        },
        'accounts.interest': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'accounts.jobstatus': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'accounts.language': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'accounts.profession': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'uid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
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
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['advertisers.Advertiser']", 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_free': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adsman.AdsPage']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_rub': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.CustomUser']", 'null': 'True', 'blank': 'True'})
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
        },
        'countries.tourismtype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'modified_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modify_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modify_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'show_in_touropedia': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['adsman']
