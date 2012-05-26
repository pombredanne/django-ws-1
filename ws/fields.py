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

from django.db.models import CharField, SubfieldBase

from ws.utils import import_task


class CeleryTaskString(str):
    @property
    def obj(self):
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
