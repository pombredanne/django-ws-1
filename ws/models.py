from __future__ import absolute_import, division

from datetime import datetime
from time import sleep

from django.db import models
from django.db.models.query import QuerySet
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, User

from jsonfield import JSONField
from celery.task.control import revoke
from guardian.shortcuts import assign, remove_perm, get_users_with_perms

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

    @property
    def state(self):
        start = self.task_set.get(node=self.workflow.start)
        ending = self.task_set.get(node=self.workflow.end)
        if start.state is 'PENDING':
            return 'PENDING'
        elif ending.state is 'PENDING' and self.task_set.filter(
                state__in=('SENT', 'RECEIVED', 'STARTED', 'RETRY')):
            return 'STARTED'
        elif ending.state is 'SUCCESS':
            return 'SUCCESS'
        return 'FAILURE'

    @property
    def percentage(self):
        percentages = self.task_set.values_list('percentage', flat=True)
        return sum(percentages) / len(percentages)

    @property
    def result(self):
        try:
            self.task_set.get(node=self.workflow.end).result
        except Task.DoesNotExist:
            return ''

    def start(self):
        self.start_node(self.workflow.start)
        self.start_date = datetime.now()
        self.save()

    def stop(self):
        for task in self.task_set.exclude(
                state__in=('SUCCESS', 'FAILURE', 'REVOKED')):
            revoke(task.task_id, terminate=True)

    def start_node(self, node):
        user = node.role.user_set.all()[0] #TODO: select valid user
        task = Task(node=node, process=self, user=user)
        task.save()
        task.assign(user)
        if not node.info_required:
            task.launch()


class TaskQuerySet(QuerySet):
    supports_locking = hasattr(QuerySet, 'select_for_update')

    def select_for_update(self, *args, **kwargs):
        if not self.supports_locking:
            return self.all()
        return super(TaskQuerySet, self).select_for_update(*args, **kwargs)

    def update(self, *args, **kwargs):
        q = super(TaskQuerySet, self).update(*args, **kwargs)
        if not self.supports_locking:
            sleep(1)
        return q


class TaskManager(models.Manager):
    def select_for_update(self, *args, **kwargs):
        return TaskQuerySet(self.model, using=self._db).select_for_update(
                *args, **kwargs)
            

class Task(models.Model):
    objects = TaskManager()

    node = models.ForeignKey(Node, related_name='task_set')
    process = models.ForeignKey(Process)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    priority = models.PositiveSmallIntegerField(null=True)
    task_id = models.CharField(max_length=36, blank=True)

    percentage = models.PositiveSmallIntegerField(default=0)
    result = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=8, 
            choices=STATES.items(), default='PENDING')

    user = models.ForeignKey(User)

    class Meta:
        permissions = (
                ('execute_task', 'Can execute task'),
                ('view_task', 'Can view task'),
                )

    def __unicode__(self):
        return u'{0} [{1}]'.format(self.node, self.pk)

    def assign(self, user):
        for user, perms in get_users_with_perms(self, attach_perms=True):
            [ remove_perm(perm, user, self) for perm in perms ]
        assign('execute_task', user, self)
        assign('view_task', user, self)

    def launch(self, extra_params={}):
        params = self.node.params.copy()
        params.update(extra_params)
        form = self.node.celery_task.form(params)
        if form.is_valid():
            result = self.apply_async(form.clean())
        else:
            result = None
        return result

    def revoke(self):
        revoke(self.task_id, terminate=True)

    @property
    def average_priority(self):
        task = self.priority or self.node.priority
        process = self.process.priority or self.process.workflow.priority
        return (task + process) // 2

    def apply_async(self, kwargs):
        kwargs['workflow_task'] = self.pk
        return self.node.celery_task.apply_async(
                kwargs=kwargs,
                priority=self.average_priority,
                )
