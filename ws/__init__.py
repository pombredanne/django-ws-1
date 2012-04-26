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

from __future__ import absolute_import

from celery.states import READY_STATES
from celery.registry import tasks as task_registry


STATES = dict([(s,s) for s in ('PENDING', 'RETRY', 'STARTED') + tuple(READY_STATES) ])

CONDITIONS = dict([(s,s) for s in ('XOR', 'AND')])

def get_registered_tasks():
    from celery.loaders import current_loader
    from ws.celery.tasks import BPMTask
    current_loader = current_loader()
    current_loader.import_default_modules()
    return [ key for key, value in task_registry.items()\
            if isinstance(value, BPMTask) ]
