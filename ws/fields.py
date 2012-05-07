from django.db.models import CharField, SubfieldBase

from ws.utils import import_task


class CeleryTaskString(str):
    @property
    def task(self):
        return import_task(self)


class CeleryTaskField(CharField):
    __metaclass__ = SubfieldBase

    def to_python(self, value):
        if hasattr(value, 'name'):
            value = value.name
        return CeleryTaskString(value)

    def get_prep_value(self, value):
        if isinstance(value, basestring):
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
