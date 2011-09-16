from django.db import models
from goflow.workflow.models import Process
from django.contrib.contenttypes.models import ContentType

class ProcessLauncher(models.Model):
    title = models.CharField(max_length=250)
    """ Ties one goflow process (workflow) to one metadata generic object. """
    workflow = models.ForeignKey(Process)
    content_type = models.ForeignKey(ContentType)

    def __unicode__(self):
        return self.title

class AssetedProcess(models.Model):
    asset_id = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    description = models.TextField()

    def ext_fields(self):
        return [{
            'name': 'asset_id',
            'label': 'Asset ID',
            'type': 'textfield',
            'default': '',
            'help': 'The identifier of this asset.'
        },{
            'name': 'title',
            'label': 'Title',
            'type': 'textfield',
            'default': '',
            'help': 'The title of this process.'
        },{
            'name': 'description',
            'label': 'Description',
            'type': 'textareafield',
            'default': 'This is the description',
            'help': 'The description of this process.'
        }]

class CreateNewChapter(AssetedProcess):
    serie = models.CharField(max_length=250)
    number = models.CharField(max_length=50)

    def ext_fields(self):
        return AssetedProcess.ext_fields(self) + [{
            'name': 'serie',
            'label': 'Serie',
            'type': 'textfield',
            'default': '',
            'help': 'The title of this serie.'
        },{
            'name': 'number',
            'label': 'Number',
            'type': 'textfield',
            'default': '',
            'help': 'The number of this chapter.'
        }]

class AdministrativeProcess(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def ext_fields(self):
        return [{
            'name': 'title',
            'label': 'Title',
            'type': 'textfield',
            'default': '',
            'help': 'The title of this process.'
        },{
            'name': 'description',
            'label': 'Description',
            'type': 'textareafield',
            'default': 'This is the description',
            'help': 'The description of this process.'
        }]
