# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Workflow'
        db.create_table('ws_workflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('params', self.gf('jsonfield.fields.JSONField')(default={}, null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=9)),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['ws.Node'])),
            ('end', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['ws.Node'])),
        ))
        db.send_create_signal('ws', ['Workflow'])

        # Adding model 'Node'
        db.create_table('ws_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ws.Workflow'])),
            ('join', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('split', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('params', self.gf('jsonfield.fields.JSONField')(default={}, null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=9)),
            ('task_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('info_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
        ))
        db.send_create_signal('ws', ['Node'])

        # Adding unique constraint on 'Node', fields ['name', 'workflow']
        db.create_unique('ws_node', ['name', 'workflow_id'])

        # Adding model 'Transition'
        db.create_table('ws_transition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ws.Workflow'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_transition_set', to=orm['ws.Node'])),
            ('child', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_transition_set', to=orm['ws.Node'])),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('ws', ['Transition'])

        # Adding unique constraint on 'Transition', fields ['parent', 'child']
        db.create_unique('ws_transition', ['parent_id', 'child_id'])

        # Adding model 'Process'
        db.create_table('ws_process', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ws.Workflow'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subprocess', null=True, to=orm['ws.Task'])),
            ('params', self.gf('jsonfield.fields.JSONField')(default={}, null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=8)),
        ))
        db.send_create_signal('ws', ['Process'])

        # Adding model 'Task'
        db.create_table('ws_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='task_set', to=orm['ws.Node'])),
            ('process', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ws.Process'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('params', self.gf('jsonfield.fields.JSONField')(default={}, null=True, blank=True)),
            ('progress', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=8)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('ws', ['Task'])


    def backwards(self, orm):
        # Removing unique constraint on 'Transition', fields ['parent', 'child']
        db.delete_unique('ws_transition', ['parent_id', 'child_id'])

        # Removing unique constraint on 'Node', fields ['name', 'workflow']
        db.delete_unique('ws_node', ['name', 'workflow_id'])

        # Deleting model 'Workflow'
        db.delete_table('ws_workflow')

        # Deleting model 'Node'
        db.delete_table('ws_node')

        # Deleting model 'Transition'
        db.delete_table('ws_transition')

        # Deleting model 'Process'
        db.delete_table('ws_process')

        # Deleting model 'Task'
        db.delete_table('ws_task')


    models = {
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
        'ws.node': {
            'Meta': {'unique_together': "[('name', 'workflow')]", 'object_name': 'Node'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'join': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'params': ('jsonfield.fields.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '9'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'split': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'task_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ws.Workflow']"})
        },
        'ws.process': {
            'Meta': {'object_name': 'Process'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'params': ('jsonfield.fields.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subprocess'", 'null': 'True', 'to': "orm['ws.Task']"}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '8'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ws.Workflow']"})
        },
        'ws.task': {
            'Meta': {'object_name': 'Task'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_set'", 'to': "orm['ws.Node']"}),
            'params': ('jsonfield.fields.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ws.Process']"}),
            'progress': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '8'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ws.transition': {
            'Meta': {'unique_together': "[('parent', 'child')]", 'object_name': 'Transition'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_transition_set'", 'to': "orm['ws.Node']"}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_transition_set'", 'to': "orm['ws.Node']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ws.Workflow']"})
        },
        'ws.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'end': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ws.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'params': ('jsonfield.fields.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '9'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['ws.Node']"})
        }
    }

    complete_apps = ['ws']