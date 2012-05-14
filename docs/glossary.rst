========
Glossary
========

.. glossary::

    Workflow
        A collection of nodes, tied by transitions. A worfklow must have at
        least one starting node.

    Node
        A concrete step of the workflow, defines *WHO* must do *WHAT*.

        Each node executes a celery task. It can define all required parameters
        or leave some empty. If at the time of execution some parameters are
        still missing human intervention is requested.

        Each node has a role assigned. When human intervention is requested the
        target user is chosen from this group.

    Role
        A Group of users with a defined role in the process. The users of this
        group will be responsible of the task; at this moment this only means
        that thew will set the missed parameters from the node's celery task.

        To control when the node must be fired a join condition is defined:

        * if a node has *AND* as the condition for joining, all the transitions
          that point to this node must be fulfilled.
        * if a node has *XOR* as the condition for joining, only one of the
          transitions that point to this node must be fulfilled. When it does,
          all other parent nodes are stopped.

        To control what to do when a node is finished, a split condition is
        defined:

        * if a node has *AND* as the condition for splitting, when this node is
          successful, all the children transitions that match the result will
          be notified.
        * if a node has *XOR* as the condition for splitting, when this node is
          successful, only one of the children transitions that match the
          result will be notified.

        Any node can be set as starting point of the workflow. If there are
        more than one starting nodes all are fired in parallel.

        Any node can be a ending point of the workflow. After any of the ending
        nodes is executed the workflow is terminated.
          
        .. todo:: *OR* conditions

    Celery task
        Each node executes some automation: send a file somewhere, notify
        someone when a task is finished, etc. This automations are implemented
        with Celery.

    Transition
        Binding that tie together two *nodes* in a *workflow*. They also have
        an optional condition witch must be fulfilled for the *transition* to
        be valid.

    Process
        Execution of a *workflow*. Besides having a starting and an ending
        date, also keeps track of the process status.


    Task
        Execution of a *node* in a given *process*. Besides having a starting
        and an ending date, also keeps track of the undergoing celery task
        status, progress and result.

        When a task is started tries to get all parametters for the celery
        task. This parameters can be defined in *workflow*, *process*, *node*,
        *task* models and will automatically inherit from one another, being
        the last ones the parameters define in *tasks*. In this way, you can
        define *workflow* wide execution parameters and override them for a
        given task.

        If there is some missing parametter the task goes into PENDING state. A
        user from the node's role must fill the gaps.

    Role
        A pool of users electible for performing some task. Only the users
        of the specified role can do the task.
