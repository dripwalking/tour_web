# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FavoriteAdsPost'
        db.create_table('adsman_favoriteadspost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adsman.AdsPost'])),
        ))
        db.send_create_signal('adsman', ['FavoriteAdsPost'])


    def backwards(self, orm):
        
        # Deleting model 'FavoriteAdsPost'
        db.delete_table('adsman_favoriteadspost')


    models = {
        'accounts.companytype': {
            'Meta': {'object_name': 'CompanyType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_agency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'accounts.customuser': {
            'Meta': {'ordering': "('email',)", 'object_name': 'CustomUser', '_ormbases': ['auth.User']},
            'about_company': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'about_me': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'allow_profile_access': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'children': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company_phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.CompanyType']", 'null': 'True', 'blank': 'True'}),
            'company_website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'country'", 'null': 'True', 'to': "orm['countries.Country']"}),
            'eye_color': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'family_status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'favorite_countries': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'favorite_countries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['countries.Country']"}),
            'figure': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'friends_rel_+'", 'null': 'True', 'to': "orm['accounts.CustomUser']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'hair_color': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.Interest']", 'null': 'True', 'blank': 'True'}),
            'job_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.JobStatus']", 'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.Language']", 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Profession']", 'null': 'True', 'blank': 'True'}),
            'regime': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Region']", 'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'send_best_materials': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_news_digest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_quest_info': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_name': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'smoking': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'tourism_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.TourismType']", 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'visited_countries': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'visited_countries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['countries.Country']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wished_countries': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wished_countries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['countries.Country']"})
        },
        'accounts.interest': {
            'Meta': {'object_name': 'Interest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'accounts.jobstatus': {
            'Meta': {'object_name': 'JobStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'accounts.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'accounts.profession': {
            'Meta': {'object_name': 'Profession'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'adsman.adscontrol': {
            'Meta': {'object_name': 'AdsControl'},
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
            'Meta': {'object_name': 'AdsPage'},
            'allow_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['adsman.AdsPage']"}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'adsman.adsplacedcontrol': {
            'Meta': {'object_name': 'AdsPlacedControl'},
            'control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adsman.AdsControl']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandatory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'controls'", 'to': "orm['adsman.AdsPage']"}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        'adsman.adspost': {
            'Meta': {'object_name': 'AdsPost'},
            'active_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['advertisers.Advertiser']", 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adsman.AdsPage']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_rub': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.CustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'adsman.adspostentry': {
            'Meta': {'object_name': 'AdsPostEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['adsman.AdsPost']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'adsman.favoriteadspost': {
            'Meta': {'object_name': 'FavoriteAdsPost'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adsman.AdsPost']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'advertisers.advertiser': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Advertiser', '_ormbases': ['auth.User']},
            'activity_countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'country_advertisers'", 'blank': 'True', 'to': "orm['countries.Country']"}),
            'activity_tourism_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tourism_type_advertisers'", 'blank': 'True', 'to': "orm['countries.TourismType']"}),
            'announcements_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'company_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['accounts.CompanyType']"}),
            'contact_person': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'advertiser_country'", 'to': "orm['countries.Country']"}),
            'disable_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'foundation_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'informers_expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'informers_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'informers_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'interview_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'messages_expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'messages_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'messages_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'other_phones': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo_expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'photo_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'photo_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Region']", 'null': 'True', 'blank': 'True'}),
            'send_reminder': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'slug_old': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'tgb_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'video_expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'video_payment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'video_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'web_site': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'countries.contentnode': {
            'Meta': {'object_name': 'ContentNode'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modify_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modify_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.IntegerField', [], {}),
            'rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'countries.continent': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Continent'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'countries.country': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Country'},
            'attraction_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'capital_lat': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'capital_lon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'content_tree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.ContentNode']"}),
            'continent': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['countries.Continent']", 'symmetrical': 'False'}),
            'count_visits': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'direction': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'domen': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified_title_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modify_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modify_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'phonecode': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'popular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'population': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'restaurant_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seo_world': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'socket': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Rosette']", 'null': 'True', 'blank': 'True'}),
            'souvenir_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_datel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_predlog': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_rodit': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_tvorit': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_vinit': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'tour_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'visa': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'visa_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'voltage': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'weather_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'countries.federaldistrict': {
            'Meta': {'ordering': "('title',)", 'object_name': 'FederalDistrict'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Country']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'countries.region': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Region'},
            'attraction_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_tree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.ContentNode']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Country']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'federal_district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.FederalDistrict']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'restaurant_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'souvenir_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_datel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_predlog': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_rodit': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_tvorit': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_vinit': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'tour_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'weather_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'countries.rosette': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Rosette'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        'countries.rubric': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Rubric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'countries.tourismtype': {
            'Meta': {'ordering': "('title',)", 'object_name': 'TourismType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modify_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modify_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'popular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rubrics': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tourtype'", 'blank': 'True', 'to': "orm['countries.Rubric']"}),
            'show_in_touropedia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['adsman']
