from time import sleep

from django.test import TestCase
from ws.tasks import add, dummy
from ws.models import Task, Node, Transition, Process, Workflow

class CeleryIntegrationTestCase(TestCase):
    fixtures = ['sample_workflow']

    def testGetCeleryTask(self):
        n1 = Node.objects.get(pk=1)
        self.assertEqual(n1.celery_task, add)

    def testNodeInfoRequired(self):
        n1 = Node.objects.get(pk=1) #"params": {"a": 2, "b": 2}
        n2 = Node.objects.get(pk=3) #"params": {"a": 2}
        self.assertFalse(n1.info_required)
        self.assertTrue(n2.info_required)
    
    def testTaskLaunch(self):
        task = Task.objects.get(pk=1)
        result = task.launch()
        result.get()
        task = Task.objects.get(pk=1) #reload, since task changed in database
        self.assertEqual('SUCCESS', task.state)
        self.assertEqual(u'2', task.result)

    def testAddTask(self):
        task_pk = 1
        result = add.delay(task_pk,8,8)
        self.assertEqual(result.get(), 16)
        self.assertTrue(result.successful())

    def testDummyTask(self):
        task_pk = 2
        result = dummy.delay(task_pk)
        self.assertEqual(result.get(), '')
        self.assertTrue(result.successful())

    def testStop(self):
        task = Task.objects.get(pk=3)
        result = task.launch()
        sleep(1)
        task.revoke()

    def testPriority(self):
        pass


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

    def test_condition(self):
        Node.objects.filter(name='Split').update(task_name='ws.tasks.add',
                params={u"a": 2, u"b": 4})
        Transition.objects.filter(parent__name='Split', child__name='One').update(
                condition='6')
        self.process.start()
        self.assertTasks('Split', 'One', 'Join')


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



