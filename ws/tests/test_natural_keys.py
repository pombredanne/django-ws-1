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
from django.utils import simplejson as json
from ws.models import Workflow, Node, Transition
from django.core.serializers import serialize, deserialize
from django.contrib.auth.models import Group

class NaturalKeysTestCase(TestCase):

    def testSerialize(self):
        role = Group(name='Computer')
        role.save()
        workflow = Workflow(name='test workflow')
        workflow.save()
        node1 = Node(name='step 1', workflow=workflow,
                     join='AND', split='AND', role=role,
                     task_name='ws.tasks.dummy.dummy')
        node1.save()
        node2 = Node(name='step 2', workflow=workflow,
                     join='AND', split='AND', role=role,
                     task_name='ws.tasks.dummy.dummy')
        node2.save()
        transition = Transition(workflow=workflow, parent=node1,
                                child=node2)
        transition.save()
        json_result = serialize('json', (workflow, node1, node2, transition),
                                  use_natural_keys=True)
        result = json.loads(json_result)

        self.assertEqual(len(result), 4)

        # Workflow field serialized as worfklow name
        self.assertEqual(result[1]['fields']['workflow'],
                         [workflow.name])

        # Node field serialized as node name and workflow name
        self.assertEqual(result[3]['fields']['parent'],
                         [node1.name, workflow.name])

        # Now deserialize the json result
        objects = deserialize('json', json_result)
        self.assertEqual(objects.next().object, workflow)
        self.assertEqual(objects.next().object, node1)
        self.assertEqual(objects.next().object, node2)
        self.assertEqual(objects.next().object, transition)
