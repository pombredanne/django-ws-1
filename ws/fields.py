from django.db.models import CharField, SubfieldBase
from django.utils.importlib import import_module
from django.utils.functional import curry
from django.utils.encoding import force_unicode, smart_unicode


def _get_FIELD_display(self, field):
    value = field.get_prep_value(getattr(self, field.attname))
    return force_unicode(dict(field.flatchoices).get(value, value), strings_only=True)


class CeleryTaskField(CharField):
    __metaclass__ = SubfieldBase

    def to_python(self, value):
        if isinstance(value, str) or isinstance(value, unicode):
            if value:
                module, _, task = value.rpartition('.')
                module = import_module(module)
                return getattr(module, task)
            else:
                return None
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

    def clean(self, value, model_instance):
        value = self.get_prep_value(value)
        self.validate(value, model_instance)
        self.run_validators(value)
        return value

    def value_to_string(self, obj):
        return smart_unicode(self.get_prep_value(self._get_val_from_obj(obj)))

    def formfield(self, *args, **kwargs):
        kwargs['coerce'] = super(CeleryTaskField, self).to_python
        return super(CeleryTaskField, self).formfield(*args, **kwargs)

    def value_from_object(self, obj):
        return self.get_prep_value(getattr(obj, self.attname))

    def contribute_to_class(self, cls, name):
        super(CeleryTaskField, self).contribute_to_class(cls, name)
        if self.choices:
            setattr(cls, 'get_{}_display'.format(self.name),
                    curry(_get_FIELD_display, field=self))

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^ws\.fields\.CeleryTaskField"])
except ImportError:
    pass
