from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json

class ViewsTestCase(TestCase):
    fixtures = ['sample_workflow']

    def setUp(self):
        self.client = Client()

    def testWorkflowListView(self):
        response = self.client.get('/ws/workflows.json')
        json_response = json.loads(response.content)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(len(json_response['rows']), json_response['total'])
        self.assertEqual(response.content, True)
