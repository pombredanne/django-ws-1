===================
Creating a workflow
===================


Create the workflow::

    from ws.models import Workflow, Node, Transition, Process

    # Create a workflow and save it
    workflow = Workflow.objects.create()

    # Create three nodes for the workflow tied to dummy tasks and save them
    first = Node.objects.create(name='first', workflow=workflow, task_name='ws.tasks.dummy.dummy')
    second = Node.objects.create(name='second', workflow=workflow, task_name='ws.tasks.dummy.dummy')
    third = Node.objects.create(name='third', workflow=workflow, task_name='ws.tasks.dummy.dummy')

    # Establish the beginning and the ending of the workflow
    workflow.beginning = first
    workflow.ending = third
    workflow.save()

    # Create two transitions to bind the nodes
    Transition.objects.create(parent=first, child=second)
    Transition.objects.create(parent=second, child=third)


Execute the workflow::

    process = Process.objects.create(workflow=workflow)
    process.start()
