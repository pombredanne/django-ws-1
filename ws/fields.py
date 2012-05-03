from django.db.models import CharField, SubfieldBase
from django.utils.importlib import import_module

class CeleryTaskField(CharField):
    __metaclass__ = SubfieldBase

    def to_python(self, value):
        if isinstance(value, str) or isinstance(value, unicode):
            module, _, task = value.rpartition('.')
            module = import_module(module)
            return getattr(module, task)
        elif hasattr(value, 'name'):
            return value
        else:
            raise TypeError

    def get_prep_value(self, value):
        if isinstance(value, str) or isinstance(value, unicode):
            return value
        elif hasattr(value, 'name'):
            return value.name
        else:
            raise TypeError

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^ws\.fields\.CeleryTaskField"])
except ImportError:
    pass
