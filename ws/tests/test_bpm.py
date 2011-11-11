from django.test import TestCase

from ws.models import Workflow, Node, Transition
from ws.models import Process, Task


class SplitJoinTest(TestCase):
    '''     
           |----One----|
    Split--|           |--Join
           |----Two----|
    '''
    fixtures = ['split_join_test']

    def assertTasks(self, *names):
        ok = Node.objects.filter(task_set__isnull=False)
        ok = ok.filter(name__in=names)
        self.assertEqual(ok.count(), len(names))

    def setUp(self):
        self.process = Process.objects.get(pk=1)

    def test_xor_to_xor(self):
        self.process.start()
        self.assertTasks('Split', 'One', 'Join')

    def test_and_to_and(self):
        Node.objects.filter(name='Split').update(split='AND')
        Node.objects.filter(name='Join').update(join='AND')
        self.process.start()
        self.assertTasks('Split', 'One', 'Two', 'Join')

    def test_and_to_xor(self):
        Node.objects.filter(name='Split').update(split='AND')
        self.process.start()
        self.assertTasks('Split', 'One', 'Join')

    def test_xor_to_and(self): #Impossible
        Node.objects.filter(name='Join').update(join='AND')
        self.process.start()
        self.assertTasks('Split', 'One')

class ConditionTest(TestCase):
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
        self.task_source.finish('SUCCESS', 'OK')
        self.assertTrue(self.destination in \
                self.task_source.childs_to_notify())


class LoopTest(TestCase):
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
        self.task_middle = self.task_first.finish('SUCCESS')[0]
        self.task_first = self.task_middle.finish('SUCCESS', 'Fail')[0]
        self.task_middle = self.task_first.finish('SUCCESS')[0]
        self.task_last = self.task_middle.finish('SUCCESS', 'OK')[0]



