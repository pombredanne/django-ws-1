from __future__ import absolute_import

from datetime import datetime
from django.db import models
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, User

from jsonfield import JSONField
from celery.task.control import revoke
from guardian.models import GroupObjectPermission, UserObjectPermission

from ws.signals import notifier
from ws import STATES, CONDITIONS


class Workflow(models.Model):
    #FIXME: Here we have a problem: a circular foreignkey, from process to activity
    #and back. We can't do it if we don't make it somewhere possible to be null
    #because of the id assignement :-/
    name = models.CharField(max_length=100)

    priority = models.PositiveSmallIntegerField(default=9)
    start = models.ForeignKey('Node', related_name='+', null=True, blank=True)
    end = models.ForeignKey('Node', related_name='+', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=100)
    workflow = models.ForeignKey(Workflow)

    join = models.CharField(max_length=3, choices=CONDITIONS.items())
    split = models.CharField(max_length=3, choices=CONDITIONS.items())

    priority = models.PositiveSmallIntegerField(default=9)
    task_name = models.CharField(max_length=256) #ws.tasks.add
    params = JSONField(null=True, blank=True, default={})
    info_required = models.BooleanField(editable=False)

    role = models.ForeignKey(Group)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        form = self.celery_task.form(self.params)
        self.info_required = not form.is_valid()
        super(Node, self).save(*args, **kwargs)

    @property
    def celery_task(self):
        module, _, task = self.task_name.rpartition('.')
        module = import_module(module)
        return getattr(module, task)


class Transition(models.Model):
    class Meta:
        unique_together = [('parent', 'child')]
    workflow = models.ForeignKey(Workflow)
    parent = models.ForeignKey(Node, related_name='child_transition_set')
    child = models.ForeignKey(Node, related_name='parent_transition_set')
    condition = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        condition = self.condition
        if condition:
            condition = '[' + condition + ']'
        return u'{0} --{1}--> {2}'.format(
                self.parent.name, condition, self.child.name)


class Process(models.Model):
    workflow = models.ForeignKey(Workflow)
    name = models.CharField(max_length=100, blank=True)

    priority = models.PositiveSmallIntegerField(null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        permissions = (
                ('execute_process', 'Can execute process'),
                )

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return u'{0} [{1}]'.format(self.workflow.name, self.pk)

    def start(self):
        self.start_node(self.workflow.start)
        self.start_date = datetime.now()
        self.save()

    def start_node(self, node):
        user = node.role.user_set.all()[0] #TODO: select valid user
        task = Task(node=node, process=self, user=user)
        task.save()
        if not node.info_required:
            task.launch()

class Task(models.Model):
    node = models.ForeignKey(Node, related_name='task_set')
    process = models.ForeignKey(Process)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    priority = models.PositiveSmallIntegerField(null=True)
    task_id = models.CharField(max_length=36, blank=True)
    result = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=8, 
            choices=STATES.items(), default='RECEIVED')

    user = models.ForeignKey(User)

    class Meta:
        permissions = (
                ('execute_task', 'Can execute task'),
                ('view_task', 'Can view task'),
                )

    def __unicode__(self):
        return u'{0} [{1}]'.format(self.node, self.pk)

    def launch(self, extra_params={}):
        params = self.node.params.copy()
        params.update(extra_params)
        form = self.node.celery_task.form(params)
        if form.is_valid():
            result = self.apply_async(form.clean())
            self.task_id = result.task_id
            self.save()
        else:
            result = None
        return result

    def revoke(self):
        revoke(self.task_id, terminate=True)

    def update(self, state, result=''):
        self.state = state
        self.result = result
        self.save()
        notifier.send(sender=self)

    def get_priority(self):
        task = self.priority or self.node.priority
        process = self.process.priority or self.process.workflow.priority
        return (task + process) / 2

    def apply_async(self, kwargs):
        return self.node.celery_task.apply_async(
                args=(self.pk,), 
                kwargs=kwargs,
                priority=self.get_priority(),
                )

    def save(self, *args, **kwargs):
        contenttype = ContentType.objects.get_for_model(Task)
        group = GroupObjectPermission.objects.get(content_type=contenttype, 
                object_pk=self.pk, permission__codename='execute_task')
        group.group = self.node.role
        group.save()

        user = UserObjectPermission.objects.get(content_type=contenttype,
                object_pk=self.pk, permission__codename='view_task')
        user.user = self.user
        user.save()

        super(Task, self).save(*args, **kwargs)
