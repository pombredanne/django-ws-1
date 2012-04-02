__all__ = [ 'http', 'bpm', 'dummy']


from celery.loaders import current_loader
current_loader = current_loader()

for module in __all__:
    current_loader.import_module('{0}.{1}'.format(__name__, module))
