from django.test import TestCase
from ws.models import Task, Node
from ws.tasks import add

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
