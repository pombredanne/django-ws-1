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
from ws import forms
from ws.models import Node
from ws.tasks.dummy import add, dummy

class FormsTestCase(TestCase):

    def testField(self):
        testfield = forms.CharField(
                required=False,
                label='Test field',
                initial=2,
                help_text='Test help text')
        ext_dict = testfield.to_ext_dict('testfield')
        self.assertIn('name', ext_dict)
        self.assertIn('xtype', ext_dict)
        self.assertIn('fieldLabel', ext_dict)
        self.assertIn('value', ext_dict)
        #TODO: self.assertTrue('required' in ext_dict)
        #TODO: self.assertTrue('help_text' in ext_dict)
        self.assertEqual(ext_dict['name'], 'testfield')
        self.assertEqual(ext_dict['xtype'], 'textfield')
        self.assertEqual(ext_dict['fieldLabel'], 'Test field')
        #TODO: self.assertEqual(ext_dict['required'], False)
        #TODO: self.assertEqual(ext_dict['help_text'], 'Test help text')

    def testIntegerField(self):
        testfield = forms.IntegerField(
                max_value=999,
                min_value=0)
        ext_dict = testfield.to_ext_dict('testfield')
        self.assertIn('max_value', ext_dict)
        self.assertIn('min_value', ext_dict)
        self.assertEqual(ext_dict['max_value'], 999)
        self.assertEqual(ext_dict['min_value'], 0)

    def testCharField(self):
        testfield = forms.CharField(
                max_length=5,
                min_length=1)
        ext_dict = testfield.to_ext_dict('testfield')
        self.assertIn('maxLength', ext_dict)
        self.assertIn('minLength', ext_dict)
        self.assertEqual(ext_dict['maxLength'], 5)
        self.assertEqual(ext_dict['minLength'], 1)

    def testBooleanField(self):
        field = forms.BooleanField(initial=1)
        ext_dict = field.to_ext_dict('field')
        self.assertIn('checked', ext_dict)
        self.assertEqual(ext_dict['xtype'], 'checkbox')
        self.assertEqual(ext_dict['checked'], 1)

    def testChoiceField(self):
        choices = (('one', 'Option One'),('two', 'Option Two'))
        field = forms.ChoiceField(choices=choices)
        ext_dict = field.to_ext_dict('field')
        self.assertIn('defaultType', ext_dict)
        self.assertIn('items', ext_dict)
        self.assertEqual(ext_dict['xtype'], 'fieldcontainer')
        self.assertEqual(len(ext_dict['items']), 2)
        item1 = ext_dict['items'][0]
        self.assertIn('boxLabel', item1)
        self.assertIn('name', item1)
        self.assertIn('inputValue', item1)
        self.assertEqual(item1['boxLabel'], 'Option One')
        self.assertEqual(item1['name'], 'field')
        self.assertEqual(item1['inputValue'], 'one')

    def testModelChoiceField(self):
        from ws.models import Workflow
        wf1 = Workflow(name='wf1')
        wf1.save()
        wf2 = Workflow(name='wf2')
        wf2.save()
        wf3 = Workflow(name='wf3')
        wf3.save()
        field = forms.ModelChoiceField(queryset=Workflow.objects.all(),
                                      empty_label=None)
        ext_dict = field.to_ext_dict('field')
        self.assertIn('defaultType', ext_dict)
        self.assertIn('items', ext_dict)
        self.assertEqual(ext_dict['xtype'], 'fieldcontainer')
        self.assertEqual(len(ext_dict['items']), 3)
        item1 = ext_dict['items'][0]
        self.assertIn('boxLabel', item1)
        self.assertIn('name', item1)
        self.assertIn('inputValue', item1)
        self.assertEqual(item1['boxLabel'], 'wf1')
        self.assertEqual(item1['name'], 'field')
        self.assertEqual(item1['inputValue'], 1)

    def testForm(self):
        class TestForm(forms.BPMTaskForm):
            one = forms.IntegerField()
            two = forms.CharField()

        field = forms.IntegerField()
        testform = TestForm()
        fields = testform.get_fields()
        self.assertEqual(len(fields), 2)
        self.assertEqual(field.to_ext_dict('one'), fields[0])

class TaskFormsTestCase(TestCase):

    def testInfoRequired(self):
        #Node1: this task needs two arguments, give two
        node1 = Node(name="test node 1",
                     workflow_id=1,
                     role_id=1,
                     celery_task=add,
                     params={"a":1,"b":1})
        node1.save()
        #Node2: this task needs two arguments, give one
        node2 = Node(name="test node 2",
                     workflow_id=1,
                     role_id=1,
                     celery_task=add,
                     params={"a":1})
        node2.save()
        #Node3: this task needs no arguments
        node3 = Node(name="test node 3",
                     workflow_id=1,
                     role_id=1,
                     celery_task=dummy,
                     params={})
        node3.save()
        self.assertEqual(node1.info_required, False)
        self.assertEqual(node2.info_required, True)
        self.assertEqual(node3.info_required, False)
