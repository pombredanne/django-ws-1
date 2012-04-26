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

'''Celery bindings, signal handling and BPM's logical tasks.

Submodules:
    bpm         -- BPM's logical tasks
    shortcuts   -- BPM's logic helpers and shortcuts
    signals     -- binding beetween Celery's signals and BPM' logical tasks
'''


from ws.celery.signals import SignalResponses
from ws.celery.bpm import (task_started, task_failed, task_retried, 
        task_succeeded)

bindings = SignalResponses()
bindings.connect(
        task_started=task_started,
        task_failed=task_failed,
        task_retried=task_retried,
        task_succeeded=task_succeeded,
        # task_revoked is called from Task model
        # task_progress is called from BPMTask class
        )
