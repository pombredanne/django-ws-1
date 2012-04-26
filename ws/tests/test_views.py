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
