from django.dispatch import Signal, receiver

notifier = Signal()
starter = Signal()

class Notifier:
    def __init__(self, sender, **kwargs):
        self.task = sender
        self.node = self.task.node

        func = self.task.state.lower()
        getattr(self, func)()

    def received(self):
        pass

    def retry(self):
        pass

    def revoked(self):
        self.failure()

    def success(self):
        transitions = self.node.child_transition_set.filter(
                condition__in=('', self.task.result))

        if self.task.node.split == 'XOR':
            transitions = transitions[:1]

        for transition in transitions.iterator():
            starter.send(sender=transition.child, process=self.task.process)

    def started(self):
        #FIXME: we must stop the paralel processes if this is a XOR
        pass

    def failure(self):
        #FIXME/FIXED?(TESTS): we've a problem with XOR splits. 
        #After a XOR split is done, if the flow fails in some 
        #node, it must return to the split to instantiate
        #the other side.
        xor = None
        while not xor:
            parents = self.node.parent_transition_set.filter(split='XOR')
            transitions = Transition.objects.filter(parent__in=parents,
                    child__task_set__isnull=True)
            if transitions:
                xor = transitions[0]
        starter.send(sender=xor.child, process=self.task.process)

    def pending(self):
        pass
notifier.connect(Notifier)


class Starter:
    def __init__(self, sender, process, **kwargs):
        node = sender

        completed = 0
        tasks = process.task_set.filter(state='SUCCESS')
        for transition in node.parent_transition_set.iterator():
            if tasks.filter(node=transition.parent,  result__in=(
                '', transition.condition)):
                completed += 1

                if node.join == 'XOR':
                    return process.start_node(node)

        if node.join == 'AND' and\
                completed == node.parent_transition_set.count():
                    return process.start_node(transition.child)
starter.connect(Starter)
