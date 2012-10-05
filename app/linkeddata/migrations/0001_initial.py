# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RDFSchema'
        db.create_table('linkeddata_rdfschema', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('uri', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('linkeddata', ['RDFSchema'])

        # Adding model 'RDFProperty'
        db.create_table('linkeddata_rdfproperty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkeddata.RDFSchema'])),
            ('rdf_property', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('inverse', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('linkeddata', ['RDFProperty'])

        # Adding model 'RDFClass'
        db.create_table('linkeddata_rdfclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkeddata.RDFSchema'])),
            ('rdf_class', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('linkeddata', ['RDFClass'])


    def backwards(self, orm):
        # Deleting model 'RDFSchema'
        db.delete_table('linkeddata_rdfschema')

        # Deleting model 'RDFProperty'
        db.delete_table('linkeddata_rdfproperty')

        # Deleting model 'RDFClass'
        db.delete_table('linkeddata_rdfclass')


    models = {
        'linkeddata.rdfclass': {
            'Meta': {'object_name': 'RDFClass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rdf_class': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linkeddata.RDFSchema']"})
        },
        'linkeddata.rdfproperty': {
            'Meta': {'object_name': 'RDFProperty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inverse': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'rdf_property': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linkeddata.RDFSchema']"})
        },
        'linkeddata.rdfschema': {
            'Meta': {'object_name': 'RDFSchema'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['linkeddata']