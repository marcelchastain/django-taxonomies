# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TaxonomyItem.parent'
        db.add_column(u'taxonomy_taxonomyitem', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taxonomy.TaxonomyItem'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TaxonomyItem.parent'
        db.delete_column(u'taxonomy_taxonomyitem', 'parent_id')


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