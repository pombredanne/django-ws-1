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

from time import sleep

from django.test import TestCase
from django.contrib.auth.models import Group, User
from ws.tasks.dummy import add, dummy
from ws.models import Task, Node, Transition, Process, Workflow
from ws.celery import shortcuts


def update_task(task):
    return Task.objects.get(pk=task.pk)

def update_process(process):
    return Process.objects.get(pk=process.pk)


class ShortcutsTestCase(TestCase):
    fixtures = ['authorization']

    def setUp(self):
        self.bosses = Group.objects.get(name='bosses')
        self.boss = User.objects.get(username='boss')

    def test_assert_one_in_queryset(self):
        Workflow.objects.create(name='one')
        Workflow.objects.create(name='two')
        with self.assertRaises(Workflow.DoesNotExist):
            shortcuts.assert_one_in_queryset(Workflow.objects.none())
        with self.assertRaises(Workflow.MultipleObjectsReturned):
            shortcuts.assert_one_in_queryset(Workflow.objects.all())
        one = Workflow.objects.filter(name='one')
        self.assertTrue(shortcuts.assert_one_in_queryset(one))


    def test_update_task(self):
        workflow = Workflow.objects.create(name='one')
        process = Process.objects.create(workflow=workflow)
        node = Node.objects.create(name='one', workflow=workflow, 
                task_name='ws.tasks.dummy.dummy', role=self.bosses)
        task = Task.objects.create(node=node, process=process, user=self.boss)

        with self.assertRaises(ValueError):
            shortcuts.update_task()

        shortcuts.update_task(pk=task.pk, task_id='example', result='2')
        task = update_task(task)
        self.assertEquals(task.task_id, 'example')
        self.assertEquals(task.result, '2')

        shortcuts.update_task(task_id='example', result='3')
        task = update_task(task)
        self.assertEquals(task.result, '3')

    def test_update_process(self):
        workflow = Workflow.objects.create(name='one')
        node = Node.objects.create(name='one', workflow=workflow, 
                is_start=True, is_end=True, task_name='ws.tasks.dummy.dummy', 
                role=self.bosses)

        process = Process.objects.create(workflow=workflow)
        task = Task.objects.create(node=node, process=process, user=self.boss)

        subprocess = Process.objects.create(workflow=workflow, parent=task)
        subtask = Task.objects.create(node=node, process=subprocess, 
                user=self.boss)

        shortcuts.update_process(process.pk, state='STARTED')

        process = update_process(process)
        self.assertEquals(process.state, 'STARTED')

        shortcuts.update_task(subtask.pk, result='1')
        shortcuts.update_process(subprocess.pk, state='SUCCESS')

        task = update_task(task)
        self.assertEquals(task.state, 'SUCCESS')
        self.assertEquals(task.result, '1')

    def test_is_launchable(self):
        workflow = Workflow.objects.create(name='main')
        process = Process.objects.create(workflow=workflow)

        join_node = Node.objects.create(name='join', workflow=workflow,
                join='XOR', task_name='ws.tasks.dummy.dummy', role=self.bosses)
        node1 = Node.objects.create(name='one', workflow=workflow, 
                task_name='ws.tasks.dummy.dummy', role=self.bosses)
        node2 = Node.objects.create(name='two', workflow=workflow, 
                task_name='ws.tasks.dummy.dummy', role=self.bosses)

        # With no parent transitions, it must be always launchable
        self.assertTrue(shortcuts.is_launchable(join_node, process))

        task1 = Task.objects.create(node=node1, process=process,
                user=self.boss)
        task2 = Task.objects.create(node=node2, process=process,
                user=self.boss)

        Transition.objects.create(workflow=workflow, parent=node1, 
                child=join_node)
        Transition.objects.create(workflow=workflow, parent=node2,
                child=join_node)

        # With parent transitions but without fulfilled tasks, it's not launchable
        self.assertFalse(shortcuts.is_launchable(join_node, process))

        # With a XOR join and with one fulfilled task, it's launchable
        task1.state = 'SUCCESS'; task1.save()
        self.assertTrue(shortcuts.is_launchable(join_node, process))

        # With an AND join and with one fulfilled task, it's not launchable
        join_node.join = 'AND'; join_node.save()
        self.assertFalse(shortcuts.is_launchable(join_node, process))

        # With an AND join and with all tasks fulfilled, it's launchable
        task2.state = 'SUCCESS'; task2.save()
        self.assertTrue(shortcuts.is_launchable(join_node, process))

    def test_get_pending_childs(self):
        pass

    def test_get_revocable_parents(self):
        pass

    def test_get_alternative_way(self):
        pass



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
        Node.objects.filter(name='Split').update(task_name='ws.tasks.dummy.add',
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



