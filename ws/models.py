###############################################################################
#  Copyright 2011,2012 GISA Elkartea.                                         #
#                                                                             #
#  This file is part of django-ws.                                            #
#                                                                             #
#  django-ws is free software: you can redistribute it and/or modify it       #
#  under the terms of the GNU Affero General Public License as published      #
#  by the Free Software Foundation, either version 3 of the License, or       #
#  (at your option) any later version.                                        #
#                                                                             #
#  django-ws is distributed in the hope that it will be useful, but WITHOUT   #
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or      #
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public       #
#  License for more details.                                                  #
#                                                                             #
#  You should have received a copy of the GNU Affero General Public License   #
#  along with django-ws. If not, see <http://www.gnu.org/licenses/>.          #
###############################################################################

from __future__ import absolute_import
from inspect import getargspec

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, User

from jsonfield import JSONField
from celery.execute import send_task
from guardian.shortcuts import assign, remove_perm, get_users_with_perms

from ws import STATES, CONDITIONS
from ws.fields import CeleryTaskField
from ws.celery import shortcuts


# TODO: django trunk includes getters and setters.
# Get basic logic down from tasks to models.

class WorkflowManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Workflow(models.Model):
    name = models.CharField(max_length=100, unique=True)

    params = JSONField(null=True, blank=True, default={})
    priority = models.PositiveSmallIntegerField(default=9)

    objects = WorkflowManager()

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name, )

    @property
    def start_nodes(self):
        return self.node_set.filter(is_start=True)

    @property
    def end_nodes(self):
        return self.node_set.filter(is_end=True)


class NodeManager(models.Manager):
    def get_by_natural_key(self, name, workflow):
        return self.get(name=name, workflow__name=workflow)


class Node(models.Model):
    class Meta:
        unique_together = [('name', 'workflow')]

    name = models.CharField(max_length=100)
    workflow = models.ForeignKey(Workflow)

    join = models.CharField(max_length=3, choices=CONDITIONS.items())
    split = models.CharField(max_length=3, choices=CONDITIONS.items())

    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)

    params = JSONField(null=True, blank=True, default={})
    priority = models.PositiveSmallIntegerField(default=9)
    celery_task = CeleryTaskField(max_length=256)
    info_required = models.BooleanField(editable=False)

    role = models.ForeignKey(Group)

    objects = NodeManager()

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name, self.workflow.name)
    natural_key.dependencies = ['ws.Workflow']

    def save(self, *args, **kwargs):
        form = self.celery_task.form(self.params)
        self.info_required = not form.is_valid()
        super(Node, self).save(*args, **kwargs)

    def is_launchable(self, process):
        return shortcuts.is_launchable(self, process)


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
    class Meta:
        permissions = (
                ('execute_process', 'Can execute process'),
                )

    workflow = models.ForeignKey(Workflow)
    name = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey('Task', null=True, blank=True,
            related_name='subprocess')

    params = JSONField(null=True, blank=True, default={})
    priority = models.PositiveSmallIntegerField(null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=8,
            choices=STATES.items(), default='PENDING')


    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return u'{0} [{1}]'.format(self.workflow.name, self.pk)

    @property
    def progress(self):
        progresses = self.task_set.values_list('progress', flat=True)
        return sum(progresses) / len(progresses)

    @property
    def results(self):
        return self.task_set.get(node__is_end=True).values_list('result',
                flat=True)

    def start(self):
        assert self.state == 'PENDING', 'Process already started'
        assert not self.workflow.start_nodes.empty(), 'No starting nodes'
        for node in self.workflow.start_nodes.iterator():
            self.launch_node(node)

    def stop(self):
        assert self.state == 'STARTED', 'Process not running'
        for task in self.task_set.exclude(state__in=(
            'SUCCESS', 'FAILURE', 'REVOKED')):
                task.revoke()

    def launch_node(self, node):
        # TODO: select valid user
        user = node.role.user_set.all()[0]
        task = Task.objects.create(node=node, process=self, user=user)
        task.assign(user)
        if not node.info_required:
            task.launch()
        return task

    def update(self, **kwargs):
        return shortcuts.update_process(self.pk, **kwargs)


class Task(models.Model):
    node = models.ForeignKey(Node, related_name='task_set')
    process = models.ForeignKey(Process)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    priority = models.PositiveSmallIntegerField(null=True)
    task_id = models.CharField(max_length=36, blank=True)
    params = JSONField(null=True, blank=True, default={})

    progress = models.PositiveSmallIntegerField(default=0)
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
            [remove_perm(perm, user, self) for perm in perms]
        assign('execute_task', user, self)
        assign('view_task', user, self)

    def _get_params(self, extra_params={}):
        # Priority order: extra_params, task, node, process, workflow
        params = {}
        for param in (self.node.workflow.params, self.process.params,
                self.node.params, self.params, extra_params):
            params.update(param)
        return params

    def _filter_params(self, params):
        # If there's a related form, cleanup params with it
        if hasattr(self.node.celery_task, 'form'):
            form = self.node.celery_task.form(params)
            if form.is_valid():
                kwargs = form.clean()
            else:
                raise forms.ValidationError

        # Else, inspect the tasks call method
        else:
            args = getargspec(self.node.celery_task.call)
            
            # If it accepts no *args nor **kwargs, pass only the accepted args
            if (args.varargs, args.keywords) == (None, None):
                kwargs = { arg: params[arg] for arg in args }
            # Else, pass them all
            else:
                kwargs = params
        return kwargs

    def launch(self, extra_params={}):
        params = self._get_params(extra_params)
        kwargs = self._filter_params(params)
        return self.apply_async(kwargs)

    def revoke(self):
        send_task('ws.celery.bpm.task_revoked', kwargs={
            'task_id': self.task_id})

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

    def update(self, **kwargs):
        return shortcuts.update_task(pk=self.pk, **kwargs)

    def get_pending_childs(self):
        return shortcuts.get_pending_childs(self)

    def get_revocable_parents(self):
        return shortcuts.get_revocable_parents(self)

    def get_alternative_way(self):
        return shortcuts.get_alternative_way(self)
