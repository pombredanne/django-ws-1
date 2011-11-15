from django import forms
from django.core import validators

class BPMTaskForm(forms.Form):
    def get_fields(self):
        fields = []
        for key,field in self.fields.items():
            fields.append(field.to_ext_dict(key))
        return fields


class Field(forms.Field):
    def to_ext_dict(self, fieldname):
        ext_dict = {
            'name': fieldname,
            'xtype': 'textfield', #Default field type
        }
        if self.label:
            ext_dict['fieldLabel'] = self.label
        if self.initial:
            ext_dict['value'] = self.initial
        
        self.field_extras(ext_dict)
        return ext_dict

    def field_extras(self, ext_dict):
        raise NotImplementedError

class IntegerField(Field, forms.IntegerField):
    def field_extras(self, ext_dict):
        ext_dict['xtype'] = 'numberfield'
        for validator in self.validators:
            if type(validator) == validators.MaxValueValidator:
                ext_dict['max_value'] = validator.limit_value
            elif type(validator) == validators.MinValueValidator:
                ext_dict['min_value'] = validator.limit_value

class CharField(Field, forms.CharField):
    def field_extras(self, ext_dict):
        for validator in self.validators:
            if type(validator) == validators.MinLengthValidator:
                ext_dict['minLength'] = validator.limit_value
            elif type(validator) == validators.MaxLengthValidator:
                ext_dict['maxLength'] = validator.limit_value
