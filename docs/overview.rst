========
Overview
========

django-ws is a Business Process Manager for Django. It uses Celery for asynchronous task automation and
ExtJS for web interface.


Basic structure
===============


Workflows
---------

*Workflows* consist of *nodes* (at least a beginning and an ending one) tied together though *transitions*. The *nodes* have related Celery *tasks* that are executed.


Nodes
-----

*Nodes* are entities related to workflows and celery tasks. They also have a joining condition and a splitting condition (*AND* or *XOR*):

    * if a node has *AND* as the condition for joining, all the transitions that point to this node must be fulfilled.
    * if a node has *XOR* as the condition for joining, only one of the transitions that point to this node must be fulfilled. When it does, all other parent nodes are stopped.
    * if a node has *AND* as the condition for splitting, when this node is successful, all the children transitions that match the result will be notified.
    * if a node has *XOR* as the condition for splitting, when this node is successful, only one of the children transitions that match the result will be notified.
      
    .. todo:: *OR* conditions


Transitions
-----------

*Transitions* are bindings that tie together two *nodes* in a *workflow*. They also have an optional condition witch must be fulfilled for the *transition* to be successful.


Processes
---------

*Processes* are executions of *workflows*. Besides having a starting and an ending date, they also keep track of the process status.


Tasks
-----

*Tasks* are executions of *nodes* in a given *process*. Besides having a starting and an ending date, they also keep track of the undergoing celery task status, progress and result.


Task execution parameters
=========================

Celery tasks need execution parameters. This parameters can be defined in *workflow*, *process*, *node*, *task* models and will automatically inherit from one another, being the last ones the parameters define in *tasks*. In this way, you can define *workflow* wide execution parameters and override them for a given task.


Task execution priorities
=========================


User permissions
================
