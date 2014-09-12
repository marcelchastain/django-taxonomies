# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for tgroup in orm['taxonomy.TaxonomyGroup'].objects.filter(display_name=None):
            tgroup.display_name = tgroup.name
            tgroup.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taxonomy.taxonomygroup': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'TaxonomyGroup'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'db_index': 'True'})
        },
        u'taxonomy.taxonomyitem': {
            'Meta': {'ordering': "['name']", 'object_name': 'TaxonomyItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxonomy.TaxonomyItem']", 'null': 'True', 'blank': 'True'}),
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
    symmetrical = True
