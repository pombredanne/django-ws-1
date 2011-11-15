from django.test import TestCase
from ws.celery import forms

class FormsTestCase(TestCase):

    def testField(self):
        testfield = forms.CharField(
                required=False,
                label='Test field',
                initial=2,
                help_text='Test help text')
        ext_dict = testfield.to_ext_dict('testfield')
        self.assertTrue('name' in ext_dict)
        self.assertTrue('xtype' in ext_dict)
        self.assertTrue('fieldLabel' in ext_dict)
        self.assertTrue('value' in ext_dict)
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
        self.assertTrue('max_value' in ext_dict)
        self.assertTrue('min_value' in ext_dict)
        self.assertEqual(ext_dict['max_value'], 999)
        self.assertEqual(ext_dict['min_value'], 0)

    def testCharField(self):
        testfield = forms.CharField(
                max_length=5,
                min_length=1)
        ext_dict = testfield.to_ext_dict('testfield')
        self.assertTrue('maxLength' in ext_dict)
        self.assertTrue('minLength' in ext_dict)
        self.assertEqual(ext_dict['maxLength'], 5)
        self.assertEqual(ext_dict['minLength'], 1)

    def testForm(self):
        class TestForm(forms.BPMTaskForm):
            one = forms.IntegerField()
            two = forms.CharField()

        testform = TestForm()
        fields = testform.get_fields()
        self.assertEqual(len(fields), 2)
