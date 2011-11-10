from django.db import models
from django.dispatch import Signal, receiver
from django.utils.importlib import import_module

from celery.execute import send_task
import jsonfield

from ws.signals import notifier, r_conditions, r_states

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

    join = models.PositiveSmallIntegerField(choices=r_conditions.items())
    split = models.PositiveSmallIntegerField(choices=r_conditions.items())
    completed = {}

    task_name = models.CharField(max_length=256) #ws.tasks.add
    params = jsonfield.JSONField(null=True)
    info_required = models.BooleanField(editable=False)

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
    parent = models.ForeignKey(Node, related_name='child_transition_set')
    child = models.ForeignKey(Node, related_name='parent_transition_set')
    condition = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '{0} --[{1}]--> {2}'.format(
                self.parent.name, self.condition, self.child.name)


class Process(models.Model):
    workflow = models.ForeignKey(Workflow)

    def __unicode__(self):
        return '{0} [{1}]'.format(self.workflow.name, self.pk)
    
    def start(self):
        self.start_node(self.workflow.first)

    def start_node(self, node):
        task = Task(node=node, process=self)
        task.save()
        task.launch()


class Task(models.Model):
    node = models.ForeignKey(Node)
    process = models.ForeignKey(Process)

    result = models.CharField(max_length=100, blank=True)
    state = models.PositiveSmallIntegerField(
            choices=r_states.items(), default=2)

    def __unicode__(self):
        return '{0} [{1}] in {2}'.format(
                self.node, self.pk, self.process)

    def launch(self):
        # instead of calling task with send_task import task and use
        # apply_async; this way celery respects CELERY_ALWAYS_EAGER, so it
        # can be tested :-) This could change in future versions of celery.
        #result = send_task(self.task, args=(self.pk,), kwargs=params)
        result = self.node.celery_task.apply_async(
                args=(self.pk,), kwargs=self.node.params)
        return result

    def update(self, state, result=''):
        self.state = state
        self.result = result
        self.save()
        notifier.send(sender=self)
