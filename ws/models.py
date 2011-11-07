from django.db import models

from . import get_operations


conditions = {'XOR': 0, 'AND': 1}
states = {'disabled': 0, 'enabled': 1, 'started': 2,
        'succeded': 3, 'cancelled': 4, 'failed': 5}

#FIXME: we've a problem with XOR splits. After a XOR split is done,
#if the flow fails in some node, it must return to the split to instantiate
#the other side.

class Workflow(models.Model):
    #FIXME: Here we have a problem: a circular foreignkey, from process to activity
    #and back. We can't do it if we don't make it somewhere possible to be null
    #because of the id assignement :-/
    name = models.CharField(max_length=100)
    start = models.ForeignKey('Node', related_name='+', null=True)
    end = models.ForeignKey('Node', related_name='+', null=True)

    def __unicode__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=100)
    workflow = models.ForeignKey(Workflow)

    join = models.PositiveSmallIntegerField(choices=conditions.items())
    split = models.PositiveSmallIntegerField(choices=conditions.items())

    operation = models.CharField(choices=get_operations(), max_length=200)
    arguments = models.TextField(editable=False)

    def __unicode__(self):
        return self.name


class Transition(models.Model):
    parent = models.ForeignKey(Node, related_name='child_transition_set')
    child = models.ForeignKey(Node, related_name='parent_transition_set')
    condition = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '{0} --[{1}]--> {2}'.format(
                self.parent.name, self.condition, self.child.name)


class Process(models.Model):
    workflow = models.ForeignKey(Workflow)

    def latest_tasks(self):
        tasks = Task.objects.none()
        for node in Node.objects.filter(workflow=self.workflow):
            tasks |= Task.objects.filter(process=self, 
                    node=node).order_by('-pk')[:1]
        return tasks

    def valid_transitions(self):
        valid = Transition.objects.none()
        for task in self.task_set.filter(state=states['succeded']):
            valid |= Transition.objects.filter(parent=task.node,
                    condition__in=(task.result, ''))
        return valid

    def valid_nodes(self):
        transitions = self.valid_transitions()
        nodes = Node.objects.filter(workflow=self.workflow)
        valid = nodes.filter(join=conditions['XOR'],
                parent_transition_set__in=transitions)

        for node in nodes.filter(join=conditions['AND']).iterator():
            if node.parent_transition_set.count() is \
                    transitions.filter(child=node).count():
                        valid |= nodes.filter(pk=node.pk)
        return valid

    def __unicode__(self):
        return '{0} [{1}]'.format(self.workflow.name, self.pk)
    

class Task(models.Model):
    node = models.ForeignKey(Node)
    process = models.ForeignKey(Process)

    result = models.CharField(max_length=100, blank=True)
    state = models.PositiveSmallIntegerField(
            choices=states.items(), default=0)

    def __unicode__(self):
        return '{0} [{1}] in {2}'.format(
                self.node, self.pk, self.process)

    def valid_transitions(self):
        return self.process.valid_transitions().filter(
                parent=self.node, condition__in=(self.result, ''))

    def valid_nodes(self):
        return self.process.valid_nodes().filter(
                parent_transition_set__in=self.valid_transitions(),
                parent_transition_set__parent=self.node)

    def childs_to_notify(self):
        childs = self.valid_nodes()
        if self.node.split is conditions['XOR']:
            #TODO: insert XOR decition logic here
            childs = childs[:1]
        return childs

    def finish(self, state, result=''):
        if type(state) is str or type(state) is unicode:
            state = states[state]
        self.state = state
        self.result = result
        self.save()
        tasks = Task.objects.none()
        for node in self.childs_to_notify():
            task = Task(
                node=node, 
                process=self.process,
                state=states['enabled'])
            task.save()
            tasks |= Task.objects.filter(pk=task.pk)
        return tasks
