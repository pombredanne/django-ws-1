from django.utils import unittest

from .models import Workflow, Node, Transition
from .models import Process, Task, conditions, states

AND = conditions['AND']
XOR = conditions['XOR']


class WorkflowSetup(unittest.TestCase):
    def setUp(self):
        #Create the process and his instance
        self.workflow = Workflow.objects.create(name='workflow')
        self.process = Process.objects.create(workflow=self.workflow)

class JoinTest(WorkflowSetup):
    def setUp(self):
        super(JoinTest, self).setUp()

        #Create some activity and his instance
        self.one = Node.objects.create(
                workflow=self.workflow, join=XOR, split=XOR)
        self.task_one = Task.objects.create(
                node=self.one, process=self.process)

        #Create some other activity and his instance
        self.two = Node.objects.create(
                workflow=self.workflow, join=XOR, split=XOR)
        self.task_two = Task.objects.create(
                node=self.two, process=self.process)

        #Convergence poit, instance must be created depending on the situation
        self.joint = Node.objects.create(
                workflow=self.workflow, split=XOR, join=XOR)

        #Transition between instances and convergence point
        self.one_joint = Transition.objects.create(
                parent=self.one, child=self.joint)
        self.two_joint = Transition.objects.create(
                parent=self.two, child=self.joint)

    def test_xor(self):
        self.joint.join = XOR; self.joint.save()

        self.assertFalse(self.joint in self.process.valid_nodes())
        self.task_one.state=states['succeded']; self.task_one.save()
        self.assertTrue(self.joint in self.process.valid_nodes())

    def test_and(self):
        self.joint.join = AND; self.joint.save()

        self.assertFalse(self.joint in self.process.valid_nodes())
        self.task_one.state=states['succeded']; self.task_one.save()
        self.assertFalse(self.joint in self.process.valid_nodes())
        self.task_two.state=states['succeded']; self.task_two.save()
        self.assertTrue(self.joint in self.process.valid_nodes())


class JoinInstantiationTest(JoinTest):
    def test_xor(self):
        self.joint.join = XOR; self.joint.save()
        self.task_one.finish('succeded')
        self.assertTrue(Task.objects.filter(node=self.joint))

    def test_and(self):
        self.joint.join = AND; self.joint.save()
        self.assertFalse(Task.objects.filter(node=self.joint))
        self.task_one.finish('succeded')
        self.assertFalse(Task.objects.filter(node=self.joint))
        self.task_two.finish('succeded')
        self.assertTrue(Task.objects.filter(node=self.joint))


class SplitTest(WorkflowSetup):
    def setUp(self):
        super(SplitTest, self).setUp()

        #Create some activity
        self.one = Node.objects.create(
                workflow=self.workflow, join=XOR, split=XOR)

        #Create some other activity
        self.two = Node.objects.create(
                workflow=self.workflow, join=AND, split=XOR)

        #Separation poit and his instance
        self.separation = Node.objects.create(
                workflow=self.workflow, join=XOR, split=XOR)
        self.task_separation = Task.objects.create(
                node=self.separation, process=self.process,
                state=states['succeded'])

        #Transition between separation point and the others
        self.separation_one = Transition.objects.create(
                child=self.one, parent=self.separation)
        self.separation_two = Transition.objects.create(
                child=self.two, parent=self.separation)

    def test_xor(self):
        self.separation.split = XOR; self.separation.save()
        childs = self.task_separation.childs_to_notify()

        #self.one has XOR join, so it must be the best guess
        self.assertTrue(tuple(childs.iterator()) == (self.one,))

    def test_and(self):
        self.separation.split = AND; self.separation.save()
        childs = self.task_separation.childs_to_notify()

        self.assertTrue(tuple(childs.iterator()) == (self.one, self.two))


class SplitInstantiationTest(SplitTest):
    def test_xor(self):
        self.separation.split = XOR; self.separation.save()
        self.task_separation.finish('succeded')
        self.assertTrue(Task.objects.filter(node=self.one))
        self.assertFalse(Task.objects.filter(node=self.two))

    def test_and(self):
        self.separation.split = AND; self.separation.save()
        self.task_separation.finish('succeded')
        self.assertTrue(Task.objects.filter(node=self.one))
        self.assertTrue(Task.objects.filter(node=self.two))


class ConditionTest(WorkflowSetup):
    def setUp(self):
        super(ConditionTest, self).setUp()
        
        #Create the source activity and his instance
        self.source = Node.objects.create(
                workflow=self.workflow, join=XOR, split=XOR)
        self.task_source = Task.objects.create(
                node=self.source, process=self.process)

        #Create the destination activity
        self.destination = Node.objects.create(
                workflow=self.workflow, join=XOR, split=XOR)

        #Create the transition with a condition
        self.source_destination = Transition.objects.create(
                parent=self.source, child=self.destination,
                condition='OK')


    def test_condition(self):
        self.assertFalse(self.destination in \
                self.task_source.childs_to_notify())
        self.task_source.finish('succeded', 'OK')
        self.assertTrue(self.destination in \
                self.task_source.childs_to_notify())


class LoopTest(WorkflowSetup):
    '''
      _____________
     |           Fail
     v             |
    first-------->middle----OK----->last
    '''
    def setUp(self):
        super(LoopTest, self).setUp()

        #Create three nodes
        self.first = Node.objects.create(name='first',
                workflow=self.workflow, join=XOR, split=XOR)
        self.middle = Node.objects.create(name='middle',
                workflow=self.workflow, join=XOR, split=XOR)
        self.last = Node.objects.create(name='last',
                workflow=self.workflow, join=XOR, split=XOR)

        #Create transitions, one of them a loop:

        self.first_middle = Transition.objects.create(
                parent=self.first, child=self.middle)
        self.middle_last = Transition.objects.create(
                parent=self.middle, child=self.last, condition='OK')
        self.middle_first = Transition.objects.create(
                parent=self.middle, child=self.first, condition='Fail')

        self.task_first = Task.objects.create(
                node=self.first, process=self.process)

    def test_loop(self):
        self.task_middle = self.task_first.finish('succeded')[0]
        self.task_first = self.task_middle.finish('succeded', 'Fail')[0]
        self.task_middle = self.task_first.finish('succeded')[0]
        self.task_last = self.task_middle.finish('succeded', 'OK')[0]



