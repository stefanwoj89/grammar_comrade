# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table(u'politiburo_site', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'politiburo', ['Site'])

        # Adding model 'Author'
        db.create_table(u'politiburo_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'politiburo', ['Author'])

        # Adding model 'Article'
        db.create_table(u'politiburo_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['politiburo.Site'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['politiburo.Author'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'politiburo', ['Article'])

        # Adding model 'User'
        db.create_table(u'politiburo_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'politiburo', ['User'])

        # Adding model 'Review'
        db.create_table(u'politiburo_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['politiburo.Article'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['politiburo.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'politiburo', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Site'
        db.delete_table(u'politiburo_site')

        # Deleting model 'Author'
        db.delete_table(u'politiburo_author')

        # Deleting model 'Article'
        db.delete_table(u'politiburo_article')

        # Deleting model 'User'
        db.delete_table(u'politiburo_user')

        # Deleting model 'Review'
        db.delete_table(u'politiburo_review')


    models = {
        u'politiburo.article': {
            'Meta': {'object_name': 'Article'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['politiburo.Author']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['politiburo.Site']"})
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