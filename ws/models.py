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

class CreateNewChapter(AssetedProcess):
    serie = models.CharField(max_length=250)
    number = models.CharField(max_length=50)

class AdministrativeProcess(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
