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
"""
WS forms.


"""

from functools import wraps

from django.forms import *
from django.core import validators


def with_cleaned_data(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'cleaned_data'):
            return func(self, *args, **kwargs)
        else:
            return ''
    return wrapper


class BPMTaskForm(Form):
    """
        A Django :class:`Form` with some additions for ExtJS integration
    """
    def get_title(self):
        return ''

    def get_description(self):
        return ''

    def get_fields(self, params={}):
        fields = []
        for key, field in self.fields.items():
            if not key in params:
                fields.append(field.to_ext_dict(key))
        return fields


class Field(Field):
    """
    Base class for ws form fields.
    """
    def to_ext_dict(self, fieldname):
        """ Returns a dictionary with field information for ExtJS.  """
        ext_dict = {
            'name': fieldname,
            'xtype': 'textfield',  # Default field type
        }
        ext_dict['fieldLabel'] = self.label or fieldname

        if self.initial:
            ext_dict['value'] = self.initial

        self.field_extras(ext_dict)
        return ext_dict

    def field_extras(self, ext_dict):
        """
        ws forms fiels must define this function with specific information.

        See already implemented fields for examples.
        """
        raise NotImplementedError


class IntegerField(Field, IntegerField):
    def field_extras(self, ext_dict):
        ext_dict['xtype'] = 'numberfield'
        for validator in self.validators:
            if type(validator) == validators.MaxValueValidator:
                ext_dict['max_value'] = validator.limit_value
            elif type(validator) == validators.MinValueValidator:
                ext_dict['min_value'] = validator.limit_value


class CharField(Field, CharField):
    def field_extras(self, ext_dict):
        if type(self.widget) == Textarea:
            ext_dict['xtype'] = 'textarea'
        for validator in self.validators:
            if type(validator) == validators.MinLengthValidator:
                ext_dict['minLength'] = validator.limit_value
            elif type(validator) == validators.MaxLengthValidator:
                ext_dict['maxLength'] = validator.limit_value


class BooleanField(Field, BooleanField):
    def field_extras(self, ext_dict):
        ext_dict['xtype'] = 'checkbox'
        if self.initial:
            ext_dict['checked'] = self.initial


class ChoiceField(Field, ChoiceField):
    def field_extras(self, ext_dict):
        fieldname = ext_dict['name']
        ext_dict['xtype'] = 'fieldcontainer'
        ext_dict['name'] = 'fieldcontainer-' + fieldname
        ext_dict['defaultType'] = 'radiofield'
        ext_dict['items'] = []
        for item in self.choices:
            ext_dict['items'].append({
                'boxLabel': item[1],
                'name': fieldname,
                'inputValue': item[0],
            })


class ModelChoiceField(ModelChoiceField, ChoiceField):
    pass
