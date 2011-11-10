from django.db import models
from django.dispatch import Signal, receiver
from django.utils.importlib import import_module

from celery.execute import send_task
import jsonfield

task_state = Signal()
start_transition = Signal()

conditions = {'XOR': 0, 'AND': 1}
states = {'STARTED': 2, 'SUCCESS': 3, 'REVOKED': 4, 'FAILURE': 5}
conditions_choices = [(value, key) for key,value in conditions.items()]
states_choices = [(value, key) for key,value in states.items()]

#FIXME: we've a problem with XOR splits. After a XOR split is done,
#if the flow fails in some node, it must return to the split to instantiate
#the other side.

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

    join = models.PositiveSmallIntegerField(choices=conditions_choices)
    split = models.PositiveSmallIntegerField(choices=conditions_choices)
    completed = {}

    task_name = models.CharField(max_length=256, blank=True) #ws.tasks.add
    params = jsonfield.JSONField(null=True)
    info_required = models.BooleanField(editable=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.celery_task:
            form = self.celery_task.form(self.params)
            self.info_required = not form.is_valid()
        super(Node, self).save(*args, **kwargs)

    @property
    def celery_task(self):
        if not self.task_name:
            return None
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
            choices=states_choices, default=2)

    def __unicode__(self):
        return '{0} [{1}] in {2}'.format(
                self.node, self.pk, self.process)

    def launch(self):
        # instead of calling task with send_task import task and use
        # apply_async; this way celery respects CELERY_ALWAYS_EAGER, so it
        # can be tested :-) This could change in future versions of celery.
        #result = send_task(self.task, args=(self.pk,), kwargs=params)
        self.state = states['STARTED']
        self.save()
        result = self.node.celery_task.apply_async(
                args=(self.pk,),
                kwargs=self.node.params)
        return result

    def finish(self, state, result=''):
        if type(state) is str or type(state) is unicode:
            state = states[state]
        self.state = state
        self.result = result
        self.save()
        task_state.send_robust(sender=self, state=self.state)


class Notification(object):
    def notify_childs(self):
        transitions = self.node.child_transition_set.filter(
                condition__in=('', self.task.result))

        if self.task.node.split is conditions['XOR']:
            transitions = transitions[:1]

        for transition in transitions.iterator():
            start_transition.send_robust(
                    sender=transition, process=self.task.process)

    def notify_xor_parent(self):
        xor = None
        while not xor:
            parents = self.node.parent_transition_set.filter(
                    split=conditions['XOR'])
            transitions = Transition.objects.filter(parent__in=parents,
                    child__task_set__isnull=True)
            if transitions:
                xor = transitions[0]
        start_transition.send_robust(sender=xor, process=self.task.process)

    def __call__(self, sender, **kwargs):
        self.state = kwargs.pop('state')
        self.task = sender
        self.node = self.task.node

        if self.state is states['SUCCESS']:
            self.notify_childs()

        elif self.state in (states['FAILURE'], states['REVOKED']):
            self.notify_xor_parent()
task_state.connect(Notification(), weak=False)


@receiver(start_transition)
def start(sender, **kwargs):
    transition = sender
    process = kwargs.pop('process')

    if process not in transition.child.completed:
        transition.child.completed[process] = set()
    transition.child.completed[process].add(transition)

    completed = len(transition.child.completed[process])
    if (transition.child.join is conditions['XOR'] and completed >= 1) or\
            (transition.child.join is conditions['AND'] and completed is\
            transition.child.parent_transition_set.count()):
                process.start_node(transition.child)
