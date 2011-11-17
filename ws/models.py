from datetime import datetime
from django.db import models
from django.utils.importlib import import_module

from django.contrib.auth.models import Group, User

from jsonfield import JSONField

from ws.signals import notifier
from ws import STATES, CONDITIONS


class Workflow(models.Model):
    #FIXME: Here we have a problem: a circular foreignkey, from process to activity
    #and back. We can't do it if we don't make it somewhere possible to be null
    #because of the id assignement :-/
    name = models.CharField(max_length=100)
    start = models.ForeignKey('Node', related_name='+', null=True, blank=True)
    end = models.ForeignKey('Node', related_name='+', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=100)
    workflow = models.ForeignKey(Workflow)

    join = models.CharField(max_length=3, choices=CONDITIONS.items())
    split = models.CharField(max_length=3, choices=CONDITIONS.items())
    completed = {}

    task_name = models.CharField(max_length=256) #ws.tasks.add
    params = JSONField(null=True, blank=True)
    info_required = models.BooleanField(editable=False)

    role = models.ForeignKey(Group)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        params = self.params or '' #send some data to the form even when the task does not need it
        form = self.celery_task.form(params)
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
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
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

    result = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=8, 
            choices=STATES.items(), default='RECEIVED')

    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'{0} [{1}]'.format(self.node, self.pk)

    def launch(self, extra_params={}):
        # instead of calling task with send_task import task and use
        # apply_async; this way celery respects CELERY_ALWAYS_EAGER, so it
        # can be tested :-) This could change in future versions of celery.
        #result = send_task(self.task, args=(self.pk,), kwargs=params)
        params = extra_params.copy()
        params.update(self.node.params)
        form = self.node.celery_task.form(params)
        if form.is_valid():
            result = self.node.celery_task.apply_async(
                    args=(self.pk,), kwargs=self.node.params)
        else:
            result = None
        return result

    def update(self, state, result=''):
        self.state = state
        self.result = result
        self.save()
        notifier.send(sender=self)
