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
Functions:
    :func:`load_task_submodules`
        automatically load all submodules
"""

import os
from importlib import import_module

from djcelery.loaders import DjangoLoader
from djcelery.loaders import autodiscover as djcelery_autodiscover

from ws.conf import load_settings


class WSLoader(DjangoLoader):
    def on_worker_init(self):
        super(WSLoader, self).on_worker_init()
        autodiscover()

    def read_configuration(self):
        load_settings()
        return super(WSLoader, self).read_configuration()

def autodiscover():
    djcelery_autodiscover()
    load_task_submodules('ws.tasks')
    import_module('ws.celery.bpm')

def load_task_submodules(module_name):
    """Load submodules of module so that tasks are automatically detected by celery."""
    module = import_module(module_name)
    directory = os.path.dirname(module.__file__)
    modules = []
    for filename in os.listdir(directory):
        filename, extension = os.path.splitext(filename)
        if extension == '.py':
            modules.append(import_module('{}.{}'.format(module_name, filename)))
    return modules
