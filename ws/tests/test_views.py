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

from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json
from ws.models import Workflow, Process

class ViewsTestCase(TestCase):
    fixtures = ['authorization', 'workflow_two_plus_two',
                'workflow_computer_trivial']

    def setUp(self):
        self.client = Client()

    def testWorkflowListView(self):
        # Anonymous users can't get workflow list
        response = self.client.get('/ws/workflows.json')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='worker', password='worker')
        response = self.client.get('/ws/workflows.json')
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['total'], 2)


        wf = Workflow(name='Guess the number')
        wf.save()
        response = self.client.get('/ws/workflows.json')
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['total'], 3)
        self.assertEqual(len(json_response['rows']), json_response['total'])
        workflow_names = [a['name'] for a in json_response['rows']]
        self.assertIn('Two plus two', workflow_names)
        self.assertIn('computer trivial', workflow_names)
        self.assertIn('Guess the number', workflow_names)

    def testProcessListView(self):
        # Anonymous users can't get process list
        response = self.client.get('/ws/processes.json')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='worker', password='worker')
        response = self.client.get('/ws/processes.json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['total'], 1)
        self.assertEqual(json_response['rows'][0]['name'],
                         'sample process')

    def testCreateProcess(self):
        url = '/ws/process/new.json'
        params = {'workflow': 1,
                  'autostart': 'off',
                  'name': 'test process'}
        # Anonymous users can't create processes
        response = self.client.post(url,  params)
        self.assertEqual(response.status_code, 302)

        # workers also, can't create processes
        self.client.login(username='worker', password='worker')
        response = self.client.post(url,  params)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='boss', password='boss')
        response = self.client.post(url,  params)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertIn('created', json_response['message'])
        self.assertNotIn('start', json_response['message'])

        #The process is created, with the correct workflow and no task has started
        process = Process.objects.get(name='test process')
        self.assertEqual(process.workflow_id, 1)
        self.assertEqual(process.task_set.count(), 0)

        #Now try with autostart
        params['autostart'] = 'on'
        params['name'] += ' with autostart'
        response = self.client.post(url,  params)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertIn('created', json_response['message'])
        self.assertIn('started', json_response['message'])

        #The process is created and one task started
        process = Process.objects.get(name='test process with autostart')
        self.assertEqual(process.task_set.count(), 1)

    def testStartProcess(self):
        url = '/ws/process/start.json'
        params = {'pk': 1}
        # Anonymous users can't start processes
        response = self.client.post(url,  params)
        self.assertEqual(response.status_code, 302)

        # workers also, can't start processes
        self.client.login(username='worker', password='worker')
        response = self.client.post(url,  params)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='boss', password='boss')
        response = self.client.post(url,  params)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual('Process started', json_response['message'])

    def testStopProcess(self):
        process = Process.objects.get(pk=1)
        process.start()

        url = '/ws/process/stop.json'
        params = {'pk': 1}
        # Anonymous users can't start processes
        response = self.client.post(url,  params)
        self.assertEqual(response.status_code, 302)

        # workers also, can't start processes
        self.client.login(username='worker', password='worker')
        response = self.client.post(url,  params)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='boss', password='boss')
        response = self.client.post(url,  params)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual('Process stopped', json_response['message'])

    def testTaskListView(self):
        #TODO: add django-guardian required info to fixtures
        # Anonymous users can't get task list
        response = self.client.get('/ws/tasks.json')
        self.assertEqual(response.status_code, 302)

        # Worker only sees his own tasks
        self.client.login(username='worker', password='worker')
        response = self.client.get('/ws/tasks.json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['total'], 1)

        # Boss sees all tasks
        self.client.login(username='boss', password='boss')
        response = self.client.get('/ws/tasks.json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['total'], 2)

    def testWorkflowGraphView(self):
        response = self.client.get('/ws/workflows/workflow_1.png')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def testTaskFormView(self):
        #Get the form for the "add 2 and something" task
        # The "add 2 and something" task has no info for b field
        from ws.tasks.dummy import AddForm
        response = self.client.get('/ws/task/4/form.json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 1)
        field = AddForm().fields['b']
        self.assertEqual(field.to_ext_dict('b'), json_response[0])

    def testTaskStartView(self):
        # Anonymous users can't start tasks
        response = self.client.get('/ws/task/1/start.json')
        self.assertEqual(response.status_code, 302)

        # Worker can't start task, as it's assigned to boss
        self.client.login(username='worker', password='worker')
        response = self.client.get('/ws/task/1/start.json')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='boss', password='boss')
        response = self.client.get('/ws/task/1/start.json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertIn('started successfully', json_response['message'].lower())

        #Trying again don't work, since it's already started
        response = self.client.get('/ws/task/1/start.json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], False)
        self.assertIn('already started', json_response['message'].lower())

    def testUserInfoView(self):
        self.client.login(username='worker', password='worker')
        response = self.client.get('/ws/user.json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['username'], 'worker')

        self.client.login(username='boss', password='boss')
        response = self.client.get('/ws/user.json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['username'], 'boss')
