from django.utils.importlib import import_module

def import_task(path):
    module, _, task = path.rpartition('.')
    module = import_module(module)
    return getattr(module, task)
