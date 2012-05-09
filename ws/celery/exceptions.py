from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ObjectDoesNotExist(ObjectDoesNotExist):
    def __init__(self, *args, **kwargs):
        super(ObjectDoesNotExist, self).__init__(*args, **kwargs)


class MultipleObjectsReturned(MultipleObjectsReturned):
    def __init__(self, *args, **kwargs):
        super(MultipleObjectsReturned, self).__init__(*args, **kwargs)
