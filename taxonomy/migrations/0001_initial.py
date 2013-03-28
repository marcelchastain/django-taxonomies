# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaxonomyGroup'
        db.create_table(u'taxonomy_taxonomygroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
        ))
        db.send_create_signal(u'taxonomy', ['TaxonomyGroup'])

        # Adding model 'TaxonomyItem'
        db.create_table(u'taxonomy_taxonomyitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxonomy_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taxonomy.TaxonomyGroup'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
        ))
        db.send_create_signal(u'taxonomy', ['TaxonomyItem'])

        # Adding model 'TaxonomyMap'
        db.create_table(u'taxonomy_taxonomymap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxonomy_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taxonomy.TaxonomyItem'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'taxonomy', ['TaxonomyMap'])


    def backwards(self, orm):
        # Deleting model 'TaxonomyGroup'
        db.delete_table(u'taxonomy_taxonomygroup')

        # Deleting model 'TaxonomyItem'
        db.delete_table(u'taxonomy_taxonomyitem')

        # Deleting model 'TaxonomyMap'
        db.delete_table(u'taxonomy_taxonomymap')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taxonomy.taxonomygroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'TaxonomyGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'})
        },
        u'taxonomy.taxonomyitem': {
            'Meta': {'ordering': "['name']", 'object_name': 'TaxonomyItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'taxonomy_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxonomy.TaxonomyGroup']"})
        },
        u'taxonomy.taxonomymap': {
            'Meta': {'object_name': 'TaxonomyMap'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'taxonomy_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxonomy.TaxonomyItem']"})
        }
    }

    complete_apps = ['taxonomy']