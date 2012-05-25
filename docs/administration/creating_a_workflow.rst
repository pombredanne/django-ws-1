===================
Creating a workflow
===================

In this section we'll see how to create new workflows through an example,
"Organizing a conference":

    First the call for papers is sent, and begins the search for a location.
    When there are sufficient talks and the location is chosen begins the
    propaganda. Then subscriptions are accounted until the starting day comes,
    when the conference finally begins.

The graph could be something like this:

.. graphviz::

    digraph conference {
        "Send the Call for Papers" -> "Collect papers"
        "Collect papers" -> "Publicize"
        "Search a location" -> "Publicize"
        "Publicize" -> "Mailing"
        "Publicize" -> "Newspapers"
        "Publicize" -> "Poster"
        "Mailing"    -> "Receive subscriptions"
        "Newspapers" -> "Receive subscriptions"
        "Poster"     -> "Receive subscriptions"
        "Receive subscriptions" -> "Wait until the starting day"
        "Wait until the starting day" -> "Receive subscriptions"
        "Wait until the starting day" -> "Start the conference"
    };


Using django admin interface
============================

We'll see how to create the "Organizing a conference" workflow using
Django's admin interface:

.. image:: /images/ws-admin.png
    :align: center


Create the workflow
-------------------

The new workflow's only required attribute is name: "Organizing conference"

Node
    * name: "Send the Call for Papers"
    * is start: True
    * split: AND
    * role: Organization
    * celery task: conferencer.tasks.mailing
Node
    * name: "Collect papers"
    * join: AND
    * split: AND
    * role: Accounting
    * celery task: conferencer.tasks.ask_human
Node
    * name: "Publicize"
    * join: AND
    * split: AND
    * role: Accounting
    * celery task: conferencer.tasks.ask_human


Using fixtures
==============

Using python
============

Create the workflow::

    from ws.models import Workflow, Node, Transition, Process
    from ws.tasks.dummy import dummy

    # Create a workflow and save it
    workflow = Workflow.objects.create()

    # Create three nodes for the workflow tied to dummy tasks and save them
    first = Node.objects.create(name='first', workflow=workflow, celery_task=dummy, is_start=True)
    second = Node.objects.create(name='second', workflow=workflow, celery_task=dummy)
    third = Node.objects.create(name='third', workflow=workflow, celery_task=dummy, is_end=True)

    # Create two transitions to bind the nodes
    Transition.objects.create(parent=first, child=second)
    Transition.objects.create(parent=second, child=third)


Execute the workflow::

    process = Process.objects.create(workflow=workflow)
    process.start()
