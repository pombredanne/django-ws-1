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

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ObjectDoesNotExist(ObjectDoesNotExist):
    def __init__(self, *args, **kwargs):
        super(ObjectDoesNotExist, self).__init__(*args, **kwargs)


class MultipleObjectsReturned(MultipleObjectsReturned):
    def __init__(self, *args, **kwargs):
        super(MultipleObjectsReturned, self).__init__(*args, **kwargs)
