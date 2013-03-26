# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Site.name'
        db.add_column(u'politiburo_site', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Site.name'
        db.delete_column(u'politiburo_site', 'name')


    models = {
        u'politiburo.article': {
            'Meta': {'object_name': 'Article'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['politiburo.Author']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'grammar_error_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['politiburo.Site']"}),
            'spell_error_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'style_error_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'word_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'politiburo.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'politiburo.review': {
            'Meta': {'object_name': 'Review'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['politiburo.Article']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['politiburo.User']"})
        },
        u'politiburo.site': {
            'Meta': {'object_name': 'Site'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'politiburo.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['politiburo']